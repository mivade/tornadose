"""Custom request handlers for pushing data to connected clients."""

import logging
from tornado import gen
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.queues import Queue
from tornado.iostream import StreamClosedError
from tornado.log import access_log
from . import stores

logger = logging.getLogger('tornadose.handlers')


class BaseHandler(RequestHandler):
    """Base handler for subscribers."""
    def submit(self, message):
        """Submit a new message to be published. This method must be
        implemented by child classes.

        """
        raise NotImplementedError('submit must be implemented!')

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
    * Browsers generally automatically try to reestablish a lost
      connection.
    * The publish/subscribe pattern is better suited to some applications
      than the full duplex model of websockets.

    __ https://developer.mozilla.org/en-US/docs/Web/API/EventSource
    __ http://curl.haxx.se/
    __ https://github.com/jkbrzt/httpie

    """
    def initialize(self, store, period=None):
        """If ``period`` is given, publishers will sleep for
        approximately the given time in order to throttle data
        speeds.

        """
        assert isinstance(store, stores.BaseStore)
        assert isinstance(period, (int, float)) or period is None
        self.store = store
        self.store.register(self)
        self.period = period
        self.finished = False
        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')

    def prepare(self):
        """Log access."""
        request_time = 1000.0 * self.request.request_time()
        access_log.info(
            "%d %s %.2fms", self.get_status(),
            self._request_summary(), request_time)

    @gen.coroutine
    def submit(self, message):
        """Receive incoming data."""
        logger.debug('Incoming message: ' + message)
        yield self.publish(message)

    @gen.coroutine
    def publish(self, message):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(message))
            yield self.flush()
        except StreamClosedError:
            self.finished = True

    @gen.coroutine
    def get(self, *args, **kwargs):
        try:
            while not self.finished:
                if self.period is not None:
                    yield gen.sleep(self.period)
                else:
                    yield gen.moment
        except Exception:
            pass
        finally:
            self.store.deregister(self)
            self.finish()


class WebSocketSubscriber(BaseHandler, WebSocketHandler):
    """A Websocket-based subscription handler to be used with
    :class:`tornadose.stores.QueueStore`.

    """
    def initialize(self, store):
        self.store = store
        self.messages = Queue()
        self.finished = False

    @gen.coroutine
    def open(self):
        """Register with the publisher."""
        self.store.register(self)
        while not self.finished:
            message = yield self.messages.get()
            yield self.publish(message)

    def on_close(self):
        self._close()

    def _close(self):
        self.store.deregister(self)
        self.finished = True

    @gen.coroutine
    def submit(self, message):
        yield self.messages.put(message)

    @gen.coroutine
    def publish(self, message):
        """Push a new message to the client. The data will be
        available as a JSON object with the key ``data``.

        """
        try:
            self.write_message(dict(data=message))
        except WebSocketClosedError:
            self._close()
