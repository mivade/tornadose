Tornado-sent events
===================

Tornadose is a simple module for defining Tornado_ request handlers
that can stream data to clients using the EventSource_ interface (also
known as server-sent events or SSE). Although similar functionality
can be accomplished using Tornado's built-in support for websockets,
the EventSource interface has a few advantages:

* It is a normal HTTP connection and so can be more easily monitored
  than websockets using tools like curl_ or HTTPie_.
* Browsers generally automatically try to reestablish a lost
  connection.
* The publish/subscribe pattern is better suited to some applications
  than the full duplex model of websockets.

Implementation
--------------

Some other modules already exist to add SSE functionality to Tornado,
including `tornado-sse`_ and `tornado-eventsource`_. Tornadose works
slightly differently in that it uses a data store to be notified of
new data to publish to clients, a model which was in part inspired by
the Flux_ architecture. This allows the ``EventSource`` request
handler to be entirely decoupled from the actual data source and thus
minimize external requirements for Tornadose itself.

Usage
-----

A simple example of usage:

.. code-block:: python

   import random
   from tornado.ioloop import IOLoop, PeriodicCallback
   from tornado.web import Application
   from tornadose.handler import EventSource
   from tornadose.stores import DataStore

   store = DataStore()

   app = Application(
       [(r'/', EventSource, {'source': store})],
       debug=True)
   app.listen(9000)

   loop = IOLoop.instance()
   PeriodicCallback(lambda: store.set_data(random.random()), 1000).start()
   loop.start()

To monitor the stream with curl:

.. code-block:: bash

   $ curl http://localhost:9000

or with HTTPie:

.. code-block:: bash

   $ http -S get localhost:9000

See also the ``demos`` directory for further examples.

License
-------

Tornadose is freely available under the terms of the MIT license. See
``LICENSE`` for details. The source code can be found on GitHub_.

.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _EventSource: https://developer.mozilla.org/en-US/docs/Web/API/EventSource
.. _curl: http://curl.haxx.se/
.. _HTTPie: https://github.com/jkbrzt/httpie
.. _tornado-sse: https://github.com/truetug/tornado-sse
.. _tornado-eventsource: https://github.com/guilhermef/tornado-eventsource
.. _Flux: https://facebook.github.io/flux/
.. _GitHub: https://github.com/mivade/tornadose
