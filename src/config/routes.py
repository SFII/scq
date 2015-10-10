"""
Routing configuration.
"""

import tornado.web
from handlers.loginhandler import LoginHandler
from handlers.indexhandler import IndexHandler

settings = {
    'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
    'xsrf_cookies': True,
    'login_url': '/login'
}

# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/([0-9]+)/", LoginHandler)
]

application = tornado.web.Application(handlers=routes,
                                      template_path='templates/',
                                      settings=settings)
