"""Tests for stores."""

import pytest

from tornado.web import Application
from tornadose.stores import DataStore, QueueStore
from utilities import TestHandler

data_store = DataStore()
queue_store = QueueStore()


@pytest.fixture
def app():
    return Application([
        (r'/datastore', TestHandler, data_store),
        (r'/queuestore', TestHandler, queue_store)
    ])
