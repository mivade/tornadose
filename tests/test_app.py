"""Basic tests for verifying compliance with ``tornado.web.Application``
instances."""

import pytest
from tornado import web
from tornadose.stores import DataStore, QueueStore
from tornadose.handlers import EventSource, WebSocketSubscriber


@pytest.fixture
def app():
    return web.Application()


def test_add_eventsource_handler(app):
    store = DataStore(1)
    app.add_handlers(".*$", [(r'/stream', EventSource, dict(source=store))])


def test_add_websocket_subscriber(app):
    store = QueueStore()
    app.add_handlers('.*$', [
        (r'/socket', WebSocketSubscriber, dict(store=store))])
