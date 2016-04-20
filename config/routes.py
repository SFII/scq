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
from handlers.profile_handler import ProfileHandler
from handlers.help_handler import HelpHandler
from handlers.surveys_handler import SurveysHandler
from handlers.groups_handler import GroupsHandler
from handlers.abuse_handler import AbuseHandler
from handlers.api.survey_handler import SurveyAPIHandler
from handlers.api.response_handler import ResponseHandler
from handlers.refresh_handler import RefreshHandler
from handlers.api.me_handler import MeHandler
from handlers.api.group_api_handler import GroupAPIHandler
from handlers.api.subscribe_api_handler import SubscribeAPIHandler
from handlers.api.survey_results_handler import SurveyResultsHandler
from handlers.api.search_handler import SearchHandler


# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register/culdap", CuLdapRegisterHandler),
    (r"/register", CuLdapRegisterHandler),
    (r"/dashboard", DashboardHandler),
    (r"/profile", ProfileHandler),
    (r"/help", HelpHandler),
    (r"/surveys", SurveysHandler),
    (r"/groups", GroupsHandler),
    (r"/abuse", AbuseHandler),
    (r"/api/surveys", SurveyAPIHandler),
    (r"/api/response", ResponseHandler),
    (r"/api/results/([\w-]+)", SurveyResultsHandler),
    (r"/api/subscribe", SubscribeAPIHandler),
    (r"/api/search", SearchHandler),
    (r"/api/me", MeHandler),
    (r"/api/groups", GroupAPIHandler),
    (r"/api/refresh", RefreshHandler)
]
