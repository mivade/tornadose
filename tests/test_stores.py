"""Tests for stores."""

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import pytest

from tornado.web import Application
from tornadose.stores import DataStore


@pytest.fixture
def store():
    return DataStore()


def test_submit(store):
    store.submit('test')
    assert store.data == 'test'


@pytest.mark.gen_test
def test_publish(store):
    pass
