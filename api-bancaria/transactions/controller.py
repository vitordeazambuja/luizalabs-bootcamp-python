from fastapi import APIRouter, Depends, HTTPException

from transactions.schema import TransactionOut
from transactions.service import TransactionService
from accounts.service import AccountService
from core.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

transaction_service = TransactionService()
account_service = AccountService()


@router.get("/me", response_model=list[TransactionOut])
async def statement(user=Depends(get_current_user)):
    account = await account_service.get_by_user(user["id"])

    if account is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    return await transaction_service.list_by_account(account["id"])
