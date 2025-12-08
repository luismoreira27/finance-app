from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./credentials.db"

engine_auth = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine_auth)

Base_auth = declarative_base()
metadata = MetaData()

class Credentials(Base_auth):
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    username = Column(String)
    password = Column(String)