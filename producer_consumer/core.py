from typing import List
import asyncio
import logging

from .exceptions import AllTasksFailedException


logger = logging.getLogger(__name__)


class TaskResult:
    fail = "fail"


class ProducerConsumer:
    def __init__(self, items, consumers):
        self.queue = asyncio.Queue()
        self.items = items
        self.consumers = consumers
        self.tasks = []

    async def produce_all(self):
        for item in self.items:
            await self.queue.put(item)

    async def perform(self, consumer_method_name, args=tuple(), kwargs=dict()):
        result = []

        try:
            await self.perform_consume(result, consumer_method_name, args, kwargs)
        except asyncio.exceptions.CancelledError:
            pass

        return result

    async def perform_consume(self, result, consumer_method_name, args, kwargs):
        produce_task = asyncio.create_task(self.produce_all())
        self.tasks = [
            asyncio.create_task(
                self.consume(
                    result, getattr(consumer, consumer_method_name), args, kwargs
                )
            )
            for consumer in self.consumers
        ]

        task_results = await asyncio.gather(*self.tasks)
        self.check_all_task_results(task_results)
        await produce_task
        await self.queue.join()

    async def consume(self, result, method, args, kwargs):
        while True:
            if len(result) == len(self.items):
                self.cancel_tasks()

            item = await self.queue.get()
            try:
                item_result = await method(item, *args, **kwargs)
                result.append(item_result)
                self.queue.task_done()
            except Exception:
                logger.exception("error")
                await self.queue.put(item)
                self.queue.task_done()
                return TaskResult.fail

    def cancel_tasks(self):
        for task in self.tasks:
            task.cancel()

    def check_all_task_results(self, task_results):
        """check all tasks are completed or failed, if all tasks failed, raise Exception"""
        failed_tasks = [t for t in task_results if t is TaskResult.fail]
        if len(failed_tasks) == len(task_results):
            raise AllTasksFailedException("all tasks failed")
