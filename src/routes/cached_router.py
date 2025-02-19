from time import sleep

from cachetools import TTLCache, cached
from fastapi import APIRouter

cached_router = APIRouter(tags=["Cache"])


@cached(cache=TTLCache(maxsize=1024, ttl=30))
def my_result():
    sleep(5)
    return {"message": "This call is sometimes cached"}


@cached_router.get("/cached")
async def get_cached():
    return my_result()
