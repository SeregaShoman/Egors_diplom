from datetime import datetime

import jwt
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, HTTPException

from configs import CONFIG
from .schemas import SignUpBody, SignInBody
from dependencies import get_db_session, decode_token
from .services import (
    _create_user, _get_user_by_creds, _get_user_by_id
)


auth_router = APIRouter(
    tags=["Роутер для аутентификационных действий"],
    prefix="/auth",
    default_response_class=ORJSONResponse
)


@auth_router.post(
    path="sign_up", status_code=status.HTTP_201_CREATED
)
async def registration_for_user(
    user_data: SignUpBody,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    new_user = await _create_user(user_data, db_session)
    return {
        "access_token": jwt.encode(
            {"role": user_data.role, "id": str(new_user.id), 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET
        ),
        "refresh_token": jwt.encode(
            {"login":new_user.login, "password":new_user.password, 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET
        )
    }


@auth_router.post(
    path="sign_in", status_code=status.HTTP_200_OK
)
async def user_login(
    user_data: SignInBody,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    user = await _get_user_by_creds(user_data, db_session)
    if user == None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg":"WRONG PASS OR LOGN"}
            )
    return {
        "access_token": jwt.encode(
            {"role": user.role.name, "id": str(user.id), 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET, 
            algorithm="HS256"
        ),
        "refresh_token": jwt.encode(
            {"login":user.login, "password":user.password, 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET,
            algorithm="HS256"
        )
    }


@auth_router.post(
    path="refresh_tokens", status_code=status.HTTP_200_OK
)
async def refresh(
    refresh_token: str,
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    refresh_token = jwt.decode(refresh_token, CONFIG.JWT_SECRET, algorithms=["HS256"])
    user = await _get_user_by_creds(
        SignInBody(login=refresh_token["login"], password=refresh_token["password"]), db_session
    )
    return {
        "access_token": jwt.encode(
            {"role": user.role.name, "id": str(user.id), 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET, 
            algorithm="HS256"
        ),
        "refresh_token": jwt.encode(
            {"login":user.login, "password":user.password, 
            "dt_identifier":str(datetime.now())}, CONFIG.JWT_SECRET, 
            algorithm="HS256"
        )
    }


@auth_router.get(
    path="refresh_tokens", status_code=status.HTTP_200_OK
)
async def get_me(
    token: dict = Depends(decode_token),
    db_session: AsyncSession = Depends(get_db_session)
) -> dict:
    if token.get("id") != None:
        user = await _get_user_by_id(token["id"], db_session)
        return {
            "id": user.id, "fio": user.fio,
            "avatar_url": user.avatar_url,
            "login": user.login,
            "email": user.email,
            "password": user.password,
            "role": user.role.name,
            "groups": user.groups,
            "institution": user.institution,
            "organization": user.organization,
            "position": user.position
        }
    return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg":"INVALID TOKEN"}
            )