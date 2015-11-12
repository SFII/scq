"""
Routing configuration.
"""

import tornado.web
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.index_handler import IndexHandler
from handlers.register_handler import RegisterHandler
from handlers.register.culdap_register_handler import CuLdapRegisterHandler
from handlers.dashboard_handler import DashboardHandler
from services.survey import Survey
from services.survey import Surveys

# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register/culdap", CuLdapRegisterHandler),
    (r"/register", RegisterHandler),
    (r"/dashboard/",DashboardHandler),
    (r"/api/survey/(\d+)", Survey),
    (r"/api/survey", Surveys)
]