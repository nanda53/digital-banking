from . import models, security
from .database import SessionLocal
# --- AUTO-SEED DATABASE FOR DEMONSTRATION ---
def seed_database():
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            print("Seeding database with demo accounts...")
            pw_hash = security.get_password_hash("demo123")
            
            alice = models.User(email="alice@bank.com", hashed_password=pw_hash)
            bob = models.User(email="bob@bank.com", hashed_password=pw_hash)
            db.add_all([alice, bob])
            db.commit()
            
            acc_alice = models.Account(account_number="ACC-ALICE-01", user_id=alice.id, balance=50000.00)
            acc_bob = models.Account(account_number="ACC-BOB-01", user_id=bob.id, balance=15000.00)
            db.add_all([acc_alice, acc_bob])
            db.commit()
            print(f"Seed complete! Alice ID: {acc_alice.id} | Bob ID: {acc_bob.id}")
    finally:
        db.close()

seed_database()
# --------------------------------------------


def run_seed():
    db = SessionLocal()
    try:
        # Check if Bob already exists
        bob_user = db.query(models.User).filter(models.User.email == "bob@bank.com").first()
        
        if not bob_user:
            print("Creating sample user Bob...")
            pw_hash = security.get_password_hash("demo123")
            bob = models.User(email="bob@bank.com", hashed_password=pw_hash)
            db.add(bob)
            db.commit()
            
            acc_bob = models.Account(account_number="ACC-BOB-01", user_id=bob.id, balance=15000.00)
            db.add(acc_bob)
            db.commit()
            
            print(f"\n" + "="*50)
            print(f"=== COPY THIS ID TO SEND MONEY TO BOB ===")
            print(f"{acc_bob.id}")
            print("="*50 + "\n")
        else:
            acc_bob = db.query(models.Account).filter(models.Account.user_id == bob_user.id).first()
            print(f"\n" + "="*50)
            print(f"=== COPY THIS ID TO SEND MONEY TO BOB ===")
            print(f"{acc_bob.id}")
            print("="*50 + "\n")
    finally:
        db.close()