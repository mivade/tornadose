"""Data storage for dynamic updates to clients."""

from uuid import uuid4
from tornado import gen
from tornado.web import RequestHandler
from tornado.queues import Queue


class DataStore(object):
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
    def __init__(self, initial_data=None):
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


class StoreContainer(object):
    """A convenience class for containing multiple data stores."""
    def __init__(self, stores=None):
        """Create the container with a list of stores."""
        assert isinstance(stores, (list, tuple)) or stores is None
        if stores is not None:
            assert [isinstance(store, DataStore) for store in stores]
            self._stores = stores
        else:
            self._stores = []

    def __len__(self):
        return len(self._stores)

    def __getitem__(self, i):
        return self._stores[i]

    def add(self, store):
        """Add a store to the container."""
        assert isinstance(store, DataStore)
        self._stores.append(store)

    def add_stores(self, stores):
        """Add several stores to the container at once."""
        assert isinstance(stores, (list, tuple))
        [self.add(store) for store in stores]


class Publisher(object):
    """Publish data via queues.

    This class is meant to be used in cases where subscribers should not
    miss any data. Compared to the :class:`DataStore` class, new
    messages to be broadcast to clients are put in a queue to be
    processed in order.

    :class:`Publisher` will work with any
    :class:`tornado.web.RequestHandler` subclasses which implement a
    ``submit`` method. It is recommended that a custom subscription
    handler's :meth:`submit` method also utilize a queue to avoid losing
    data. The subscriber must also register/deregister itself with the
    :class:`Publisher` via the :meth:`Publisher.register` and
    :meth:`Publisher.deregister` methods.

    A :class:`Publisher`-compatible request handler is included in
    :class:`tornadose.handlers.WebSocketSubscriber`.

    """
    def __init__(self):
        self.messages = Queue()
        self.subscribers = set()

    def register(self, subscriber):
        """Register a new subscriber."""
        assert isinstance(subscriber, RequestHandler)
        self.subscribers.add(subscriber)

    def deregister(self, subscriber):
        """Stop publishing to a subscriber."""
        self.subscribers.remove(subscriber)

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
