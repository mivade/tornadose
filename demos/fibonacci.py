"""Demonstration of using tornadose EventSource handlers to publish
the Fibonacci sequence to listeners.

"""

import signal
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.locks import Event
from tornado.web import Application, RequestHandler
from tornadose.handlers import EventSource
from tornadose.stores import DataStore

define('port', default=9000)

html = """
<div id="messages"></div>
<script type="text/javascript">
  var source = new EventSource('/fibonacci');
  source.onmessage = function (message) {
    var div = document.getElementById("messages");
    div.innerHTML = message.data + "<br>" + div.innerHTML;
  };
</script>"""

store = DataStore()
finish = Event()


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class MainHandler(RequestHandler):
    def get(self):
        self.write(html)


@gen.coroutine
def generate_sequence():
    for number in fibonacci():
        store.submit(number)
        yield gen.sleep(1)
        if finish.is_set():
            break


@gen.coroutine
def main():
    app = Application(
        [
            ('/', MainHandler),
            ('/fibonacci', EventSource, {'store': store})
        ],
        debug=True
    )
    app.listen(options.port)
    yield generate_sequence()


def shutdown(sig, frame):
    finish.set()
    IOLoop.instance().stop()


if __name__ == "__main__":
    options.parse_command_line()
    signal.signal(signal.SIGINT, shutdown)
    IOLoop.instance().run_sync(main)
