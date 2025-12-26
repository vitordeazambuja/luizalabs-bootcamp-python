from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "sqlite+aiosqlite:///./api_bancaria.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL.replace("+aiosqlite",""),
    connect_args={"check_same_thread": False}
)