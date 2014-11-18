# coding: utf-8

from __future__ import print_function

import hmac
import hashlib
import os
from os import path
import simplejson as json
import tornado.ioloop
import tornado.web

from models.hipchat import HipChat


BASE_DIR = path.dirname(path.abspath(__file__))

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
            return False
        return True

    def send_hipchat(self, payload_body):
        hc = HipChat()
        hc.send_message_to(room_id='', message=payload_body)


class Config(object):
    def __init__(self):
        f = open(BASE_DIR + '/config.json')
        json_data = json.load(f)
        self.token = json_data['token']
        self.room_id = json_data['room_id']
        self.color = json_data['color']

    def get_room_id(self, room):
        return self.room_id.get(room)


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
