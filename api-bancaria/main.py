from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, engine, metadata

import auth.model
import accounts.model
import transactions.model

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(
    title="API Bancária",
    lifespan=lifespan,
)