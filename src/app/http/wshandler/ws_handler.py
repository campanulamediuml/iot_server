from tornado.websocket import WebSocketHandler

from app.http.relay.receiver import Rec

import json

from app.http.relay.ws_relay import Relay


class ws_handler(WebSocketHandler):
    def check_origin(self, origin):
        return True
        # 同源检测
    def open(self):
        Relay.regist_ws_connection(self)
        return

    def on_message(self, message):
        Rec.recv(self,message)
        return

    def on_close(self):
        Relay.disconnect(self)
        return
