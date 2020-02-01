import urllib
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from app.http.relay.relay import Relay
from sdk.wechat_auth import *
from config.wechat_config import WST
from data.server import Data
from error import error


class player_get_appid(HandlerBase):
    @run_on_executor
    def get(self):
        reply = {
            'app_id': WST.APP_ID
        }
        self.send_ok(reply)
        return

class player_login(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            wechat_verify_code = data['code']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_PARAM)

        player_base = wechat_login(wechat_verify_code)
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        token = self.create_token(player_base['id'], table_name="player")

        # player_id = player_base['id']
        # Relay.player_login(player_id, token)
        reply = {
            'token': token,
        }
        self.send_ok(reply)
        return


class player_log_out(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        player_id = player_base['id']
        Data.update('player', [('id', '=', player_id)], {'token': ''})
        if player_id in Relay.player_token_dict:
            Relay.player_token_dict[player_id] = ''

        reply = {
            'logout': 'done!',
        }
        self.send_ok(reply)
        return

class get_wechat_cfg(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()

        print(data)
        url = data['url']
        signDct = sign_wechat(urllib.parse.unquote(url))
        result = {
            'debug': 0,
            'appId': WST.APP_ID,
            'timestamp': signDct['timestamp'],
            'nonceStr': signDct['nonceStr'],
            'signature': signDct['signature'],
        }
        reply = {
            'ticket_data': result
        }
        self.send_ok(reply)

        return

