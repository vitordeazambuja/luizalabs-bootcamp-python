from sqlalchemy import Table, Column, Integer, ForeignKey, Numeric
from database import metadata

accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), unique=True, nullable=False),
    Column("balance", Numeric(12,2), default=0),
)