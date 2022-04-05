import logging

from app import db
from app.models import Task
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from .tasks import ExecutableTasks

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
        self.task_pool = []
        self.scheduler.start()

    async def add_task(self, **kwargs):
        self.scheduler.add_job(**kwargs)

    async def execute_task(self, method: str, **kwargs):
        return await getattr(ExecutableTasks, method)(**kwargs)

    async def process_task(self, db_session: AsyncSession, task: Task):
        print(f'Processing task #{task.id}...')
        print(f'Updating task #{task.id} process status"...')
        await task.update_process_status(db_session)
        result = await self.execute_task(task.name, **task.kwargs)
        await task.add_result(db_session, result)
        print(f'Task #{task.id} Result: {task.result}')

    async def get_db_tasks(self) -> None:
        """Get new tasks from db"""

        async with db.Session() as db_session:
            db_tasks = await Task.get_executable_tasks(db_session)
            tasks = db_tasks.scalars().all()

            for task in tasks:
                if task not in self.task_pool:
                    self.task_pool.append(task)
            for i, task in enumerate(self.task_pool):
                await self.process_task(db_session, task)
                del self.task_pool[i]
