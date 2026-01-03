from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.finance_db import SessionLocal
from backend.models import TransactionModel
from backend.schemas import (
    TransactionSchema,
    TransactionCreate,
    TransactionUpdate
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[TransactionSchema])
def get_all(db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).all()

    return transactions

@router.post("/", response_model = TransactionSchema)
def create(t: TransactionCreate, db: Session = Depends(get_db)):    
    db_t = TransactionModel(**t.model_dump())
    db.add(db_t)
    db.commit()
    db.refresh(db_t)

    return db_t

@router.put("/{transaction_id}", response_model = TransactionSchema)
def update(transaction_id: int, 
           update_data: TransactionUpdate, 
           db: Session = Depends(get_db)
           ):
    t = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    
    if not t:
        raise HTTPException(status_code = 404, detail = "Transaction not found!")
    
    for key, value in update_data.model_dump(exclude_unset = True).items():
        setattr(t, key, value)

    db.commit()
    db.refresh(t)
    return t

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    t = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if t:
        db.delete(t)
        db.commit()
    
    if not t:
        raise HTTPException(status_code = 404, detail = "Transaction not found!")
    return {"message": "Transaction deleted!"}