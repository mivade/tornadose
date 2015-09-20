"""A simple example of using the ``EventSource`` handler. To see
streaming data, do::

  $ curl http://localhost:9000

"""

import random
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application
from tornado import log
from tornadose.handler import EventSource
from tornadose.stores import DataStore

log.enable_pretty_logging()

store = DataStore()

app = Application(
    [(r'/', EventSource, {'source': store})],
    debug=True)
app.listen(9000)

loop = IOLoop.instance()
PeriodicCallback(lambda: store.set_data(random.random()), 1000, loop).start()
loop.start()
