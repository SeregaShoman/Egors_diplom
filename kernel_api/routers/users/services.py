from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from db import EventRegistration, User


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