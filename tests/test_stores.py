"""Tests for stores."""

import pytest

from tornado.web import Application
from tornadose.stores import BaseStore, DataStore, QueueStore, RedisStore
from utilities import TestHandler


class BaseTest(object):
    @pytest.fixture
    def store(self):
        return None

    @pytest.fixture
    def app(self):
        return Application([
            (r'/store', TestHandler, self.store)
        ])

    def test_submit(self, store):
        store.submit('data')


class TestBaseStore(BaseTest):
    @pytest.fixture
    def store(self):
        return BaseStore()

    def test_submit(self, store):
        with pytest.raises(NotImplementedError):
            super(TestBaseStore, self).test_submit(store)


class TestDataStore(BaseTest):
    @pytest.fixture
    def store(self):
        return DataStore()

    def test_data_property(self, store):
        assert store.data is None
        store.data = 'data'
        assert store.data == 'data'


class TestQueueStore(BaseTest):
    @pytest.fixture
    def store(self):
        return QueueStore()


class TestRedisStore(BaseTest):
    @pytest.fixture
    def store(self):
        return RedisStore(channel='tornadose-test')

    def test_submit(self, store):
        store.submit('data', debug=True)
