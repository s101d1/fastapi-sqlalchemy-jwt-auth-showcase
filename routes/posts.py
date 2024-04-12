from typing import List
from uuid import UUID

from cachetools import TTLCache
from fastapi import APIRouter, Depends, Response, status, Path

from controllers.post import get_posts, add_post, delete_post
from deps.auth import get_current_user
from models.dto.post import AddPostData, PostResponse

router = APIRouter(prefix="/posts")

_cache = TTLCache(maxsize=1024 * 1024, ttl=300)  # memory cache with 5 minutes (300 secs) TTL


def get_posts_cache_key(user_id: UUID):
    """
        Return cache key for the GET /posts cache
    """
    return "get_posts_" + str(user_id)


@router.get("/", tags=["posts"])
async def get_posts_route(user_id: UUID = Depends(get_current_user)) -> List[PostResponse]:
    """
        Get posts route
    """
    cache_key = get_posts_cache_key(user_id)
    cache_value = _cache.get(cache_key)
    if cache_value is None:
        result = get_posts(user_id)
        _cache[cache_key] = result
        return result

    return cache_value


@router.post("/", tags=["posts"])
async def add_post_route(data: AddPostData, response: Response,
                         user_id: UUID = Depends(get_current_user)):
    """
        Add post route
    """
    response.status_code = status.HTTP_201_CREATED
    result = add_post(data, user_id)

    # clear GET /posts cache for the authenticated user
    _cache.pop(get_posts_cache_key(user_id), None)

    return result


@router.delete("/{post_id}", tags=["posts"])
async def delete_post_route(post_id: UUID = Path(title="The ID of the Post to delete"),
                            user_id: UUID = Depends(get_current_user)):
    """
        Delete post route
    """
    result = delete_post(post_id, user_id)

    if result["deleted"]:
        # clear GET /posts cache for the authenticated user
        _cache.pop(get_posts_cache_key(user_id), None)

    return result
