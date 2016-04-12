Tornado-sent events
===================

An implementation of the publish/subscribe pattern for the Tornado_ web
server.

Installation
------------

Tornadose is on PyPI:

.. code-block:: bash

    $ pip install tornadose

This will grab the latest official release. Alternatively, or for development,
you can clone the repository and install it manually:

.. code-block:: bash

    $ git clone https://github.com/mivade/tornadose.git
    $ cd tornadose
    $ pip install -e .

Usage
-----

A simple example of using server-sent events (a.k.a. EventSource):

.. code-block:: python

   import random
   from tornado.ioloop import IOLoop, PeriodicCallback
   from tornado.web import Application
   from tornadose.handlers import EventSource
   from tornadose.stores import DataStore

   store = DataStore()

   app = Application(
       [(r'/', EventSource, {'store': store})],
       debug=True)
   app.listen(9000)

   loop = IOLoop.instance()
   PeriodicCallback(lambda: store.submit(random.random()), 1000).start()
   loop.start()

To monitor the stream with curl_:

.. code-block:: bash

   $ curl http://localhost:9000

or with HTTPie_:

.. code-block:: bash

   $ http -S get localhost:9000

Additional demos can be found in the ``demos`` directory.

Contributing
------------

Contributions, complaints, criticisms, and whatever else are welcome. The source
code and issue tracker can be found on GitHub_.

See also
--------

Some other implementations of server-sent events with Tornado include:

* tornado-sse_
* tornado-eventsource_

License
-------

Tornadose is freely available under the terms of the MIT license. See
``LICENSE`` for details.

.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _EventSource: https://developer.mozilla.org/en-US/docs/Web/API/EventSource
.. _curl: http://curl.haxx.se/
.. _HTTPie: https://github.com/jkbrzt/httpie
.. _tornado-sse: https://github.com/truetug/tornado-sse
.. _tornado-eventsource: https://github.com/guilhermef/tornado-eventsource
.. _GitHub: https://github.com/mivade/tornadose
