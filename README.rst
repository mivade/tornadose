Tornado-sent events
===================

Tornadose is a simple module for defining Tornado_ request handlers
that can stream data to clients using the EventSource_ interface.

Usage
-----

Data to be pushed to clients is stored in ``DataStore`` objects. When
its data is updated, ``EventSource`` handlers will publish the new
data to listeners.

.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _EventSource: https://developer.mozilla.org/en-US/docs/Web/API/EventSource
