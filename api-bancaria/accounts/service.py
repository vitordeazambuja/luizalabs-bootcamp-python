from accounts.model import accounts
from database import database

class AccountService:
    async def create(self, user_id: int):
        query = accounts.insert().values(user_id=user_id)
        account_id = await database.execute(query)
        return account_id
    
    async def get_by_user(self, user_id: int):
        query = accounts.select().where(accounts.c.user_id == user_id)
        return await database.fetch_one(query)