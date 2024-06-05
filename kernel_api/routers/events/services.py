from uuid import UUID

from sqlalchemy import update
from sqlalchemy.sql import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import EventSchema
from db import Event, EventRegistration, User

async def create_event(
    event_data: EventSchema,
    db_session: AsyncSession,
    creator_id: str
) -> Event:
    event = Event(
        description=event_data.description,
        max_participants=event_data.max_participants,
        status=event_data.status,
        name=event_data.name,
        type=event_data.type,
        start_time=event_data.start_time,
        image_url=event_data.image_url,
        creator_id=creator_id
    )
    db_session.add(event)
    await db_session.commit()
    return event


async def get_all(db_session: AsyncSession):
    query = (
        select(
            Event,
            func.count(EventRegistration.id).label('registrations_count'),
            func.array_agg(EventRegistration.user_id).label('user_ids')
        )
        .outerjoin(EventRegistration, Event.id == EventRegistration.event_id)
        .group_by(Event.id)
    )
    result = await db_session.execute(query)
    events = result.all()

    return [
        {
            'event': event,
            'registrations_count': registrations_count,
            'user_ids': user_ids
        }
        for event, registrations_count, user_ids in events
    ]


async def get_events_by_creator_id(creator_id: UUID, db_session: AsyncSession):
    query = (
        select(
            Event,
            func.count(EventRegistration.id).label('registrations_count'),
            func.array_agg(EventRegistration.user_id).label('user_ids')
        )
        .outerjoin(EventRegistration, Event.id == EventRegistration.event_id)
        .where(Event.creator_id == creator_id)
        .group_by(Event.id)
    )
    result = await db_session.execute(query)
    events = result.all()

    return [
        {
            'event': event,
            'registrations_count': registrations_count,
            'user_ids': user_ids
        }
        for event, registrations_count, user_ids in events
    ]


async def create_event_registration(
    event_id: str, user_id: str, db_session: AsyncSession
):
    registration = EventRegistration(event_id=event_id, user_id=user_id)
    db_session.add(registration)
    await db_session.commit()
    await db_session.refresh(registration)
    return registration


async def get_events_by_user_id(
    user_id: str,
    db_session: AsyncSession
):
    query = (
        select(Event)
        .join(Event.registrations)
        .filter(EventRegistration.user_id == user_id)
    )
    result = await db_session.execute(query)
    events = result.scalars().all()
    return events


async def update_event_in_db(
    event_id: str, db_session: AsyncSession, 
    creator_id: str = None, start_time: str = None,
    description: str = None, max_participants: int = None,
    status: str = None, type: str = None, image_url: str = None,
):
    stmt = update(Event).where(Event.id == event_id)
    if creator_id:
        stmt = stmt.where(Event.creator_id == creator_id)
    if description is not None:
        stmt = stmt.values(description=description)
    if max_participants is not None:
        stmt = stmt.values(max_participants=max_participants)
    if status is not None:
        stmt = stmt.values(status=status)
    if type is not None:
        stmt = stmt.values(type=type)
    if start_time is not None:
        stmt = stmt.values(start_time=start_time)
    if image_url is not None:
        stmt = stmt.values(image_url=image_url)
    await db_session.execute(stmt)
    await db_session.commit()


async def get_users_by_event_id(event_id: UUID, db_session: AsyncSession):
    query = (
        select(User)
        .join(EventRegistration, User.id == EventRegistration.user_id)
        .where(EventRegistration.event_id == event_id)
        .options(selectinload(User.role))
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
            'groups': user.groups,
            'institution': user.institution,
            'organization': user.organization,
            'position': user.position
        }
        for user in users
    ]