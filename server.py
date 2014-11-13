# coding: utf-8

from __future__ import print_function

import hmac
import hashlib
import simplejson as json
import os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    pass

class Root(MainHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        payload_body = self.request.body
        if not self.is_verify(payload_body):
            return
        self.send_hipchat(payload_body)

    def is_verify(self, payload_body):
        secret_token = os.environ['GITHUB_WEBHOOK_SECRET_TOKEN']
        signature    = 'sha1=' + hmac.new(secret_token, payload_body, hashlib.sha1).hexdigest()
        if self.request.headers['X-Hub-Signature'] != signature:
            print('GITHUB_WEBHOOK_SECRET_TOKEN not equal signature')
            return False
        return True
        

    def send_hipchat(self, payload_body):
        print(payload_body)

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
