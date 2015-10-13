"""
Application configuration.

All settings should be configurable through flags or environment variables.
Secrets must be configured through envrionment variables.
"""
application = tornado.web.Application(handlers=routes,
                                      template_path='templates/',
                                      static_path='assets/',
                                      settings=settings)

settings = {
    'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
    'xsrf_cookies': True,
    'login_url': '/login'
}
