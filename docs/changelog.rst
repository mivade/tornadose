Changelog
=========

Version 0.5
-----------

*Upcoming*

* Remove ready event from ``DataStore``.

Version 0.4.1
-------------

*2016-06-30*

* Point release which includes a source distribution on PyPI. This
  avoids problems if Tornadose is a requirement listed in a ``setup.py``
  file since setuptools doesn't do wheels.

Version 0.4.0
-------------

*2016-05-28*

* Added a Redis-backed data store. This allows for cross-application
  publishing since anything can publish to the channel the store is
  listening to.

Version 0.3.0
-------------

*2015-12-08*

* Improve performance by always using a Queue for message handling.

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
