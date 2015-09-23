"""Demonstration of using tornadose EventSource handlers to publish
the Fibonacci sequence to listeners.

"""

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from tornadose.handlers import EventSource
from tornadose.stores import DataStore

html = """
<div id="messages"></div>
<script type="text/javascript">
  var source = new EventSource('/events');
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

sequence = fibonacci()


def get_next():
    store.data = next(sequence)


class MainHandler(RequestHandler):
    def get(self):
        self.write(html)

if __name__ == "__main__":
    define('port', default=9000)
    options.parse_command_line()

    app = Application(
        [
            ('/', MainHandler),
            ('/events', EventSource, {'source': store})
        ],
        debug=True
    )
    app.listen(options.port)
    PeriodicCallback(get_next, 1000).start()
    IOLoop.instance().start()
