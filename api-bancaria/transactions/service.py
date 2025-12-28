from transactions.model import transactions
from database import database
from decimal import Decimal

class TransactionService:
    async def create(self, account_id: int, type_: str, amount: Decimal):
        query = transactions.insert().values(
            account_id=account_id,
            type=type_,
            amount=amount,
        )
        await database.execute(query)

    async def list_by_account(self, account_id: int):
        query = (
            transactions.select()
            .where(transactions.c.account_id == account_id)
            .order_by(transactions.c.created_at.desc())
        )

        return await database.fetch_all(query)