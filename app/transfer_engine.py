import uuid
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Account, Transaction, JournalEntry, EntryDirection

def execute_transfer(db: Session, req, user_id: uuid.UUID):
    if req.source_account_id == req.destination_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account.")

    first_id, second_id = sorted([req.source_account_id, req.destination_account_id])

    try:
        acc1 = db.execute(select(Account).filter_by(id=first_id).with_for_update()).scalar_one_or_none()
        acc2 = db.execute(select(Account).filter_by(id=second_id).with_for_update()).scalar_one_or_none()

        if not acc1 or not acc2:
            raise HTTPException(status_code=404, detail="Account not found.")

        sender = acc1 if acc1.id == req.source_account_id else acc2
        receiver = acc2 if acc2.id == req.destination_account_id else acc1

        if sender.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized access to source account.")
        if sender.balance < req.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds.")

        ref = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        txn = Transaction(
            reference_number=ref, idempotency_key=req.idempotency_key,
            source_account_id=sender.id, destination_account_id=receiver.id,
            amount=req.amount
        )
        db.add(txn)
        db.flush()

        sender.balance -= req.amount
        receiver.balance += req.amount
        sender.version += 1
        receiver.version += 1

        db.add(JournalEntry(transaction_id=txn.id, account_id=sender.id, direction=EntryDirection.DEBIT, amount=req.amount, balance_after=sender.balance))
        db.add(JournalEntry(transaction_id=txn.id, account_id=receiver.id, direction=EntryDirection.CREDIT, amount=req.amount, balance_after=receiver.balance))

        db.commit()
        return {"transaction_id": txn.id, "reference": ref, "status": "SUCCESS"}
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))