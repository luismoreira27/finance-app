from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./finance.db"

engine_finance = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine_finance)

Base_finance = declarative_base()
metadata = MetaData()

class Transaction(Base_finance):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key = True)
    date = Column(String)
    category = Column(String)
    amount = Column(Float)
    note = Column(String)