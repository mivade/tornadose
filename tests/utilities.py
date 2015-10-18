"""Common utilities for tests."""

from tornado import gen
from tornadose.handlers import BaseHandler
from tornadose.stores import BaseStore


class TestHandler(BaseHandler):
    """Generic subscription handler for testing stores."""
    def submit(self, message):
        self.message = message

    def publish(self):
        assert self.message is not None


class TestStore(BaseStore):
    """Special store for testing handlers."""
    def submit(self, message):
        self.message = message

    @gen.coroutine
    def publish(self):
        for subscriber in self.subscribers:
            yield subscriber.publish(self.message)
