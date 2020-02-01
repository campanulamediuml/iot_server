import json
import time
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from app.http.mods.admin import admin_tools
from common.common import str_to_time
from data.server import Data
from error import error
from app.http.mods.admin.admin_tools import write_admin_record


# 会员管理首页
class get_player_list(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_player_list')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            player_name = data['player_name']
            player_phone = data['player_phone']
            start_time = data['start_time']
            end_time = data['end_time']
            status = data['status']  # 0代表用户账户正常，1代表冻结
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if player_phone == '':
            player_phone = "%"
        if start_time != '':
            start_time += ' 00:00:00'
            start_time = str_to_time(start_time)
        else:
            start_time = 0
        if end_time != '':
            end_time += ' 00:00:00'
            end_time = str_to_time(end_time)
        else:
            end_time = int(time.time())

        players = []
        player_list = Data.select('player', [('phone', 'like', '%{}%'.format(player_phone))],
                                  order=('join_time', 'desc'))

        if player_list:
            for player in player_list:
                if start_time <= int(player['join_time']) <= end_time:
                    players.append(player)
            res_list = list(map(admin_tools.get_player_list, players))
        else:
            res_list = []

        res = []
        for i in res_list:
            if i == None:
                continue
            if player_name != '':
                if player_name in i['name']:
                    res.append(i)
            else:
                res.append(i)

        res1 = []
        for i in res:
            if int(status) == i['status']:
                res1.append(i)

        result = {
            'player_info_list': res1
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='会员管理首页')

        return


# 会员详细信息
class get_player_info(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_player_info')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            player_id = data['player_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)
        player = Data.find('player', [('id', '=', player_id)])
        player_info = {}
        if player:
            player_info['nickname'] = player['nickname']
            player_info['phone'] = player['phone']
            player_info['sex'] = player['sex']
            player_info['add_time'] = player['add_time']
            player_info['open_id'] = player['open_id']
            player_info['union_id'] = player['union_id']

        result = {
            'player_info': player_info
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='会员详细信息', player_id=player_id)

        return
