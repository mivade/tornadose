"""Basic example that appears in the REAMDME."""

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
