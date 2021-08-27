from fastapi import APIRouter, HTTPException, status, Request

from fastapi.responses import RedirectResponse


from app.crud import urls as crud_urls
from app.crud import visits as crud_visits
from app.utils.misc import get_device_type, get_country


router = APIRouter()


@router.get("/{hash}")
async def main_redirect(hash: str, request: Request):
    try:
        url_data = await request.app.state.redis.hgetall(hash)
        if not url_data:
            url_data = await crud_urls.get_url_by_hash(hash)
            url_id, original_url = url_data["id"], url_data["original_url"]
            await request.app.state.redis.hmset(
                hash, {"id": url_id, "original_url": original_url})
        original_url = url_data.get("original_url")
        device = get_device_type(request.headers["user-agent"])
        country = await get_country(request)
        await crud_visits.create_visit(int(url_data["id"]), device, country)
        return RedirectResponse(url=original_url)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url Not Found'
        )
