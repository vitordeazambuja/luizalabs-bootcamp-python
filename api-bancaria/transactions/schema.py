from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: Decimal

class TransactionOut(BaseModel):
    id: int
    type: str
    amount: Decimal
    created_at: datetime