from sqlalchemy import Table, Column, Integer, ForeignKey, Numeric, String, DateTime, func
from datetime import datetime
from database import metadata

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("account_id", ForeignKey("accounts.id"), nullable=False),
    Column("type", String, nullable=False),
    Column("amount", Numeric(12,2), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(),nullable=False),
)