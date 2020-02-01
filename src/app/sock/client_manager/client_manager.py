from common.Scheduler import IntervalTask
from config.config import dev_heart_beat
from app.sock.client_manager.dev_client import dev_client
from common import common
import time

class ClientManager(object):
    def __init__(self):
        self.client_dict = {}
        # self.keep_connect()
        print('创建客户端管理器')
    #
        IntervalTask(10,self.keep_connect)
    #
    def keep_connect(self):
        # print('<----------------清理超时客户端-------------------->')
        time_out_sid_list = self.get_time_out_sid()
        for sid in time_out_sid_list:
            print(sid,'超时')
            self.client_close(sid)
        # print('<---------------------------------------->')
        return

    def is_client(self,connecion):
        client_sid = id(connecion)
        if client_sid in self.client_dict:
            return True
        else:
            return False
        # 判断客户端是否存在

    def get_time_out_sid(self):
        res = []
        for client in self.client_dict.values():
            if int(time.time())-client.get_last_connect_time() > dev_heart_beat:
                res.append(client.get_sid())
        return res

    def add_new_client(self,connecion):
        client_sid = id(connecion)
        client = dev_client(client_sid,connecion)
        self.client_dict[client_sid] = client
        return client
        # 添加新的客户端对象

    def update_client(self,client_sid,data):
        client = self.get_client_by_sid(client_sid)
        imei = data.split()[0].split('IMEI')[1]
        pos = data.split()[1].split(',')
        client.update_client_info_by_heart(imei,pos)
        client_sid = client.get_sid()

        self.clean_same_client(imei,client_sid)
        # 关闭所有同imei不同sid的客户端
        print('[',common.time_to_str(int(time.time())),'SID:',client_sid,']RECEIVE')
        print('客户端',imei,client_sid,'发生更新')
        print('=====================================================')
        return 
        # 更新客户端信息

    def clean_same_client(self,imei,client_sid):
        all_client_sid = []
        for client in self.client_dict.values():
            if client.get_imei() == imei:
                all_client_sid.append(client.get_sid())

        if len(all_client_sid) > 1:
            print(imei,'存在',len(all_client_sid),'个重复客户端')
        for sid in all_client_sid:
            if sid != client_sid:
                self.client_close(sid)
        return 
        # 清理同一个imei下全部已挂起客户端

    def get_client_by_sid(self,client_sid):
        if client_sid in self.client_dict:
            return self.client_dict[client_sid]
        return  None
        # 通过sid获取client

    def client_close(self,client_sid):
        client = self.get_client_by_sid(client_sid)
        print(client_sid)
        if client != None:
            # connection = client.get_connection()
            client.kill_connect()
            # 退出事件注册表
            if client_sid in self.client_dict:
                self.client_dict.pop(client_sid)

        print('客户端',client_sid,'关闭连接')
        return
        # 关闭client

    def get_client_by_imei(self,imei):
        for client in self.client_dict.values():
            if client.get_imei() == imei:
                return client
        return

    def show_clients(self):
        result = []
        for client in self.client_dict.values():
            info = client.get_client_attr()
            result.append(info)
        return result


    def show_info_by_imei(self,imei):
        client = self.get_client_by_imei(imei)
        if client != None:
            info = client.get_client_attr()
            return info
        return















