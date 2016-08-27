"""Tests for stores."""

import unittest
from tornado.testing import AsyncTestCase
from tornadose.stores import BaseStore, DataStore, QueueStore, RedisStore


class BaseStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.store = BaseStore()

    def test_submit(self):
        with self.assertRaises(NotImplementedError):
            self.store.submit("data")

    def test_publish(self):
        with self.assertRaises(NotImplementedError):
            self.store.publish()


class TestDataStore(AsyncTestCase):
    def setUp(self):
        self.store = DataStore()
        super(TestDataStore, self).setUp()

    def test_data_property(self):
        self.assertIsNone(self.store.data)
        self.store.data = 'data'
        self.assertEqual(self.store.data, 'data')


class TestQueueStore(AsyncTestCase):
    def setUp(self):
        self.store = QueueStore()
        super(TestQueueStore, self).setUp()

    def test_submit(self):
        self.store.submit("data")


class TestRedisStore(AsyncTestCase):
    def setUp(self):
        self.store = RedisStore(channel='tornadose-test')
        super(TestRedisStore, self).setUp()

    def test_submit(self):
        self.store.submit('data', debug=True)
