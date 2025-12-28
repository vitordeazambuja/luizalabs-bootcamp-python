from accounts.model import accounts
from database import database


class AccountService:
    async def create(self, user_id: int) -> int:
        query = accounts.insert().values(user_id=user_id, balance=0)
        return await database.execute(query)

    async def get_by_user(self, user_id: int):
        query = accounts.select().where(accounts.c.user_id == user_id)
        return await database.fetch_one(query)

    async def deposit(self, user_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Valor do depósito deve ser positivo")

        async with database.transaction():
            account = await self.get_by_user(user_id)
            if not account:
                raise ValueError("Conta não encontrada")

            new_balance = account["balance"] + amount

            query = (
                accounts.update()
                .where(accounts.c.id == account["id"])
                .values(balance=new_balance)
            )
            await database.execute(query)

            return new_balance

    async def withdraw(self, user_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Valor do saque deve ser positivo")

        async with database.transaction():
            account = await self.get_by_user(user_id)
            if not account:
                raise ValueError("Conta não encontrada")

            if account["balance"] < amount:
                raise ValueError("Saldo insuficiente")

            new_balance = account["balance"] - amount

            query = (
                accounts.update()
                .where(accounts.c.id == account["id"])
                .values(balance=new_balance)
            )
            await database.execute(query)

            return new_balance