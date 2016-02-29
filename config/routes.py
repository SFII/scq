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
from handlers.raw_dump_handler import RawDumpHandler
from handlers.surveys_handler import SurveysHandler
from handlers.groups_handler import GroupsHandler
from handlers.api.survey_handler import SurveyHandler
from handlers.api.response_handler import ResponseHandler
from handlers.refresh_handler import RefreshHandler
from handlers.user_info_handler import UserInfoHandler
from handlers.user_info_update_handler import UserInfoUpdateHandler
from handlers.api.me_handler import MeHandler
from handlers.api.group_api_handler import GroupAPIHandler
from handlers.api.subscribe_api_handler import SubscribeAPIHandler


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
    (r"/rawdump", RawDumpHandler),
    (r"/surveys", SurveysHandler),
    (r"/groups", GroupsHandler),
    (r"/api/surveys", SurveyHandler),
    (r"/api/response", ResponseHandler),
    (r"/api/subscribe", SubscribeAPIHandler),
    (r"/api/me", MeHandler),
    (r"/api/groups", GroupAPIHandler),
    (r"/api/refresh", RefreshHandler),
    (r"/userinfo", UserInfoHandler),
    (r"/userinfo/update", UserInfoUpdateHandler)
]
