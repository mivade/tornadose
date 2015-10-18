"""Tests for the EventSource handlers."""

import pytest

from tornado import escape
from tornado.web import Application

from tornadose.handlers import EventSource
from utilities import TestStore

store = TestStore()


@pytest.fixture
def app():
    return Application([
        (r'/', EventSource, dict(store=store))
    ])


def test_get(http_server, http_client, io_loop, base_url):
    def callback(chunk):
        print(chunk)
        assert 'test' in escape.native_str(chunk)
        http_client.close()

    store.submit('test')
    io_loop.call_later(0.01, store.publish)
    http_client.fetch(base_url, streaming_callback=callback)
