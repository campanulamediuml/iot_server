import time

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from common import dev
from common.dev import dev_v3
from data.server import Data
from error import error


# 绑定设备
class player_add_device(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            imei = data['imei']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        devinfo = dev_v3.get_dev_info(imei)
        if devinfo == None:
            return self.send_faild(error.ERROR_DEV_NOY_CONNECT_YET)

        device = Data.find('devices', [('imei', '=', imei)])
        if device:
            if device['user_id'] == '':
                Data.update('devices', [('imei', '=', imei)], {'user_id': player_base['id']})
            else:
                return self.send_faild(error.ERROR_DEVICE_EXISTS)

        dev_v3.send_bind_status(imei)
        reply = {
            'commit': 1
        }
        self.send_ok(reply)
        return


# 设备管理界面 查看已绑定设备
class player_device_list(HandlerBase):
    @run_on_executor
    def get(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)
        devices_list = []
        devices = Data.select('devices', [('user_id', '=', player_base['id'])])
        if devices != None:
            for device in devices:
                params = {}
                params['imei'] = device['imei']
                params['bind_time'] = device['ctime']
                devices_list.append(params)

        # 返回最后一条测试记录
        test_params = {}
        test_info = Data.find_last('user_test_result', [('player_id', '=', player_base['id'])], info='test_time',
                                   limit=1)
        if test_info != None:
            player_id = test_info['user_id']
            player_info = Data.find('player_member', [('id', '=', player_id)])
            if player_info == None:
                return self.send_faild(error.ERROR_NO_USER)
            group_id = player_info['group_id']
            group_info = Data.find('player_group', [('id', '=', group_id)])
            if group_info == None:
                return self.send_faild(error.ERROR_DATA_NOT_FOUND)
            imei_info = Data.find('dev_main', [('imei', '=', test_info['imei'])])
            if imei_info == None:
                return self.send_faild(error.ERROR_INVALIDATE_IMEI)
            test_params['imei'] = test_info['imei']
            test_params['player_name'] = player_info['name']
            test_params['group_name'] = group_info['name']
            test_params['left_eye'] = test_info['left_eye']
            test_params['astigmatism_left'] = test_info['astigmatism_left']
            test_params['right_eye'] = test_info['right_eye']
            test_params['astigmatism_right'] = test_info['astigmatism_right']

        reply = {
            'devices_list': devices_list,
            'test_info': test_params
        }
        self.send_ok(reply)
        return


# 用户选择设备界面
class player_chose_device(HandlerBase):
    @run_on_executor
    def get(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)
        devices_list = []
        devices = Data.select('devices', [('user_id', '=', player_base['id'])])
        if devices != None:
            for device in devices:
                params = {}
                params['imei'] = device['imei']
                device_info = Data.find_last(
                    'user_test_result', [('imei', '=', device['imei'])],
                    info='test_time', limit="1")
                if device_info != None:
                    test_time = device_info['test_time']
                else:
                    test_time = device['ctime']
                params['last_use_time'] = test_time
                devices_list.append(params)

        reply = {
            'devices_list': devices_list
        }
        self.send_ok(reply)
        return


# 解绑设备
class player_unbind_device(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            imei = data['imei']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        devinfo = dev_v3.get_dev_info(imei)
        if devinfo == None:
            return self.send_faild(error.ERROR_DEV_NOY_CONNECT_YET)

        dev = Data.find('devices', [('imei', '=', imei)])
        if dev == None:
            return self.send_faild(error.ERROR_DEVICE_EXISTS)

        params = {
            'imei': imei,
            'ctime': int(time.time()),
            'user_id': '',
            'times': 0,
            'status': 0
        }

        Data.update('devices', [('imei', '=', imei)], params)

        dev_v3.send_bind_status(imei)
        reply = {
            'commit': 1
        }
        self.send_ok(reply)
        return


# 使用设备
class player_use_device(HandlerBase):
    @run_on_executor
    def post(self):
        player_base = self.get_player_base()
        if player_base is None:
            return self.send_faild(error.ERROR_NO_USER)

        try:
            data = self.get_post_data()
            imei = data['imei']
            member_id = data['member_id']
            type = data['type']  # 0视力检测 1 散光检测 65536 视力和散光

        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        commit = 0
        devinfo = dev_v3.get_dev_info(imei)
        if devinfo == None:
            return self.send_faild(error.ERROR_DEV_NOY_CONNECT_YET)

        # 用户信息
        bind_user = Data.find('devices', [('imei', '=', imei)])
        if bind_user == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        bind_user_id = bind_user['id']
        use_user = Data.find('player_member', [('id', '=', member_id)])
        if use_user == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        member_name = use_user['name']
        member_phone = use_user['phone']
        group_id = use_user['group_id']

        group_info = Data.find('player_group', [('id', '=', group_id)])
        if group_info == None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        member_group = group_info['comment']
        user_info = {

            'bind_user_id': bind_user_id,  # 设备绑定者id
            'member_id': member_id,  # 使用者id
            'member_name': member_name,  # 使用者姓名
            'member_group': member_group,  # 使用者分组的comment
            'member_phone': member_phone,  # 使用者手机号
        }
        dev_start = dev.dev_v3.get_dev_start(imei, type, user_info)
        if dev_start != None:
            commit = 1

        reply = {
            'commit': commit # 1为成功 0为失败
        }
        self.send_ok(reply)
        return
