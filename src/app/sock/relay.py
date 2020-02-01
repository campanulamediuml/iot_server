from app.sock.client_manager import client_manager
from config import config
import json
import time

class Relay(object):
    cm = None
    server = None
    http_firstline =  'HTTP/1.1 200 ok\r\n'
    http_header = 'Content-Type: text/json;charset=utf-8\r\n'
    http_frame = http_firstline+http_header


    frame_headers = 'dev_unlock:55 00 0C 4F 50 04 00 00 FF FF FF AA;dev_lock:55 00 0C 53 50 04 00 00 FF FF FF AA;dev_status:55 00 0C 42 56 04 00 00 FF FF FF AA\r\n'
    frame_tail = 'SEND  SOCKET\r\n'

    @staticmethod
    def send_return(imei,payload):
        info = Relay.frame_headers+Relay.frame_tail+payload
        client = Relay.get_client_by_imei(imei)
        if client != None:
            client.send_msg(info)
        return


    
    @staticmethod
    def init(server):
        Relay.server = server
        Relay.cm = client_manager.ClientManager()
    #
    @staticmethod
    def get_http_return_data():
        result = {
            'code':0,
            'msg':'',
        }
        return result
        # 返回值

    @staticmethod
    def send_msg(client,content,is_byte=False):
        return client.send_msg(content,is_byte)
        # 发送消息

    @staticmethod
    def send_ok(client_sid,data):
        content = Relay.get_http_return_data()
        content['data'] = data
        content = json.dumps(content)
        Relay.send_http_msg(client_sid,content)
        return
        # http返回正确

    @staticmethod
    def send_http_msg(client_sid,content):
        response = Relay.http_frame+'\r\n'+content
        client = Relay.get_client_by_sid(client_sid)
        Relay.send_msg(client,response)
        Relay.client_close(client_sid)
        return
        # 发送http消息

    @staticmethod
    def client_close(client_sid):
        client = Relay.get_client_by_sid(client_sid)
        if client == None:
            return
        return Relay.cm.client_close(client_sid)
        # 关闭链接

    @staticmethod
    def is_client(connection):
        return Relay.cm.is_client(connection)
        # 查看这个连接对应的客户端是否存在

    @staticmethod
    def add_new_client(connection):
        print('总连接数:',len(Relay.get_all_client_info()))
        return Relay.cm.add_new_client(connection)
        # 创建链接对应的客户端

    @staticmethod
    def update_client(client_sid,data):
        return Relay.cm.update_client(client_sid,data)
        # 更新客户端心跳

    @staticmethod
    def get_client_by_sid(client_sid):
        return Relay.cm.get_client_by_sid(client_sid)
        # 通过sid获取客户端对象实例

    @staticmethod
    def get_client_by_imei(imei):
        return Relay.cm.get_client_by_imei(imei)
        # 通过imei取得客户端

    @staticmethod
    def get_all_client_info():
        return Relay.cm.show_clients()
        # 获取全部在线客户端信息

    @staticmethod
    def get_client_info(imei):
        return Relay.cm.show_info_by_imei(imei)
        # 获取客户端信息

    @staticmethod
    def send_msg_by_sid(sid,data):
        client = Relay.get_client_by_sid(sid)
        if client != None:
            Relay.send_msg(client,data)
        return
        # 根据sid发送消息

    @staticmethod
    def send_msg_by_imei(imei,data):
        client = Relay.get_client_by_imei(imei)
        if client != None:
            Relay.send_msg(client,data)
        return 
        # 根据imei发送消息

    @staticmethod
    def send_byte_by_imei(imei,data):
        client = Relay.get_client_by_imei(imei)
        if client != None:
            Relay.send_msg(client,data,is_byte=True)
        return 
        # 根据imei发送字节串

    @staticmethod
    def send_byte_by_sid(sid,data):
        client = Relay.get_client_by_sid(sid)
        if client != None:
            Relay.send_msg(client,data,is_byte=True)
        return
        # 根据sid发送字节串

    @staticmethod
    def listen_call_back(imei,return_length):
        client = Relay.get_client_by_imei(imei)
        if client == None:
            return 65536
        client.clean_buffer()
        s_time = int(time.time())
        # data = b''
        while 1:
            # 死循环获取
            data = client.get_buffer()
            if int(time.time()) - s_time > config.mq_time_out:
                break
            if len(data) >= return_length:
                break
            time.sleep(1)
        client.clean_buffer()
        return data
        # 单线程死循环


        






        






