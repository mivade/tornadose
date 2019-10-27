import pytest

from tornado import escape
from tornado.web import Application

from tornadose.handlers import EventSource


@pytest.fixture()
def app(dummy_store) -> Application:
    handlers = [(r"/", EventSource, {"store": dummy_store})]
    app = Application(handlers)
    return app


@pytest.mark.gen_test
class TestEventSource:
    def test_get(self, io_loop, http_client, base_url, dummy_store):

        def callback(chunk):
            assert "test" in escape.native_str(chunk)

        dummy_store.submit("test")
        io_loop.add_callback(dummy_store.publish)
        http_client.fetch(base_url, streaming_callback=callback)
