from app.sock.relay import Relay
from app.sock.handlers.test_http import test_http
from app.sock.handlers.send_info import send_info,send_start,send_byte
from app.sock.handlers.check_clients import check_clients,check_db,check_info
import json

class Recver(object):
    http_methods = [b'GET',b'POST']
    http_interface = [
        '/send_info',
        '/send_byte',
        '/send_start',
        '/check_clients',
        '/check_info',
        '/is_db',
        '/test',
    ]

    @staticmethod
    def receive_msg(client_sid,data):
        client = Relay.get_client_by_sid(client_sid)
        if client == None:
            return
        # print(data)
        # return
        data_list = data.split()
        method = data_list[0]
        if method in Recver.http_methods:
            src = data_list[1].decode('utf-8')
            form = data.split(b'\r\n')
            entry = form[-1]
            try:
                data = json.loads(entry.decode('utf-8'))
            except Exception as e:
                print('收到的requestbody不是一个合法的json')
                data = {}
            # print(data)
            Recver.http_req_handler(src,client_sid,data)
            return
        # 处理http请求
        data_list = data.split(b':')
        # imei = client.get_imei()
        # if imei != None:
            # print('<---------------------------->')
            # print('设备imei:',imei)
            # print('数据:',data)
            # print('<---------------------------->')
        if data_list[0] == b'heart':
            # print(data)
            data_frame = data.split()
            data_string = data_frame[0].decode('utf-8') + ' '
            try:
                data_string += data_frame[1].decode('utf-8')
            except Exception as e:
                print(str(e),'定位信息获取失败')
                data_string += '0,0'
            Relay.update_client(client_sid,data_string)
            return
        # 处理心跳包

        client.write_buffer(data)
        # 不是心跳包也不是http数据就写入buffer


    def http_req_handler(src,client_sid,data):
        print(src,data)
        if src not in Recver.http_interface:
            return
        if src == '/send_info':
            send_info(client_sid,data)
        if src == '/send_start':
            send_start(client_sid,data)
        if src == '/send_byte':
            send_byte(client_sid,data)
        if src == '/check_clients':
            check_clients(client_sid,data)
        if src == '/check_info':   
            check_info(client_sid,data)
        if src == '/is_db':
            check_db(client_sid,data)
        if src == '/test':
            test_http(client_sid,data)
        return
        # http接口


