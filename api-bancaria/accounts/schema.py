from pydantic import BaseModel, PositiveFloat
from decimal import Decimal

class AccountOut(BaseModel):
    id: int
    balance: Decimal

class DepositIn(BaseModel):
    amount: PositiveFloat

class WithdrawIn(BaseModel):
    amount: PositiveFloat