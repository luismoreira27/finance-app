from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.finance_db import SessionLocal
from pydantic import BaseModel

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TransactionBase(BaseModel):
    date : str
    category : str
    amount : float
    note : str | None = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True


@router.get("/", response_model=list[Transaction])
def get_all(start_date: str, end_date: str, category: str, db: Session = Depends(get_db)):
    transactions = Session.query(Transaction).all()
    if start_date:
        transactions = [t for t in transactions if t.date >= start_date]
    if end_date:
        transactions = [t for t in transactions if t.date <= end_date]
    if category:
        transactions = [t for t in transactions if t.category.lower() == category.lower()]

    return transactions

@router.post("/", response_model = Transaction)
def create(t: TransactionCreate, db: Session = Depends(get_db)):
    db_t = Transaction(**TransactionCreate.dict())
    db.add(db_t)
    db.commit()
    db.refresh(db_t)

    return db_t

@router.delete("({transaction_id})")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if t:
        db.delete(t)
        db.commit()
    
    if not t:
        raise HTTPException(status_code = 404, detail = "Transaction not found!")
    return {"message": "Transaction deleted!"}