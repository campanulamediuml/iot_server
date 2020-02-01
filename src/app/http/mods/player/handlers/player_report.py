import time

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from common import dev
from common.common import str_to_time
from data.server import Data
from error import error


# 使用报告
class player_report_list(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            name = data['name']
            group_name = data['group_name']
            comment = data['comment']
            start_time = data['start_time']
            end_time = data['end_time']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

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
        report_list = []

        # 关联的手机号
        user = Data.find('player', [('id', '=', player_base['id'])])
        phone = user['phone']

        # 所有用户列表
        player_list = Data.select('player_member', [('id', '=', 0)])

        # 要查的使用记录的id列表
        player_id_list = []

        # 通过组查id
        group_id = []
        group_info = Data.select('player_group', [('player_id', '=', player_base['id'])])
        if group_info != None:
            for row in group_info:
                group_id.append(row['id'])

        for player in player_list:
            if len(group_id) >0:
                if player['group_id'] in group_id:
                    player_id_list.append(player['id'])
            elif player['phone'] == phone:
                player_id_list.append(player['id'])

        if len(player_id_list) > 0:
            for id in player_id_list:
                # 一个人可能多条记录
                player_info = Data.find('player_member', [('id', '=', id)])
                if player_info == None:
                    continue
                group = Data.find('player_group', [('id', '=', player_info['group_id'])])
                if group == None:
                    continue
                test_report_list = Data.select('user_test_result', [('user_id', '=', id)])
                if test_report_list == None:
                    continue

                for test_report in test_report_list:
                    params = {}
                    params['name'] = player_info['name']
                    params['group'] = group['name']
                    params['group_id'] = group['group_id']
                    params['imei'] = test_report['imei']
                    params['test_time'] = test_report['test_time']
                    params['left_eye'] = test_report['left_eye']
                    params['astigmatism_left'] = test_report['astigmatism_left']
                    params['right_eye'] = test_report['right_eye']
                    params['astigmatism_right'] = test_report['astigmatism_right']
                    params['comment'] = test_report['comment']
                    report_list.append(params)

        res1 = []
        res2 = []
        res3 = []
        res4 = []
        if len(report_list) > 0:
            for i in report_list:
                if name != '':
                    if name in i['name']:
                        res1.append(i)
                else:
                    res1.append(i)

            for i in res1:
                if group_name != '':
                    if group_name in i['group']:
                        res2.append(i)
                else:
                    res2.append(i)

            for i in res2:
                if comment != '':
                    if comment in i['group']:
                        res3.append(i)
                else:
                    res3.append(i)

            for i in res3:
                if start_time <= str_to_time(i['test_time']) <= end_time:
                    res4.append(i)
                else:
                    res4.append(i)

        reply = {
            'report_list': res4
        }
        self.send_ok(reply)
        return




# 根据手机号返回使用报告
class player_report_phone_list(HandlerBase):
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

        report_list = []

        # 要查的使用记录的id列表
        player_id_list = []

        # 通过关联手机号查id
        player_by_phone = Data.select('player_member', [('phone', '=', phone)])
        if player_by_phone != None:
            for player in player_by_phone:
                player_id_list.append(player['id'])

        if len(player_id_list) > 0:
            # 遍历所有id
            for id in player_id_list:
                # 一个人可能多条记录
                test_report_list = Data.select('user_test_result', [('user_id', '=', id)])
                if test_report_list == None:
                    continue
                player_info = Data.find('player_member', [('id', '=', id)])
                if player_info == None:
                    continue

                group = Data.find('player_group', [('id', '=', player_info['group_id'])])
                if group == None:
                    continue

                for test_report in test_report_list:
                    params = {}
                    params['name'] = player_info['name']
                    params['group'] = group['name']
                    params['group_id'] = group['group_id']
                    params['imei'] = test_report['imei']
                    params['test_time'] = test_report['test_time']
                    params['left_eye'] = test_report['left_eye']
                    params['astigmatism_left'] = test_report['astigmatism_left']
                    params['right_eye'] = test_report['right_eye']
                    params['astigmatism_right'] = test_report['astigmatism_right']
                    params['comment'] = test_report['comment']
                    report_list.append(params)

        reply = {
            'report_list': report_list
        }
        self.send_ok(reply)
        return
