import time

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from data.server import Data
from error import error


# 成员展示
class player_show_member(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            name = data['member_name']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        player_list = []
        res = []

        group = Data.select('player_group', [('player_id', '=', player_base['id'])])
        if group != None:
            for row in group:
                group_id = row['id']
                players = Data.select('player_member', [('group_id', '=', group_id)])
                if players != None:
                    for player in players:
                        params = {}
                        use_times = 0
                        params['member_name'] = player['name']
                        params['member_id'] = player['id']
                        params['member_phone'] = player['phone']
                        params['group_name'] = row['name']
                        test_result = Data.select('user_test_result', [('user_id', '=', player['id'])])
                        if test_result != None:
                            use_times = len(test_result)
                        params['use_times'] = use_times
                        res.append(params)

        if len(res) > 0:
            for i in res:
                if name != '':
                    if name in i['name']:
                        player_list.append(i)
                else:
                    player_list.append(i)

        reply = {
            'result': player_list
        }
        self.send_ok(reply)
        return


# 添加成员
class player_add_member(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            name = data['member_name']
            group = data['group_id']
            comment = data['comment']
            phone = data['phone']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        group_info = Data.find('player_group',[('id','=',group)])
        if group_info == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        params = {
            'name': name,
            'comment': comment,
            'add_time': int(time.time()),
            'status': 1,
            'phone':phone,
            'group_id':group
        }

        Data.insert('player_member', params)

        reply = {
            'add_success': 1
        }
        self.send_ok(reply)
        return


