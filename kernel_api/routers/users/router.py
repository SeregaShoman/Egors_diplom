from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, HTTPException

from dependencies import decode_token, get_db_session
from .services import get_users_by_event_id, get_user_by_id

users_router = APIRouter(
    tags=["Роутер для манипуляций с пользователями"],
    prefix="/users",
    default_response_class=ORJSONResponse
)


@users_router.get(
    path="/by_event_id",
    status_code=status.HTTP_200_OK
)
async def get_users_registered_in_events(
    event_id: str,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] in ["Партнёр", "Админ"]:
        users =  await get_users_by_event_id(event_id, db_session)
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не можешь получить эти данные"
        )
    

@users_router.get(
    path="/by_id",
    status_code=status.HTTP_200_OK
)
async def get_users_by_id(
    user_id: str,
    db_session: AsyncSession = Depends(get_db_session)
):
    users =  await get_user_by_id(user_id, db_session)
    return users