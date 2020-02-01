import json
import time

from data.server import Data


class dev_client(object):
    def __init__(self,connection,sid):
        self.imei = ''
        self.connection = connection
        self.last_connect_time = int(time.time())
        self.sid = sid
        self.pos = ['0','0']

    def login(self,imei):
        if self.imei == '':
            self.imei = imei
            self.update_device_info(imei)
        return

    def send_msg(self, event='', msg=None):
        if msg is None:
            msg = {}
        connection = self.get_connection()
        if event == '':
            connection.write_message('3')
            return

        payload = [
            event,
            msg
        ]
        msg = json.dumps(payload)
        connection.write_message('42'+msg)
        return
        # 发送消息

    def update_device_info(self, imei):
        dev_info = Data.find('dev_main',[('imei','=',imei)])
        if dev_info == None:
            params = {
                'imei':imei,
                'last_connect_time':int(time.time()),
                'ctime':int(time.time())
            }
            Data.insert('dev_main',params)
        else:
            params = {
                'last_connect_time': int(time.time()),
            }
            Data.update('dev_main',[('imei','=',imei)],params)
        # self.update_heartbeat()
        self.last_connect_time = int(time.time())
        # 更新设备信息
        return



    def update_user_test_info(self,data):
        params = {
            'imei':data['imei']
        }
        return

    def get_connection(self):
        return self.connection
        # 获取链接对象

    def get_imei(self):
        return self.imei

    def get_sid(self):
        return self.sid

    def get_last_connect_time(self):
        return self.last_connect_time

    def update_heartbeat(self):
        if self.get_imei() != '':
            self.update_device_info(self.get_imei())
            self.send_msg(event='')
        # 只有存在imei才会正确操作心跳系统
        return

    def update_dev_pos(self,pos):
        self.pos = pos
        return

    def close_connection(self):
        connection = self.get_connection()
        connection.close()
        return
        # 关闭链接









