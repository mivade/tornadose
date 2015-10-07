"""Tests for the EventSource handlers."""

import pytest

from tornado import gen
from tornado.web import Application
from tornado.httpclient import HTTPRequest

from tornadose.handlers import EventSource
from tornadose.stores import BaseStore


class TestStore(BaseStore):
    """Special store for testing handlers."""
    def submit(self, message):
        self.message = message

    @gen.coroutine
    def publish(self):
        yield gen.sleep(1)
        for subscriber in self.subscribers:
            yield subscriber.publish(self.message)

store = TestStore()
application = Application([
    (r'/', EventSource, dict(store=store))
])
req = HTTPRequest('http://localhost')


@pytest.fixture
def app():
    return application


@pytest.mark.gen_test
def test_get(http_client):
    store.submit('test')
    yield [store.publish(), http_client.fetch('http://localhost:5555/')]
