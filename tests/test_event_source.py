import pytest

from tornado.ioloop import IOLoop
from tornado import escape
from tornado.web import Application

from tornadose.handlers import EventSource


@pytest.mark.asyncio
class EventSourceTestCase:
    def test_get(self, dummy_store):
        handlers = [r"/", EventSource, {"store": dummy_store}]
        app = Application(handlers)

        def callback(chunk):
            assert "test" in escape.native_str(chunk)

        self.store.submit("test")
        IOLoop.current().call_later(0.01, self.store.publish)
        self.http_client.fetch(self.get_url("/"), streaming_callback=callback)
