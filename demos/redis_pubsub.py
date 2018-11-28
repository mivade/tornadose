"""Running this demo assumes a Redis instance installed on localhost
with default port and no authentication requirements.

"""

from uuid import uuid4
from tornado import log
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application, RequestHandler
from tornadose.stores import RedisStore
from tornadose.handlers import EventSource
import redis

store = RedisStore(channel='mychannel')


def send_random_string(store):
    store.submit(str(uuid4()), debug=True)


class MainHandler(RequestHandler):
    def get(self):
        self.render('redis-pubsub.html')


if __name__ == "__main__":
    log.enable_pretty_logging()
    app = Application([
        (r'/', MainHandler),
        (r'/stream', EventSource, dict(store=store))
    ], template_path='templates', debug=True)
    app.listen(8765)
    print('Listening on port 8765')

    loop = IOLoop.current()
    PeriodicCallback(lambda: send_random_string(store), 500).start()
    loop.call_later(10, lambda: redis.StrictRedis().publish('mychannel', 'called later!'))
    loop.start()
