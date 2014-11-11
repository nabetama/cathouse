# coding: utf-8

from __future__ import print_function
import os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    pass

class Root(MainHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        s_json = self.get_argument('payload')
        print(s_json)

application = tornado.web.Application([
    (r"/", Root)
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    )

if __name__ == '__main__':
    application.listen(8888)
    print("Server is up...")
    tornado.ioloop.IOLoop.instance().start()
