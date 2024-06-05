from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, HTTPException

from dependencies import decode_token, get_db_session
from .schemas import EventSchema
from .services import (
    create_event, get_all, get_events_by_creator_id, 
    create_event_registration, get_events_by_user_id, update_event_in_db, get_users_by_event_id
)

event_router = APIRouter(
    tags=["Роутер для создания ивентов"],
    prefix="/event",
    default_response_class=ORJSONResponse
)


@event_router.post(
    path="/created",
    status_code=status.HTTP_201_CREATED
)
async def create_event_py_patner(
    event_data: EventSchema,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] != "Партнёр":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не можешь создавать ивенты."
        )
    else:
        new_event = await create_event(
            event_data, db_session, token["id"]
        )
        return {
            "msg":"Ивент был успешно создан", 
            "new_event":new_event.id
        }
    

@event_router.get(
    path="/get_all",
    status_code=status.HTTP_200_OK
)
async def get_all_events(
    db_session: AsyncSession = Depends(get_db_session)
):
    return await get_all(db_session)


@event_router.get(
    path="/get_all/by_creator",
    status_code=status.HTTP_200_OK
)
async def get_all_events_by_creator(
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] != "Партнёр":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не можешь создавать ивенты."
        )
    else:
        return await get_events_by_creator_id(
            token["id"], db_session
        )
    

@event_router.post(
    path="/student_registration",
    status_code=status.HTTP_201_CREATED
)
async def registration_student_to_event(
    event_id: str,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] != "Студент":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не студент, тебе низя регатся."
        )
    if await create_event_registration(
        event_id, token["id"], db_session
    ):
        return {"msg":"Вы успешно зарегистрировались на мероприятий."}
    

@event_router.get(
    path="/get_all/by_student",
    status_code=status.HTTP_200_OK
)
async def get_all_events(
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] != "Студент":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не студент тебе низя."
        )
    else:
        return await get_events_by_user_id(
            token["id"], db_session
        )
    

@event_router.get(
    path="/get_users_registered_in_events",
    status_code=status.HTTP_200_OK
)
async def get_users_registered_in_events(
    event_id: str,
    db_session: AsyncSession = Depends(get_db_session)
):
    users =  await get_users_by_event_id(event_id, db_session)
    return users
    

@event_router.put(
    path="/update",
    status_code=status.HTTP_201_CREATED
)
async def update_event(
    event_id: str,
    event_data: EventSchema,
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
):
    if token["role"] == "Партнёр":
        await update_event_in_db(
            event_id, db_session, token["id"], event_data.start_time,
            event_data.description, event_data.max_participants,
            event_data.status, event_data.type, event_data.image_url
        )
        return {"msg": "Ты успешно обновил событие."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ты не можешь редактировать ивенты"
        )
    