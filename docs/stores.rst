Data storage and publishing
===========================

In order to publish data to listeners, Tornadose utilizes a data store
concept somewhat reminiscent of that used in Flux_. In short,
subscribers start listening to a data store and are notified when
there are updates.

.. _Flux: https://facebook.github.io/flux/

.. autoclass:: tornadose.stores.BaseStore
   :members:

.. autoclass:: tornadose.stores.DataStore

.. autoclass:: tornadose.stores.QueueStore
