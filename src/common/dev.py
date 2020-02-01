import requests
import time
import json
from data.server import Data
from common import common
from config import config


class dev_v2(object):
    url = 'http://' + config.mqtt_server + ':10086'
    get_unlock = '55 00 0C 4F 50 04 00 00 FF FF FF AA'
    get_lock = '55 00 0C 53 50 04 00 00 FF FF FF AA'
    get_status = '55 00 0C 42 56 04 00 00 FF FF FF AA'
    session = requests.Session()

    @staticmethod
    def post(session, url, payload={}, params={}):
        headers = {'Content-Type': 'application/json'}
        try:
            r = session.post(url, params=params, data=payload, headers=headers)
        except:
            return

        print(r)
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return

    @staticmethod
    def get(session, url, params={}):
        headers = {'Content-Type': 'application/json'}
        print(url)
        try:
            r = session.get(url, params=params, headers=headers)
        except:
            return
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return

    @staticmethod
    def send_command(imei, command):
        url = dev_v2.url + '/send_byte'
        data = json.dumps({
            'imei': imei,
            'need_return': 1,
            'length': 112,
            'content': command,  # 状态
        })
        result = dev_v2.post(dev_v2.session, url, payload=data)
        if result == None:
            return
        else:
            return json.loads(result)['data']

    @staticmethod
    def get_dev_start(imei):
        command = dev_v2.get_unlock
        result = dev_v2.send_command(imei, command)
        print(result)
        if result == None:
            return
        if result['dev_status'] == 65536:
            return
        return result['dev_status']
        # 开机

    @staticmethod
    def get_dev_stop(imei):
        command = dev_v2.get_lock
        # try:
        result = dev_v2.send_command(imei, command)
        if result == None:
            return
        if result['dev_status'] == 65536:
            return
        return result['dev_status']
        # 关机

    # 0-成功，-1-失败，65536-设备不在线
    @staticmethod
    def get_dev_status(imei):
        command = dev_v2.get_status
        result = dev_v2.send_command(imei, command)
        print(result)
        if result == None:
            return
        if result['dev_status'] == 65536:
            return

        dev_status_hex = result["dev_info"]
        try:
            dev_info = dev_v2.get_dev_all_info(dev_status_hex)
        except Exception as e:
            print('解析失败')
            print(str(e))
            return
        dev_info['last_connect_time'] = dev_v2.get_last_connect_time(imei)
        dev_info['pos'] = dev_v2.get_dev_pos(imei)
        return dev_info
        # 设备状态

    @staticmethod
    def get_last_connect_time(imei):
        res = Data.find('CWS_APP.latestreport', [('imei', '=', imei)])
        if res == None:
            return 0
        return common.str_to_time(str(res['time']))
        # 获取设备最后一次通讯时间

    @staticmethod
    def get_dev_pos(imei):
        res = Data.find('CWS_APP.latestreport', [('imei', '=', imei)])
        if res == None:
            return ['0', '0']
        return [res['lng'], res['lat']]
        # 获取设备地理位置

    @staticmethod
    def get_dev_all_info(dev_status_hex):
        string = dev_v2.split_string_code(dev_status_hex)
        print(string)
        code = string.split()
        dev_info = {
            'ver_soft': dev_v2.get_info_from_hex(code[9:25]).decode('utf-8'),
            # 软件版本
            'ver_hard': dev_v2.get_info_from_hex(code[25:41]).decode('utf-8'),
            # 硬件版本
            'imei': dev_v2.get_info_from_hex(code[57:72]).decode('utf-8'),
            # 设备imei
            'dev_status': int(bytes.hex(dev_v2.get_info_from_hex(code[72:73]))),
            # 设备当前状态，1-已经解锁，等待中，2-已经启动，用户按了暂停键，3-正在运行中，4-锁屏状态
            'res_time': int('0x' + bytes.hex(dev_v2.get_info_from_hex(code[73:75])), 16),
            # 设备剩余运行时间，单位秒
        }
        return dev_info

    @staticmethod
    def get_info_from_hex(hex_list):
        info = bytes.fromhex(''.join(hex_list))
        print(info)
        info = info.replace(b'\x00', b'')
        return info

    @staticmethod
    def split_string_code(code):
        string = ''
        for i in range(0, len(code), 2):
            string += code[i:i + 2]
            string += ' '
        # print(string)
        return string

    @staticmethod
    def check_db(imei):
        url = dev_v2.url + '/is_db'
        data = json.dumps({
            'imei': imei,
        })
        result = dev_v2.post(dev_v2.session, url, payload=data)
        return json.loads(result)['data']['client_in_base']




class dev_v3(object):
    url = 'http://' + config.dev_server
    session = requests.Session()

    @staticmethod
    def post(session, url, payload={}, params={}):
        headers = {'Content-Type': 'application/json'}
        try:
            r = session.post(url, params=params, data=payload, headers=headers)
        except:
            return

        print(r)
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return

    @staticmethod
    def get(session, url, params={}):
        headers = {'Content-Type': 'application/json'}
        print(url)
        try:
            r = session.get(url, params=params, headers=headers)
        except:
            return
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return

    @staticmethod
    def send_command(api,command):
        url = dev_v3.url + api
        data = json.dumps(
            command
        )
        result = dev_v3.post(dev_v3.session, url, payload=data)
        if result == None:
            return
        else:
            return json.loads(result)['data']

    @staticmethod
    def get_dev_start(imei,test_type,user_info):
        api = '/dev/machine_start'
        data = {
            'type':test_type,
            'user_info':user_info,
            'imei':imei,
        }
        # user_info = {
        #     bind_user_id:0 //设备绑定者id
        #     member_id: 0 // 使用者id
        #     member_name:'' //使用者姓名
        #     member_group:'' //使用者分组的comment
        #     member_phone:'' //使用者手机号
        # }
        result = dev_v3.send_command(api,data)
        print(result)
        return result

        # 开机

    @staticmethod
    def get_dev_info(imei):
        api = '/dev/get_dev_info'
        data = {
            'imei':imei
        }
        result = dev_v3.send_command(api, data)
        print(result)
        return result
        # 查看设备信息

    @staticmethod
    def send_bind_status(imei):
        api = '/dev/send_bind_status'
        data = {
            'imei': imei
        }
        result = dev_v3.send_command(api, data)
        print(result)
        return result