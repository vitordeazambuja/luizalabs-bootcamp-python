from fastapi import APIRouter, Depends
from core.security import get_current_user
from accounts.service import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])
service = AccountService()

@router.post("/", response_model=dict)
async def create_account(user=Depends(get_current_user)):
    account_id = await service.create(user_id=user["id"])
    return {"id": account_id}

@router.get("/me")
async def my_account(user=Depends(get_current_user)):
    return await service.get_by_user(user_id=user["id"])