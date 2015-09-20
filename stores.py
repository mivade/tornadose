"""Data storage for dynamic updates to clients."""

try:
    import simplejson as json
except ImportError:
    import json


class DataStore(object):
    """Generic object for producing data to feed to clients.

    Notes
    -----
    To use this, simply instantiate and update the ``data`` property
    whenever new data is available. When creating a new
    :class:`views.EventSource` handler, specify the :class:`DataStore`
    instance so that the :class:`views.EventSource` can listen for
    updates.

    """
    def __init__(self, initial_data=None):
        self._data = initial_data

    def set_data(self, new_data):
        """Convenience function so multiple stores can be updated with list
        comprehension.

        """
        self.data = new_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data


class StoreContainer(object):
    """Class for holding multiple stores."""
    def __init__(self, stores=None):
        """Create the container with a list of stores."""
        assert isinstance(stores, (list, tuple)) or stores is None
        if stores is not None:
            assert [isinstance(store, DataStore) for store in stores]
            self._stores = stores
        else:
            self._stores = []

    def __len__(self):
        return len(self._stores)

    def __getitem__(self, i):
        return self._stores[i]

    def add(self, store):
        """Add a store to the container."""
        assert isinstance(store, DataStore)
        self._stores.append(store)

    def add_stores(self, stores):
        """Add several stores to the container at once."""
        assert isinstance(stores, (list, tuple))
        [self.add(store) for store in stores]
