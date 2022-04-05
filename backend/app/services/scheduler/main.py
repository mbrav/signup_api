import logging

from app.config import settings

from .google_cal import CalendarService
from .scheduler import SchedulerService

logger = logging.getLogger()

scheduler_service = SchedulerService()
calendar_service = CalendarService(
    api_key=settings.CAL_API_KEY,
    cal_id=settings.CAL_ID)


# Service startup
async def start_scheduler():
    logger.info('Scheduler service startup BEGIN')
    await scheduler_service.add_task(
        func=scheduler_service.get_db_tasks,
        trigger='interval', seconds=5, max_instances=2)
    logger.info('Scheduler service startup DONE')


# Service startup
async def start_calendar():
    logger.info('Google Calendar service startup BEGIN')
    # await scheduler_service.add_task(
    #     func=calendar_service.update_events,
    #     trigger='interval', seconds=300, max_instances=1)

    await calendar_service.update_events()
    logger.info('Google Calendar service startup DONE')


# Dependency
async def get_scheduler() -> SchedulerService:
    yield scheduler_service


# Dependency
async def get_calendar() -> CalendarService:
    yield calendar_service
