import tornado.web

class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('dashboard.html')