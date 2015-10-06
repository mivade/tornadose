"""Data storage for dynamic updates to clients."""

from uuid import uuid4
from tornado import gen
from tornado.web import RequestHandler
from tornado.queues import Queue
from tornado.log import app_log


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
        self.subscribers.add(subscriber)

    def deregister(self, subscriber):
        """Stop publishing to a subscriber."""
        try:
            self.subscribers.remove(subscriber)
        except KeyError:
            app_log.debug(
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

    When data is updated, a unique id is generated. This is in order
    to enable the publisher to update any new data, even if the value
    is the same as the previous data.

    """
    def initialize(self, initial_data=None):
        self.last_id = None
        self.set_data(initial_data)

    def set_data(self, new_data):
        """Update the store with new data."""
        self._data = new_data
        self.id = uuid4()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self.set_data(new_data)

    def submit(self, message):
        self.data = message

    @gen.coroutine
    def publish(self):
        while True:
            if self.id is not self.last_id:
                yield [subscriber.submit(self.data) for subscriber in self.subscribers]
            else:
                yield gen.moment


class QueueStore(BaseStore):
    """Publish data via queues.

    This class is meant to be used in cases where subscribers should not
    miss any data. Compared to the :class:`DataStore` class, new
    messages to be broadcast to clients are put in a queue to be
    processed in order.

    :class:`QueueStore` will work with any
    :class:`tornado.web.RequestHandler` subclasses which implement a
    ``submit`` method. It is recommended that a custom subscription
    handler's :meth:`submit` method also utilize a queue to avoid
    losing data. The subscriber must also register/deregister itself
    with the :class:`QueueStore` via the :meth:`QueueStore.register`
    and :meth:`QueueStore.deregister` methods.

    A :class:`QueueStore`-compatible request handler is included in
    :class:`tornadose.handlers.WebSocketSubscriber`.

    """
    def initialize(self):
        self.messages = Queue()

    @gen.coroutine
    def submit(self, message):
        """Submit a new message to publish to subscribers."""
        yield self.messages.put(message)

    @gen.coroutine
    def publish(self):
        while True:
            message = yield self.messages.get()
            if len(self.subscribers) > 0:
                print("Pushing message {} to {} subscribers...".format(
                    message, len(self.subscribers)))
                yield [subscriber.submit(message) for subscriber in self.subscribers]
