from fastapi import APIRouter, status
from auth.schema import UserCreate
from auth.service import AuthService

router = APIRouter()
service = AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    user_id = await service.create_user(email=user.email, password=user.password,)
    return {"message": "Usuario criado com sucesso"}

@router.post("/login")
async def login(user: UserCreate):
    token = await service.login(email=user.email, password=user.password,)
    return {"access_token": token, "token_type": "bearer"}