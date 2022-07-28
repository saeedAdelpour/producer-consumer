import asyncio
import logging


logger = logging.getLogger(__name__)


class TaskResult:
    fail = "fail"


class ProducerConsumer:
    def __init__(self, items, consumers) -> None:
        self.queue = asyncio.Queue()
        self.items = items
        self.consumers = consumers

    def produce_all(self):
        for item in self.items:
            self.queue.put_nowait(item)

    async def consume(self, result, method, args, kwargs):
        while True:
            # because we sure that queue will be filled completely, we can check queue.empty()
            if len(result) == len(self.items):
                self.cancel_tasks("consume")

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

    def cancel_tasks(self, task_name):
        tasks = asyncio.all_tasks()
        for task in tasks:
            coro = task.get_coro()
            if coro.__name__ == task_name:
                task.cancel()
