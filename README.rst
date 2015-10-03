Tornado-sent events
===================

An implementation of the publish/subscribe pattern for the Tornado_ web
server.

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
