from fastapi.responses import ORJSONResponse
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs import CONFIG
from .services import get_all_tags
from dependencies import get_db_session


static_tags_router = APIRouter(
    tags=["Роутер который вернёт статические данные о ТЭГАХ"],
    prefix="/tags",
    default_response_class=ORJSONResponse
)


@static_tags_router.get(
    path="/", status_code=status.HTTP_200_OK
)
async def get_static_tags(
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    return await get_all_tags(db_session)