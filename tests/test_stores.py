from unittest.mock import patch

import pytest

from tornadose.stores import BaseStore, DataStore, QueueStore, RedisStore


@pytest.fixture
def base_store():
    yield BaseStore()


@pytest.fixture
def data_store():
    yield DataStore()


@pytest.fixture
def queue_store():
    yield QueueStore()


@pytest.fixture
def redis_store():
    with patch("tornadose.stores.redis.StrictRedis"):
        yield RedisStore()


@pytest.mark.asyncio
class TestBaseStore:
    async def test_submit(self, base_store):
        with pytest.raises(NotImplementedError):
            base_store.submit("data")

    async def test_publish(self, base_store):
        with pytest.raises(NotImplementedError):
            base_store.publish()


@pytest.mark.asyncio
class TestDataStore:
    async def test_data_property(self, data_store):
        assert data_store.data is None
        data_store.data = "data"
        assert data_store.data == "data"


@pytest.mark.asyncio
class TestQueueStore:
    async def test_submit(self, queue_store):
        queue_store.submit("data")


@pytest.mark.asyncio
class TestRedisStore:
    async def test_submit(self, redis_store):
        with patch.object(redis_store._redis, "publish") as publish:
            redis_store.submit("data", debug=True)
            publish.assert_called_once_with(redis_store.channel, "data")
