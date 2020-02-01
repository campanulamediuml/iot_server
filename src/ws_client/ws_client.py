from websocket import create_connection
import socket
from threading import Timer, Thread
import json
import time
import _thread as thread
import gevent

# from ws_client.WSRC import WSRC
from common.Scheduler import IntervalTask


class WS_connect(object):
    def __init__(self, SERVER_URL):
        # 启动链接
        print('创建推送链接...')
        self.server_url = SERVER_URL
        # 把传入的网址设置为客户端使用的网址
        self.listener_dict = {}
        # 创建监听字典
        self.connect()
        # 链接到服务器
        IntervalTask(10,self.keep_connect)
        # 保持链接


    def connect(self):
        try:
            self.ws = create_connection(self.server_url)
            # 创建连接
            self.login_as_admin()
            print('与推送服务器连接成功！')
            # admin状态登录
        except Exception as e:
            print('推送服务器超时')
            return

    def keep_connect(self):
        try:
            # print('heartbeat')
            self.send_heart_beat()
            self.send_data('heart_beat',{})
        except Exception as e:
            self.connect()


    def login_as_admin(self):
        self.send_data('ADMIN_IN', {})

    def send_heart_beat(self):
        try:
            self.ws.send('2')
            # self.send_data('heart_beat',{})
            return True
        except Exception as e:
            print('向推送服务器发送心跳失败，正在重新连接...')
            self.connect()
            return

    def disconnect(self):
        self.ws.send('42' + json.dumps(['disconnect']))

    def send_data(self, code, content):
        res = self.send_heart_beat()
        if res != True:
            return 
        
        data = '42' + json.dumps([code, content])
        self.ws.send(data)
        return True


    def on_message(self,message):
        # message = super().recv_frame()
        if len(message) < 2:
            return
        print(message)
        if message[0] == '0':
            print('hand shake...')
            return
        if message[:2] != '42':
            print('not valid info')
            return
        message = message[2:]
        message = json.loads(message)
        event = message[0]
        data = message[1]
        print(data)
        if 'server_token' in data:
            self.add_item(data['server_token'],data)
        return
        # 重写监听信息

    def listen(self):
        try:
            res = self.ws.recv()
            self.on_message(res)
            return
        except Exception as e:
            print(str(e))
            return
        # 监听

    def add_item(self,server_token,data):
        self.listener_dict[data[server_token]] = data
        # 添加进程结果
        return
            
    def get_data_by_event_id(self,event_id):
        self.listen()
        if event_id in self.listener_dict:
            result = self.listener_dict[event_id]
            self.del_data_by_event_id(event_id)
            return result
        else:
            return None 
        # 如果存在进程，则返回对应进程内容

    def del_data_by_event_id(self,event_id):
        if event_id in self.listener_dict:
            self.listener_dict.pop(event_id)
        return

    def get_wsrc_dict(self):
        return self.listener_dict
        # 返回现在的进程池


    
        
 