"""
Application configuration.

All settings should be configurable through flags or environment variables.
Secrets must be configured through envrionment variables.
"""

import tornado.web
from tornado.options import define
from routes import routes

settings = {
    'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
    'xsrf_cookies': True,
    'login_url': '/login'
}

define("port", default=8000, help="run on the given port", type=int)

application = tornado.web.Application(handlers=routes,
                                      debug=True,
                                      template_path='templates/',
                                      static_path='static/',
                                      settings=settings)
