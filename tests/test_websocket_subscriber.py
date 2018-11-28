"""Tests for the WebSocketSubscriber handlers."""

import json

import pytest

from tornado.web import Application
from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase

from tornadose.handlers import WebSocketSubscriber


@pytest.mark.asyncio
class WebSocketSubscriberTestCase(AsyncHTTPTestCase):
    async def test_get_message(self, dummy_store):
        app = Application([
            (r'/', WebSocketSubscriber, dict(store=dummy_store))
        ])
        url = self.get_url('/').replace("http://", "ws://")
        conn = yield websocket_connect(url)
        dummy_store.submit('test')
        self.io_loop.call_later(0.01, dummy_store.publish)
        msg = await conn.read_message()
        msg = json.loads(msg)
        assert msg["data"] == "test"
        conn.close()
