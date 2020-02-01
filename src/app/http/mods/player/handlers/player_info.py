from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from data.server import Data
from error import error



class player_info(HandlerBase):
    @run_on_executor
    def get(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        player_info = Data.find('player', [('id', '=', player_base['id'])])
        params = {}
        if player_info:
            params['nickname'] = player_info['nickname']
            params['sex'] = player_info['sex']
            params['avatar'] = player_info['avatar']
            params['phone'] = player_info['phone']
        reply = {
            'plyer_info':params
        }
        self.send_ok(reply)
        return

class player_change_nickname(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)
        try:
            data = self.get_post_data()
            nickname = data['nickname']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        player = Data.find('player',[('id','=',player_base['id'])])
        if player is None:
            return self.send_faild(error.ERROR_NO_USER)

        Data.update('player',[('id', '=', player_base['id'])],{'nickname':nickname})

        reply = {
            'commit':1
        }
        self.send_ok(reply)
        return


class player_change_phone(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)
        try:
            data = self.get_post_data()
            phone = data['phone']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        player = Data.find('player',[('id','=',player_base['id'])])
        if player is None:
            return self.send_faild(error.ERROR_NO_USER)

        Data.update('player',[('id', '=', player_base['id'])],{'phone':phone})

        reply = {
            'commit':1
        }
        self.send_ok(reply)
        return