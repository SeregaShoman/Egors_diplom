from uuid import UUID
from typing import Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db import EventRegistration, User, Student, Partner
from .schemas import UserUpdateSchema, StudentUpdateSchema, PartnerUpdateSchema


async def get_users_by_event_id(event_id: UUID, db_session: AsyncSession):
    query = (
        select(User)
        .join(EventRegistration, User.id == EventRegistration.user_id)
        .where(EventRegistration.event_id == event_id)
        .options(selectinload(User.role), selectinload(User.student_info))
    )
    result = await db_session.execute(query)
    users = result.scalars().all()

    return [
        {
            'id': str(user.id),
            'fio': user.fio,
            'avatar_url': user.avatar_url,
            'login': user.login,
            'email': user.email,
            'role': user.role.name if user.role else None,
            'groups': user.student_info.groups if user.student_info else None,
            'institution': user.student_info.institution if user.student_info else None
        }
        for user in users
    ]


async def get_user_by_id(
    user_id: str,
    db_session: AsyncSession
) -> User:
    query = (
        select(User)
        .options(selectinload(User.role), selectinload(User.student_info), selectinload(User.partner_info))
        .where(User.id == user_id)
    )
    result = await db_session.execute(query)
    user = result.scalars().first()
    return user


async def update_user_in_db(
    user_id: UUID, db_session: AsyncSession,
    user_info: Optional[UserUpdateSchema] = None,
    student_info: Optional[StudentUpdateSchema] = None,
    partner_info: Optional[PartnerUpdateSchema] = None
):
    stmt = update(User).where(User.id == user_id)
    if user_info.fio is not None:
        stmt = stmt.values(fio=user_info.fio)
    if user_info.avatar_url is not None:
        stmt = stmt.values(avatar_url=user_info.avatar_url)
    if user_info.login is not None:
        stmt = stmt.values(login=user_info.login)
    if user_info.email is not None:
        stmt = stmt.values(email=user_info.email)
    if user_info.password is not None:
        stmt = stmt.values(password=user_info.password)
    await db_session.execute(stmt)
    if student_info is not None:
        stmt = update(Student).where(Student.user_id == user_id)
        if student_info.groups is not None:
            stmt = stmt.values(groups=student_info.groups)
        if student_info.institution is not None:
            stmt = stmt.values(institution=student_info.institution)
        await db_session.execute(stmt)
    if partner_info is not None:
        stmt = update(Partner).where(Partner.user_id == user_id)
    if partner_info.organization is not None:
        stmt = stmt.values(organization=partner_info.organization)
    if partner_info.position is not None:
        stmt = stmt.values(position=partner_info.position)
    await db_session.execute(stmt)
    await db_session.commit()
