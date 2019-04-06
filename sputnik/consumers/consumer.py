import abc
import asyncio
import typing
from contextlib import suppress

import aio_pika
import uvloop
from aio_pika import Channel


class Consumer:
    def __init__(self, url: str, timeout: float = 3):
        self._loop: asyncio.AbstractEventLoop = None
        self.url = url
        self.connection: aio_pika.Connection = None
        self.queues: typing.List[aio_pika.Queue] = []
        self.timeout: float = timeout
        self.with_ack: bool = False

    async def setup(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    async def run(self, loop: asyncio.AbstractEventLoop):
        await self.connect(loop)
        await self.declare_queues()

        for queue in self.queues:
            await self._consume(queue)

    @abc.abstractmethod
    async def declare_queues(self):
        pass

    @abc.abstractmethod
    async def processing(self, message: aio_pika.IncomingMessage, queue: aio_pika.Queue):
        pass

    async def dispose(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        await self.close()
        self.connection = None
        self.queues = []

    async def connect(self, loop: asyncio.AbstractEventLoop = None):
        self.connection = await aio_pika.connect_robust(
            url=self.url,
            loop=loop if loop else asyncio.get_event_loop()
        )

    def channel(self) -> Channel:
        return self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def declare_processing_queue(self, name: str,
                                       exchange: str,
                                       durable: bool = True,
                                       arguments: dict = None,
                                       routing_key: str = None,
                                       prefetch_count: int = None,
                                       timeout: int = None,
                                       channel: aio_pika.Channel = None,
                                       with_ack: bool = False) -> (aio_pika.Queue, aio_pika.Channel):
        """
        :param with_ack:
        :param name:
        :param exchange:
        :param durable:
        :param arguments:
        :param routing_key:
        :param prefetch_count:
        :param timeout:
        :param channel:
        :return:
        """

        self.timeout = timeout
        self.with_ack = with_ack

        if channel is None:
            channel = await self.channel()

        if prefetch_count is not None:
            await channel.set_qos(
                prefetch_count=prefetch_count
            )

        queue = await channel.declare_queue(
            name=name,
            durable=durable,
            arguments=arguments,
            timeout=timeout,
        )

        await queue.bind(
            exchange=exchange,
            routing_key=routing_key or '',
            timeout=timeout
        )

        self.queues.append(queue)
        return queue, channel

    async def _consume(self, queue: aio_pika.Queue) -> asyncio.Task:
        async def _queue_handler(message: aio_pika.IncomingMessage):
            await asyncio.wait_for(self.processing(message, queue), timeout=self.timeout)

            if self.with_ack is True:
                await message.ack()

        return queue.loop.create_task(
            queue.consume(_queue_handler, no_ack=not self.with_ack),
        )


def run(consumers: typing.List[Consumer]):
    async def _cancel_tasks():
        tasks = asyncio.Task.all_tasks()
        for task in tasks:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    _ = [loop.run_until_complete(consumer.setup(loop)) for consumer in consumers]

    try:
        _ = [loop.run_until_complete(consumer.run(loop)) for consumer in consumers]
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(_cancel_tasks())
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        _ = [loop.run_until_complete(consumer.dispose(loop)) for consumer in consumers]
        loop.run_until_complete(asyncio.sleep(0.05))

    loop.close()
