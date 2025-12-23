import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    assert service.create(PostIn(title="post 1", content="some content", published=True))
    assert service.create(PostIn(title="post 2", content="some content", published=True))
    assert service.create(PostIn(title="post 3", content="some content", published=False))

@pytest.mark.parametrize("published,total", [("on", 2), ("off",1)])
async def test_read_posts_by_status_success(client: AsyncClient, access_token: str, published: str, total: int):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total