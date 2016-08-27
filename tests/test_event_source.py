"""Tests for the EventSource handlers."""

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from tornado import escape
from tornado.web import Application

from tornadose.handlers import EventSource
import utilities


class EventSourceTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.store = utilities.TestStore()
        super(EventSourceTestCase, self).setUp()

    def get_app(self):
        return Application([
            (r'/', EventSource, dict(store=self.store))
        ])

    def test_get(self):
        def callback(chunk):
            print(chunk)
            self.assertIn('test', escape.native_str(chunk))

        self.store.submit('test')
        IOLoop.current().call_later(0.01, self.store.publish)
        self.http_client.fetch(self.get_url("/"), streaming_callback=callback)
