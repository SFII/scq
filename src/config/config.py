"""
Application configuration.

All settings should be configurable through flags or environment variables.
Secrets must be configured through envrionment variables.
"""

import tornado.web
from tornado.options import define, options
from config.routes import routes

SETTINGS = {
    'cookie_secret': "8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=",
    'autoreload': True,
    'template_path':'templates/',
    'static_path':'static/',
    'login_url': '/login'
}

define('port', default=8000, help='run on the given port', type=int)
define('database_name', default='scq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)

application = tornado.web.Application(handlers=routes, **SETTINGS)
