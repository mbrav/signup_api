import logging

from app import db, models
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..tasks import ExecutableTasks

logger = logging.getLogger()


def test_task(name: str = 'TEST'):
    result = f'EXECUTING {name} TASK'
    logger.debug(result)
    print(result)
    return result


class SchedulerService:
    """Scheduler service"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.db_session = db.Session()
        self.task_pool = []

    async def start(self):
        self.scheduler.start()
        self.scheduler.add_job(
            self.get_db_tasks,
            'interval', seconds=5, max_instances=2)

    async def execution_task(self, method: str, **kwargs):
        return await getattr(ExecutableTasks, method)(**kwargs)

    async def process_task(self, task: models.Task):
        print(f'Processing task #{task.id}...')
        print(f'Updating task #{task.id} process status"...')
        await task.update_process_status(self.db_session)
        result = await self.execution_task(task.name, **task.kwargs)
        await task.add_result(self.db_session, result)
        print(f'Task #{task.id} Result: {task.result}')

    async def get_db_tasks(self) -> None:
        try:
            db_tasks = await models.Task.get_executable_tasks(self.db_session)
            for task in db_tasks.scalars().all():
                if task not in self.task_pool:
                    self.task_pool.append(task)
            for i, task in enumerate(self.task_pool):
                await self.process_task(task)
                del self.task_pool[i]

        except Exception as ex:
            print(ex)


scheduler = SchedulerService()


# Service startup
async def start_scheduler():
    logger.info('Scheduler service startup BEGIN')
    await scheduler.start()
    logger.info('Scheduler service startup DONE')


# Dependency
async def get_scheduler() -> SchedulerService:
    yield scheduler
