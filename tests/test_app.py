"""Basic tests for verifying compliance with ``tornado.web.Application``
instances."""

import pytest
from tornado import web

from tornadose.handlers import EventSource, WebSocketSubscriber
import utilities


@pytest.fixture
def app():
    return web.Application()


def test_add_eventsource_handler(app):
    store = utilities.TestStore()
    app.add_handlers(".*$", [(r'/stream', EventSource, dict(store=store))])


def test_add_websocket_subscriber(app):
    store = utilities.TestStore()
    app.add_handlers('.*$', [
        (r'/socket', WebSocketSubscriber, dict(store=store))])
