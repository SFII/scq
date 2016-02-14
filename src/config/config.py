"""
Application configuration.

All settings should be configurable through flags or environment variables.
Secrets must be configured through envrionment variables.
"""

import tornado.web
from tornado.options import define, options
from config.routes import routes

application = tornado.web.Application(handlers=routes, **SETTINGS)
