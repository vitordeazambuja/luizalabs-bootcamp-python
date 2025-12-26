from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="API Bancária",
    lifespan=lifespan,
)