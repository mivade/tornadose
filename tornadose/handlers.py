"""Custom request handlers for pushing data to connected clients."""

from tornado import gen
from tornado.web import RequestHandler, HTTPError
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.queues import Queue
from tornado.iostream import StreamClosedError
from tornado.log import access_log
from . import stores


class EventSource(RequestHandler):
    """Base handler for server-sent events a.k.a. EventSource.

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
    def initialize(self, source, period=None):
        """The ``source`` parameter is a string that is updated with
        new data. The :class:`EventSource` instance will continuously
        check if it is updated and publish to clients when it is.

        If ``period`` is given, publishers will sleep for approximately the
        given time in order to throttle data speeds.

        """
        assert isinstance(source, (stores.DataStore, stores.StoreContainer))
        assert isinstance(period, (int, float)) or period is None
        self.source = source
        self.period = period
        self._last = None
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
    def publish(self, message):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(message))
            yield self.flush()
        except StreamClosedError:
            self.finished = True

    @gen.coroutine
    def get(self, *args, **kwargs):
        if type(self.source) is stores.StoreContainer:
            index = int(args[0])
            if index >= len(self.source):
                raise HTTPError(405, 'StoreContainer index out of range')
            self.source = self.source[index]

        while not self.finished:
            if self.source.id != self._last and self.source.data is not None:
                yield self.publish(self.source.data)
                self._last = self.source.id
            else:
                if self.period is not None:
                    yield gen.sleep(self.period)
        self.finish()


class WebSocketSubscriber(WebSocketHandler):
    """A Websocket-based subscription handler to be used with
    :class:`tornadose.stores.Publisher`.

    """
    def initialize(self, publisher):
        self.publisher = publisher
        self.messages = Queue()
        self.finished = False

    def open(self):
        """Register with the publisher."""
        self.publisher.register(self)
        self.run()

    def on_close(self):
        self._close()

    def _close(self):
        self.publisher.deregister(self)
        self.finished = True

    @gen.coroutine
    def submit(self, message):
        yield self.messages.put(message)

    @gen.coroutine
    def run(self):
        """Coroutine for publishing messages as they become
        available.

        """
        while not self.finished:
            message = yield self.messages.get()
            self.publish(message)

    def publish(self, message):
        """Push a new message to the client. The data will be
        available as a JSON object with the key ``data``.

        """
        try:
            self.write_message(dict(data=message))
        except WebSocketClosedError:
            self._close()
