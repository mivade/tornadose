Changelog
=========

Version 0.2.2
-------------

*2015-10-21*

* Fix bug that printed out all messages sent with websocket
  subscribers which was originally present for debugging purposes.

Version 0.2.1
-------------

*2015-10-17*

* Subscription handlers automatically get registered with stores. This
  simplifies creating custom handlers.

Version 0.2.0
-------------

*2015-10-11*

* Reworks stores and handlers (backwards incompatible!).
* Adds a new queue-based ``QueueStore`` store.
* Implements a websocket-based subscriber to supplement
  ``EventSource``.
* Begins to add unit testing.

Version 0.1.2
-------------

*2015-09-20*

* Defines an ``EventSource`` request handler and a ``DataStore``
  object for using server-sent events with Tornado.
