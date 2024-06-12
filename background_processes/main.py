import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select

from configs import CONFIG
from db import Event, async_session


async def check_events_status():
    async with async_session() as session:
        async with session.begin():
            current_time = datetime.now()
            result = await session.execute(
                select(Event).where(Event.status != 'Прошедшее')
            )
            events = result.scalars().all()
            for event in events:
                if event.start_time < current_time:
                    event.status = 'Прошедшее'
                    session.add(event)
            await session.commit()


async def main():
    scheduler = AsyncIOScheduler()
    await check_events_status()
    scheduler.start()
    scheduler.add_job(
        check_events_status, 'interval', seconds=CONFIG.WORK_INTERVAL
    )
    while True:        
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        raise e