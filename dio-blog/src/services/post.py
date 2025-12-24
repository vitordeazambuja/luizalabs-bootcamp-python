from database import database
from databases.interfaces import Record
from fastapi import HTTPException, status
from models.post import posts
from schemas.post import PostIn, PostUpdateIn
import sqlalchemy as sa

class PostService:
    async def read_all(self, published: bool | None, limit: int, skip: int = 0) -> list[Record]:
        query = posts.select()
        if published is not None:
            query = query.where(posts.c.published == published)
        query = query.limit(limit).offset(skip)
        return await database.fetch_all(query)
    
    async def create(self, post: PostIn) -> int:
        command = posts.insert().values(**post.model_dump())
        return await database.execute(command)
    
    async def read(self, id:int) -> Record:
        return await self.__get_by_id(id)
    
    async def update(self, id:int, post: PostUpdateIn) -> Record:
        data = post.model_dump(exclude_unset=True)
        if not data:
            return await self.__get_by_id(id)
        command = posts.update().where(posts.c.id == id).values(**data)
        await database.execute(command)
        
        return await self.__get_by_id(id)

    async def delete(self, id:int) -> None:
        command = posts.delete().where(posts.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id: int) -> Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
        
        return post