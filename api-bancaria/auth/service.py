from sqlalchemy import select
from database import database
from auth.model import users
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:

    async def create_user(self, email: str, password: str):
        query = select(users).where(users.c.email == email)
        existing_user = await database.fetch_one(query)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ja registrado",)
        
        hashed_password = hash_password(password)

        insert_query = users.insert().values(email=email, password=hashed_password, is_active=True,)
        user_id = await database.execute(insert_query)

        return user_id
    
    async def login(self, email: str, password: str):
        query = select (users).where(users.c.email == email)
        user = await database.fetch_one(query)

        if not user or not verify_password(password, user["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciais invalidas")
        
        token = create_access_token({"sub": str(user["id"])})
        return token