"""Tests for stores."""

import pytest

from tornado.web import Application
from tornadose.stores import BaseStore, DataStore, QueueStore
from tornadose.handlers import BaseHandler


class TestHandler(BaseHandler):
    def submit(self, message):
        self.message = message

    def publish(self):
        assert self.message is not None

data_store = DataStore()
queue_store = QueueStore()


@pytest.fixture
def app():
    return Application([
        (r'/datastore', TestHandler, data_store),
        (r'/queuestore', TestHandler, queue_store)
    ])
