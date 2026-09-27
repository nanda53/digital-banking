from pydantic import BaseModel, condecimal
from uuid import UUID

class UserCreate(BaseModel):
    email: str
    password: str

class TransferRequest(BaseModel):
    source_account_id: UUID
    destination_account_id: UUID
    amount: condecimal(gt=0, decimal_places=4) # type: ignore
    idempotency_key: str