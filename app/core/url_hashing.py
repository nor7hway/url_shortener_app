from app.crud.urls import get_url_by_hash
import shortuuid


def gen_short_url(length: int = 6):
    return shortuuid.uuid()[:length]


async def get_url_hash(original_url: str):
    url_hash = gen_short_url()
    while await get_url_by_hash(url_hash):
        url_hash = gen_short_url()
    return url_hash
