from pydantic import BaseModel, field_validator
from decimal import Decimal

class AccountOut(BaseModel):
    id: int
    balance: Decimal

class DepositIn(BaseModel):
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def validate_positive(cls, v: Decimal):
        if v <= 0:
            raise ValueError("Valor deve ser positivo")
        return v

class WithdrawIn(BaseModel):
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def validate_positive(cls, v: Decimal):
        if v <= 0:
            raise ValueError("Valor deve ser positivo")
        return v