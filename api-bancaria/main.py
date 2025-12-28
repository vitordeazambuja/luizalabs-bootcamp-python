from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, engine, metadata

import auth.model
import accounts.model
import transactions.model

from auth.controller import router as auth_router
from accounts.controller import router as accounts_router

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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])