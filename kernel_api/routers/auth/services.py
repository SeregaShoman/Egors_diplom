from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from db import User, Student, Partner
from .schemas import SignUpBody, SignInBody

async def _create_user(
    user_data: SignUpBody,
    db_session: AsyncSession
) -> User:
    if user_data.role == "Студент":
        role_id = 1
    elif user_data.role == "Партнёр":
        role_id = 2
    elif user_data.role == "Админ":
        role_id = 3

    new_user = User(
        fio=user_data.fio,
        avatar_url=user_data.avatar_url,
        login=user_data.login,
        email=user_data.email,
        password=user_data.password,
        role_id=role_id
    )

    db_session.add(new_user)
    await db_session.flush()  # Ensure the user is added and we have an ID for relationships

    if user_data.role == "Студент":
        student_info = Student(
            user_id=new_user.id,
            groups=user_data.group,
            institution=user_data.institution
        )
        db_session.add(student_info)
    elif user_data.role == "Партнёр":
        partner_info = Partner(
            user_id=new_user.id,
            organization=user_data.organization,
            position=user_data.position
        )
        db_session.add(partner_info)

    await db_session.commit()
    return new_user


async def _get_user_by_creds(
    user_data: SignInBody,
    db_session: AsyncSession
) -> User:
    query = (
        select(User)
        .options(selectinload(User.role))
        .where(User.login == user_data.login, User.password == user_data.password)
    )
    result = await db_session.execute(query)
    user = result.scalars().first()
    return user


async def _get_user_by_id(
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
