import logging

from app import db
from app.models import Task
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
        self.db_session = db.Session()
        self.task_pool = []
        self.scheduler.start()

    async def add_task(self, **kwargs):
        self.scheduler.add_job(**kwargs)

    async def execute_task(self, method: str, **kwargs):
        return await getattr(ExecutableTasks, method)(**kwargs)

    async def process_task(self, task: Task):
        print(f'Processing task #{task.id}...')
        print(f'Updating task #{task.id} process status"...')
        await task.update_process_status(self.db_session)
        result = await self.execute_task(task.name, **task.kwargs)
        await task.add_result(self.db_session, result)
        print(f'Task #{task.id} Result: {task.result}')

    async def get_db_tasks(self) -> None:
        try:
            db_tasks = await Task.get_executable_tasks(self.db_session)
            for task in db_tasks.scalars().all():
                if task not in self.task_pool:
                    self.task_pool.append(task)
            for i, task in enumerate(self.task_pool):
                await self.process_task(task)
                del self.task_pool[i]

        except Exception as ex:
            print(ex)
