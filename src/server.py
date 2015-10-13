import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options
from config.config import application

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print "Listening for connections on... localhost:{0}".format(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
