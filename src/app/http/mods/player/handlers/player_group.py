import time

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from data.server import Data
from error import error


# 分组展示
class player_show_group(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            name = data['group_name']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        res_list = []
        group_list = []
        group = Data.select('player_group', [('player_id', '=', player_base['id'])])
        if group != None:
            for row in group:
                params = {}
                number = 0
                params['id'] = row['id']
                params['name'] = row['name']
                group_member = Data.select('player_member', [('group_id', '=', row['id'])])
                if group_member != None:
                    number = len(group_member)
                params['group_number'] = number
                res_list.append(params)

        if len(res_list) > 0:
            for i in res_list:
                if name != '':
                    if name in i['name']:
                        group_list.append(i)
                else:
                    group_list.append(i)

        reply = {
            'result': group_list
        }
        self.send_ok(reply)
        return


# 添加分组
class player_add_group(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            name = data['group_name']
            comment = data['group_desc']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        params = {
            'name': name,
            'comment': comment,
            'add_time': int(time.time()),
            'user_id': player_base['id'],
            'status': 1
        }

        Data.insert('player_group', params)

        reply = {
            'commit': 1
        }
        self.send_ok(reply)
        return

# 删除分组
class player_del_group(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            group_id = data['group_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        group = Data.select('player_group', [('id', '=', group_id)])
        if group == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)

        Data.delete('player_group', [('id','=',group_id)])

        reply = {
            'commit': 1
        }
        self.send_ok(reply)
        return

# 修改分组
class player_change_group(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            group_id = data['group_id']
            name = data['group_name']
            comment = data['group_desc']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        group = Data.select('player_group', [('id', '=', group_id)])
        if group == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        Data.update('player_group', [('id','=',group_id)],{'name':name,'comment':comment})

        reply = {
            'commit': 1
        }
        self.send_ok(reply)
        return