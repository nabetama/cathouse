# coding: utf-8
from hypchat import HypChat
import simplejson as json

class Config(object):
    def __init__(self):
        f = open('config.json')
        json_data = json.load(f)
        self.token = json_data['token']
        self.room_id = json_data['room_id']
        self.color = json_data['color']

    def get_room_id(self, room):
        return self.room_id.get(room)
config=Config()


class HipChat(object):
    def __init__(self, token=config.token):
        self.token = token

    def send_message_to(self, room_id, message):
        hipchat = HypChat(self.token)
        room = hipchat.get_room(config.get_room_id('bot'))
        room.notification(message, color=config.color)

