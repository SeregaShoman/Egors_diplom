from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, HTTPException

from .schemas import UserUpdateSchema
from dependencies import decode_token, get_db_session
from .services import (
    get_users_by_event_id, get_user_by_id, 
    update_user_in_db, delete_user_and_related_data
)

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


@users_router.put(
    path="/by_id",
    status_code=status.HTTP_200_OK
)
async def update_user_by_id(
    user_id: str | None,
    it_self: bool,
    user_data: UserUpdateSchema,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] in ["Партнёр", "Админ"] and it_self == False:
        await update_user_in_db(
            user_id, db_session, user_data, 
            user_data.student_info, user_data.partner_info
        )
    if token["role"] in ["Партнёр", "Админ", "Студент"] and it_self == True:
        await update_user_in_db(
            user_id, db_session, user_data, 
            user_data.student_info, user_data.partner_info
        )
    return {"msg": "Ты успешно обновил данные!"}


@users_router.delete(
    path="/by_id",
    status_code=status.HTTP_200_OK
)
async def delete_user_by_id(
    user_id: str | None,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] in ["Админ"]:
        await delete_user_and_related_data(user_id, db_session)
    return {"msg": "Ты успешно удалил данные!"}