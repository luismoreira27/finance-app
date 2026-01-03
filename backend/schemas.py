from pydantic import BaseModel
from typing import List

class TransactionBase(BaseModel):
    date : str
    category : str
    amount : float
    note : str | None = None


class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionSchema(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class DeleteTransactionsRequest(BaseModel):
    transaction_ids: List[int]