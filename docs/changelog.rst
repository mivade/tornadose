Changelog
=========

Version 0.2.1 (Upcoming)
------------------------

* Subscription handlers automatically get registered with stores, simplifying
  the creation of custom handlers.

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
