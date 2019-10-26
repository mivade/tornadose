import pytest
from tornado import web

from tornadose.handlers import EventSource, WebSocketSubscriber


@pytest.fixture
def app():
    return web.Application()


def test_add_eventsource_handler(app, dummy_store):
    app.add_handlers(".*$", [(r"/stream", EventSource, dict(store=dummy_store))])


def test_add_websocket_subscriber(app, dummy_store):
    app.add_handlers(
        ".*$", [(r"/socket", WebSocketSubscriber, dict(store=dummy_store))]
    )
