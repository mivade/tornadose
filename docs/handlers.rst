Request handlers
================

Tornadose defines handlers for using the EventSource_ interface or
WebSockets_. For other handlers, the :class:`BaseHandler` class is
provided.

.. _EventSource: https://developer.mozilla.org/en-US/docs/Web/API/EventSource
.. _WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

.. autoclass:: tornadose.handlers.BaseHandler
   :show-inheritance:
   :members:

.. autoclass:: tornadose.handlers.EventSource
   :show-inheritance:
   :members: initialize, publish

.. autoclass:: tornadose.handlers.WebSocketSubscriber
   :show-inheritance:
   :members: open, publish
