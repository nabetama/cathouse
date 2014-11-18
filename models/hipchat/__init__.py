# coding: utf-8
from hypchat import HypChat

class HipChat(object):
    def __init__(self, token):
        from server import Config
        self.config = Config()
        self.token = self.config.token

    def send_message_to(self, room_id, message):
        hipchat = HypChat(self.token)
        room = hipchat.get_room(self.config.get_room_id('bot'))
        room.notification(message, color=self.config.color)

