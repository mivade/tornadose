import pytest

from tornadose.handlers import BaseHandler
from tornadose.stores import BaseStore


class DummyStore(BaseStore):
    """Special store for testing handlers."""

    def submit(self, message):
        self.message = message

    async def publish(self):
        for subscriber in self.subscribers:
            await subscriber.publish(self.message)


@pytest.fixture
def dummy_store():
    yield DummyStore()


@pytest.fixture
def handler_class():
    class MyHandler(BaseHandler):
        """Generic subscription handler for testing stores."""

        def submit(self, message):
            self.message = message

        def publish(self):
            assert self.message is not None

    yield MyHandler
