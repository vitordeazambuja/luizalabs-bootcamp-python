from fastapi import status, Response, APIRouter, Depends
from schemas.post import PostIn, PostUpdateIn
from views.post import PostOut
from services.post import PostService
from security import login_required

router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])
service = PostService()

@router.get('/', response_model=list[PostOut])
async def read_posts(published: bool | None = None, limit: int = 10, skip: int = 0):
    return await service.read_all(published=published, limit=limit, skip=skip)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    post_id = await service.create(post)
    return {**post.model_dump(), "id": post_id}

@router.get("/{id}", response_model=PostOut)
async def read_post(id: int):
    return await service.read(id)

@router.patch("/{id}", response_model=PostOut)
async def update_post(id: int, post: PostUpdateIn):
    return await service.update(id=id, post=post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    await service.delete(id)