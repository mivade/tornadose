"""Tests for the WebSocketSubscriber handlers."""

import json
import pytest

from tornado.web import Application
from tornado.websocket import websocket_connect

from tornadose.handlers import WebSocketSubscriber
import utilities


@pytest.fixture
def store():
    return utilities.TestStore()


@pytest.fixture
def app():
    return Application([
        (r'/', WebSocketSubscriber, dict(store=store))
    ])


@pytest.mark.gen_test
def test_get_message(http_server, io_loop, base_url, store):
    conn = yield websocket_connect('ws' + base_url.split('http')[1])
    store.submit('test')
    io_loop.call_later(0.01, store.publish)
    msg = yield conn.read_message()
    msg = json.loads(msg)
    assert msg['data'] == 'test'
    conn.close()
