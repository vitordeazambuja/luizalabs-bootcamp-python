from fastapi import FastAPI
from controllers import post
import sqlalchemy as sa
import databases

DATABASE_URL = "sqlite:///./blog.db"

database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread":False})

metadata.create_all(engine)

app = FastAPI()
app.include_router(post.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()