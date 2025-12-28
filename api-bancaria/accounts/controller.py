# accounts/controller.py
from fastapi import APIRouter, Depends, HTTPException, status

from accounts.schema import AccountOut, DepositIn, WithdrawIn
from accounts.service import AccountService
from core.security import get_current_user

from transactions.service import TransactionService

router = APIRouter(prefix="/accounts", tags=["Accounts"])
service = AccountService()
transaction_service = TransactionService()


@router.post("/me/deposit", response_model=AccountOut)
async def deposit(
    data: DepositIn,
    user=Depends(get_current_user),
):
    try:
        balance = await service.deposit(user_id=user["id"], amount=data.amount)
        account = await service.get_by_user(user["id"])

        if account is None:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        await transaction_service.create(account["id"], "deposit", data.amount)
        return {"id": user["id"], "balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/me/withdraw", response_model=AccountOut)
async def withdraw(
    data: WithdrawIn,
    user=Depends(get_current_user),
):
    try:
        balance = await service.withdraw(user_id=user["id"], amount=data.amount)
        account = await service.get_by_user(user["id"])

        if account is None:
            raise HTTPException(status_code=404, detail="Conta não encontrada")

        await transaction_service.create(account["id"], "withdraw", data.amount)
        return {"id": user["id"], "balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
