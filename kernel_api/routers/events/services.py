from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import EventSchema
from db import Event, EventRegistration

async def create_event(
    event_data: EventSchema,
    db_session: AsyncSession,
    creator_id: str
) -> Event:
    event = Event(
        description=event_data.description,
        max_participants=event_data.max_participants,
        status=event_data.status,
        type=event_data.type,
        image_url=event_data.image_url,
        creator_id=creator_id
    )
    db_session.add(event)
    await db_session.commit()
    return event


async def get_all(
    db_session: AsyncSession
):
    query = select(Event)
    result = await db_session.execute(query)
    events = result.scalars().all()
    return events


async def get_events_by_creator_id(
    creator_id: str,
    db_session: AsyncSession
):
    query = select(Event).where(Event.creator_id == creator_id)
    result = await db_session.execute(query)
    events = result.scalars().all()
    return events


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
    creator_id: str = None,
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
    if image_url is not None:
        stmt = stmt.values(image_url=image_url)
    await db_session.execute(stmt)
    await db_session.commit()