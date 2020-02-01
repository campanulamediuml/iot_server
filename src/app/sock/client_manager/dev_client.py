import time
from data.server import Data
from common import common

class dev_client(object):
    def __init__(self,sid,connection):
        self.last_connect_time = int(time.time())
        self.sid = sid
        self.pos = None
        self.imei = None
        self.connection = connection
        self.buffer_info = b''

    def get_buffer(self):
        return self.buffer_info

    def clean_buffer(self):
        self.buffer_info = b''
        return self.buffer_info

    def write_buffer(self,data):
        self.buffer_info += data
        return 
    # 数据缓存

    def update_client_info_by_heart(self,imei,pos):
        self.pos = pos
        self.last_connect_time = int(time.time())
        self.imei = imei
        self.update_devices_info()
        return
    # 更新心跳信息

    def update_devices_info(self):
        res = Data.find('CWS_APP.devices',[('imei','=',self.imei)])
        if res == None:
            self.create_device()

        # 创建全新的设备信息
        report = {
            'imei':self.get_imei(),
            'lng':self.get_pos()[0],
            'lat':self.get_pos()[1],
            'time':common.time_to_str(int(time.time())),
            'status':'heart',
        }
        resp = Data.find('CWS_APP.latestreport',[('imei','=',self.imei)])
        if resp == None:
            Data.insert('CWS_APP.latestreport',report)
        else:
            Data.update('CWS_APP.latestreport',[('imei','=',self.imei)],report)
            print(self.get_imei(),'写入通讯表')
        return
        # 更新最后通讯时间

    def create_device(self):
        params = {
            'imei':self.get_imei(),
            'sn':self.get_imei(),
            'valid_time':common.time_to_str(int(time.time())),
            'lastshakingtime':common.time_to_str(int(time.time())),
            'lastlowbatterytime':common.time_to_str(0),
            'lastlosingexternalpowertime':common.time_to_str(0),
            'lastcrossingbordertime':common.time_to_str(0),
            'lastoverspeedtime':common.time_to_str(0),
        }
        Data.insert('CWS_APP.devices',params)
        print('创建设备imei',self.get_imei())
        # 创建设备
    
    def get_client_attr(self):
        info = {
            'imei':self.get_imei(),
            'sid':self.get_sid(),
            'pos':self.get_pos(),
            'lst':self.get_last_connect_time(),
        }
        return info
    # 获取这个客户端的各种信息

    def get_imei(self):
        return self.imei
    # 获取imei

    def get_sid(self):
        return self.sid
    # 获取sid

    def get_pos(self):
        return self.pos
    # 获取地理坐标

    def get_last_connect_time(self):
        return self.last_connect_time
    # 获取最后通讯时间

    def get_connection(self):
        return self.connection
    # 获取通讯handler

    def send_msg(self,data,is_byte=False):
        if is_byte == False:
            print('发送字符串',data)
            return_data = bytes(data,encoding="utf-8")
        else:
            print('发送字节串',data)
            return_data = data
        self.connection.send(return_data)
        print('发送数据完毕')
        return
    # 发送信息到客户端

    def kill_connect(self):
        return self.connection.close()
    # 关闭连接


