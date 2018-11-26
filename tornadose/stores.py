"""Data storage for dynamic updates to clients."""

from asyncio import Event, Queue
import logging
from concurrent.futures import ThreadPoolExecutor

from tornado.concurrent import run_on_executor
from tornado.web import RequestHandler

try:
    import redis
except ImportError:
    redis = None

logger = logging.getLogger('tornadose.stores')


class BaseStore(object):
    """Base class for all data store types.

    At a minimum, derived classes should implement ``submit`` and
    ``publish`` methods.

    """
    def __init__(self, *args, **kwargs):
        self.subscribers = set()
        self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        """Hook for doing custom initialization. Child classes should
        implement this method instead of overwriting ``__init__``.

        """

    def register(self, subscriber):
        """Register a new subscriber. This method should be invoked by
        listeners to start receiving messages.

        """
        assert isinstance(subscriber, RequestHandler)
        logger.debug('New subscriber')
        self.subscribers.add(subscriber)

    def deregister(self, subscriber):
        """Stop publishing to a subscriber."""
        try:
            logger.debug('Subscriber left')
            self.subscribers.remove(subscriber)
        except KeyError:
            logger.debug(
                'Error removing subscriber: ' +
                str(subscriber))

    def submit(self, message):
        """Add a new message to be pushed to subscribers. This method
        must be implemented by child classes.

        This method exists to store new data. To actually publish the
        data, implement the ``publish`` method.

        """
        raise NotImplementedError('submit must be implemented!')

    def publish(self):
        """Push messages to all listeners. This method must be
        implemented by child classes. A recommended way to implement
        this method is as a looping coroutine which yields until new
        data is available via the :meth:`submit` method.

        """
        raise NotImplementedError('publish must be implemented!')


class DataStore(BaseStore):
    """Generic object for producing data to feed to clients.

    To use this, simply instantiate and update the ``data`` property
    whenever new data is available. When creating a new
    :class:`EventSource` handler, specify the :class:`DataStore`
    instance so that the :class:`EventSource` can listen for
    updates.

    """
    def initialize(self, initial_data=None):
        self.set_data(initial_data)
        self.publish()

    def set_data(self, new_data):
        """Update the store with new data."""
        self._data = new_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self.set_data(new_data)

    def submit(self, message):
        self.data = str(message)

    async def publish(self):
        while True:
            await [subscriber.submit(self.data) for subscriber in self.subscribers]


class RedisStore(BaseStore):
    """Publish data via a Redis backend.

    This data store works in a similar manner as
    :class:`DataStore`. The primary advantage is that external
    programs can be used to publish data to be consumed by clients.

    The ``channel`` keyword argument specifies which Redis channel to
    publish to and defaults to ``tornadose``.

    All remaining keyword arguments are passed directly to the
    ``redis.StrictRedis`` constructor. See `redis-py`__'s
    documentation for detais.

    New messages are read in a background thread via a
    :class:`concurrent.futures.ThreadPoolExecutor`.

    __ https://redis-py.readthedocs.org/en/latest/

    :raises ConnectionError: when the Redis host is not pingable

    """
    def initialize(self, channel='tornadose', **kwargs):
        if redis is None:
            raise RuntimeError("The redis module is required to use RedisStore")

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.channel = channel
        self.messages = Queue()
        self._done = Event()

        self._redis = redis.StrictRedis(**kwargs)
        self._redis.ping()
        self._pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        self._pubsub.subscribe(self.channel)

        self.publish()

    def submit(self, message, debug=False):
        self._redis.publish(self.channel, message)
        if debug:
            logger.debug(message)
            self._redis.setex(self.channel, 5, message)

    def shutdown(self):
        """Stop the publishing loop."""
        self._done.set()
        self.executor.shutdown(wait=False)

    @run_on_executor
    def _get_message(self):
        data = self._pubsub.get_message(timeout=1)
        if data is not None:
            data = data['data']
        return data

    async def publish(self):
        while not self._done.is_set():
            data = await self._get_message()
            if len(self.subscribers) > 0 and data is not None:
                [subscriber.submit(data) for subscriber in self.subscribers]


class QueueStore(BaseStore):
    """Publish data via queues.

    This class is meant to be used in cases where subscribers should
    not miss any data. Compared to the :class:`DataStore` class, new
    messages to be broadcast to clients are put in a queue to be
    processed in order.

    """
    def initialize(self):
        self.messages = Queue()
        self.publish()

    async def submit(self, message):
        await self.messages.put(message)

    async def publish(self):
        while True:
            message = await self.messages.get()
            if len(self.subscribers) > 0:
                await [subscriber.submit(message) for subscriber in self.subscribers]
