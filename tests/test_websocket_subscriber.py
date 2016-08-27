"""Tests for the WebSocketSubscriber handlers."""

import json

from tornado.web import Application
from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase, gen_test

from tornadose.handlers import WebSocketSubscriber
import utilities


class WebSocketSubscriberTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.store = utilities.TestStore()
        super(WebSocketSubscriberTestCase, self).setUp()

    def get_app(self):
        return Application([
            (r'/', WebSocketSubscriber, dict(store=self.store))
        ])

    @gen_test
    def test_get_message(self):
        url = self.get_url('/').replace("http://", "ws://")
        conn = yield websocket_connect(url)
        self.store.submit('test')
        self.io_loop.call_later(0.01, self.store.publish)
        msg = yield conn.read_message()
        msg = json.loads(msg)
        self.assertEqual(msg['data'], 'test')
        conn.close()
