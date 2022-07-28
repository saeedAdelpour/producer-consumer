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
