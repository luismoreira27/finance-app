from sqlalchemy import Column, Integer, String, Float
from backend.finance_db import Base_finance

class TransactionModel(Base_finance):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key = True)
    date = Column(String)
    category = Column(String)
    amount = Column(Float)
    note = Column(String)