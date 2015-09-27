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
        authd = ldapauth.auth_user_ldap(identikey, password)
        self.write("authd: {0}".format(authd))
        return

def main():
    tornado.options.parse_command_line()
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
