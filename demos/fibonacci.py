"""Demonstration of using tornadose EventSource handlers to publish
the Fibonacci sequence to listeners.

"""

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from tornadose.handlers import EventSource
from tornadose.stores import DataStore

html = """
<div id="messages"></div>
<script type="text/javascript">
  var source = new EventSource('/fibonacci');
  source.onmessage = function(message) {
    var div = document.getElementById("messages");
    div.innerHTML = message.data + "<br>" + div.innerHTML;
  };
</script>"""

store = DataStore()


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

if __name__ == "__main__":
    define('port', default=9000)
    options.parse_command_line()

    IOLoop.instance().run_sync(main)
