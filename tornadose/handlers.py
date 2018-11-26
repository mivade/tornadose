"""Custom request handlers for pushing data to connected clients."""

from asyncio import Queue
import logging

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.iostream import StreamClosedError
from tornado.log import access_log

from . import stores

logger = logging.getLogger('tornadose.handlers')


class BaseHandler(RequestHandler):
    """Base handler for subscribers. To be compatible with data stores
    defined in :mod:`tornadose.stores`, custom handlers should inherit
    this class and implement the :meth:`publish` method.

    """
    def initialize(self, store):
        """Common initialization of handlers happens here. If additional
        initialization is required, this method must either be called with
        ``super`` or the child class must assign the ``store`` attribute and
        register itself with the store.

        """
        assert isinstance(store, stores.BaseStore)
        self.messages = Queue()
        self.store = store
        self.store.register(self)

    async def submit(self, message):
        """Submit a new message to be published."""
        await self.messages.put(message)

    def publish(self):
        """Push a message to the subscriber. This method must be
        implemented by child classes.

        """
        raise NotImplementedError('publish must be implemented!')


class EventSource(BaseHandler):
    """Handler for server-sent events a.k.a. EventSource.

    The EventSource__ interface has a few advantages over websockets:

    * It is a normal HTTP connection and so can be more easily monitored
      than websockets using tools like curl__ or HTTPie__.
    * Browsers generally try to reestablish a lost connection
      automatically.
    * The publish/subscribe pattern is better suited to some applications
      than the full duplex model of websockets.

    __ https://developer.mozilla.org/en-US/docs/Web/API/EventSource
    __ http://curl.haxx.se/
    __ https://github.com/jkbrzt/httpie

    """
    def initialize(self, store):
        super(EventSource, self).initialize(store)
        self.finished = False
        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    def prepare(self):
        """Log access."""
        request_time = 1000.0 * self.request.request_time()
        access_log.info(
            "%d %s %.2fms", self.get_status(),
            self._request_summary(), request_time)

    async def publish(self, message):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(message))
            await self.flush()
        except StreamClosedError:
            self.finished = True

    async def get(self, *args, **kwargs):
        try:
            while not self.finished:
                message = await self.messages.get()
                await self.publish(message)
        except Exception:
            pass
        finally:
            self.store.deregister(self)
            self.finish()


class WebSocketSubscriber(BaseHandler, WebSocketHandler):
    """A Websocket-based subscription handler."""
    def initialize(self, store):
        super(WebSocketSubscriber, self).initialize(store)
        self.finished = False

    async def open(self):
        """Register with the publisher."""
        self.store.register(self)
        while not self.finished:
            message = await self.messages.get()
            await self.publish(message)

    def on_close(self):
        self._close()

    def _close(self):
        self.store.deregister(self)
        self.finished = True

    async def publish(self, message):
        """Push a new message to the client. The data will be
        available as a JSON object with the key ``data``.

        """
        try:
            self.write_message(dict(data=message))
        except WebSocketClosedError:
            self._close()
