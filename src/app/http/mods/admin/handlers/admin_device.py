import time
from tornado.concurrent import run_on_executor
from werkzeug.security import generate_password_hash
from common import common
from common.common import str_to_time
from data.server import Data
from error import error
from app.http.handler_base import HandlerBase
from app.http.mods.admin.admin_tools import write_admin_record


# 获取设备列表
class get_devices_list(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_devices_list')

        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            imei = data['imei']
            player_name = data['player_name']
            phone = data['phone']
            start_time = data['start_time']
            end_time = data['end_time']
            status = data['status']
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

        devices = Data.select('devices',[('id','!=',0)])
        devices_list = []
        if devices:
            for device in devices:
                user_id = device['user_id']
                user_info = Data.find('player',[('id','=',user_id)])
                if user_info is None:
                    continue
                dev_info = Data.find('dev_main', [('id', '=', device['id'])])
                if dev_info is None:
                    continue
                params = {}
                params['id'] = device['id']
                params['player_name'] = user_info['nickname']
                params['phone'] = user_info['phone']
                params['imei'] = device['imei']
                params['ctime'] = device['ctime']
                params['status'] = device['status']
                devices_list.append(params)

        # 筛选
        res = []
        res1 = []
        res2 = []
        res3 = []
        res4 = []
        if len(devices_list) >0:
            for i in devices_list:
                if start_time <= str_to_time(i['ctime']) <= end_time:
                    res.append(i)
            for i in res:
                if imei in i['imei']:
                    res1.append(i)
            for i in res1:
                if player_name in i['player_name']:
                    res2.append(i)
            for i in res2:
                if phone in i['phone']:
                    res3.append(i)
            for i in res3:
                if status == i['status']:
                    res4.append(i)

        result = {
            'devices_list': res4
        }

        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='获取设备列表')

        return


# 获取设备详情
class get_device_detail(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_device_detail')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            device_id = data['device_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        device_info = Data.find('devices',[('id','=',device_id)])
        if device_info == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        params = {}
        params['imei'] = device_info['imei']
        params['ctime'] = device_info['ctime']
        params['times'] = device_info['times']
        params['status'] = device_info['status']
        params['user_id'] = device_info['user_id']
        user_info = Data.find('player',[('id','=',params['user_id'])])
        if user_info is None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        params['user_nickname'] = user_info['nickname']


        result = {
            'device_info':params,
        }

        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='获取设备详情', device_id=device_id)

        return

# 获取设备测试记录
class get_device_test(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_device_detail')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            imei = data['imei']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        test_list = []
        test_info_list = Data.select('user_test_result',[('imei','=',imei)])
        if test_info_list != None:
            for test_info in test_info_list:
                params = {}
                player_id = test_info['user_id']
                player_info = Data.find('player_member',[('id','=',player_id)])
                if player_info == None:
                    continue
                params['player_name'] = player_info['name']
                params['phone'] = player_info['phone']
                params['comment'] = test_info['comment']
                params['left_eye'] = test_info['left_eye']
                params['right_eye'] = test_info['right_eye']
                if test_info['astigmatism_left'] +test_info['astigmatism_left'] >0:
                    params['astigmatism'] = 1
                else:
                    params['astigmatism'] = 0
                test_list.append(params)

        result = {
            'test_list':test_list
        }

        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='获取设备测试记录', device_id=device_id)

        return