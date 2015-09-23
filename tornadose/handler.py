"""Backwards-compatibility layer. This will likely be removed in
future releases of tornadose.

"""

import warnings
from .handlers import EventSource

warnings.warn(
    'tornado.handler is deprecated. Import from tornado.handlers instead.',
    DeprecationWarning)
