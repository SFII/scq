import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options

import ldapauth
import db
from models.user import User

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(db.course() + ", SECTION COUNT: " + db.section_count())

class MyselfHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""
                <form method="post" action="/myself">
                <b>Enter Your Identikey</b><br>
                <input type="text" name="identikey"><br>
                <b>Enter Your Password</b><br>
                <input type="password" name="password"></p>
                <input type="submit" value="Submit">
                </form>
            """)
    def post(self):
        identikey = self.get_argument('identikey')
        password = self.get_argument('password')
        print User
        print User.get(uid=identikey)
        authd = ldapauth.auth_user_ldap(identikey, password)
        attrs = ['cn','cuEduPersonPrimaryMajor1','cuEduPersonPrimaryMajor2','cuEduPersonSecondaryMajor1','cuEduPersonSecondaryMajor2','cuEduPersonSecondaryMinor','mail','cuEduPersonClass']
        results = ldapauth.user_info_ldap(identikey, attrs)[0]
        print results[1]
        writeout = "authd: {0}<br>".format(authd)
        if authd:
            writeout += "{0}".format(results)
        self.write(writeout)
        return

def main():
    tornado.options.parse_command_line()
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'cookie_secret': '8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=',
        'xsrf_cookies': True,
        'login_url': '/login'
    }
    # Tornado pro-tip: regex routing is optimized by putting more frequently
    # accessed routes and simpler regexes before other routes.
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler), #index
            (r"/myself", MyselfHandler)
        ]
    )
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
