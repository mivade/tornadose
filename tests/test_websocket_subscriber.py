"""Tests for the WebSocketSubscriber handlers."""

import json

import pytest

from tornado.web import Application
from tornado.websocket import websocket_connect

from tornadose.handlers import WebSocketSubscriber


@pytest.fixture
def app(dummy_store) -> Application:
    app = Application([(r"/", WebSocketSubscriber, dict(store=dummy_store))])
    return app


class TestWebSocketSubscriber:
    @pytest.mark.gen_test
    async def test_get_message(self, http_server, io_loop, base_url, dummy_store):
        url = base_url.replace("http://", "ws://")
        conn = await websocket_connect(url, connect_timeout=1)
        dummy_store.submit("test")
        io_loop.add_callback(dummy_store.publish)
        msg = await conn.read_message()
        msg = json.loads(msg)
        assert msg["data"] == "test"
        conn.close()
