import tornado.web

class ChildHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('child.html')
