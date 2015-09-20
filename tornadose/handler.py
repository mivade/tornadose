from tornado import gen
from tornado.web import RequestHandler, HTTPError
from tornado.iostream import StreamClosedError
from tornado.log import access_log
from . import stores


class EventSource(RequestHandler):
    """Base handler for server-sent events a.k.a. EventSource."""
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
        self.period = 0.01 or period
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
    def publish(self, data):
        """Pushes data to a listener."""
        try:
            self.write('data: {}\n\n'.format(data))
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
                yield gen.sleep(self.period)
        self.finish()
