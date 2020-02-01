import socket
import time
from common.common import get_md5
from app.sock.relay import Relay
import time
import threading
from app.sock.recver import Recver as REC
import os

# os.system('ulimit –n 0')

class socket_base(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket_server = socket.socket()
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        # 运行
        Relay.init(self)
        self.socket_server.bind((self.host,self.port))
        # self.socket_server.setblocking(False)
        self.socket_server.listen()
        print('socket服务器开始监听',self.host,self.port)
        self.recieve_run_pool()
        return

    def recieve_run_pool(self):
        # Relay.init(self)
        while True:
            connection,addr = self.socket_server.accept()
            if Relay.is_client(connection) == False:
                Relay.add_new_client(connection)
                t = threading.Thread(target = self.reciever,args=(connection,))
                t.start()


    def reciever(self,connection):
        # 监听器
        client_sid = id(connection)
        client = Relay.get_client_by_sid(client_sid)
        try:
            self.message_handler(client)
        except Exception as e:
            print(str(e))
        return

    def message_handler(self,client):
        # 对消息进行处理
        while 1:
            connection = client.get_connection()
            client_sid = client.get_sid()
            # imei = client.get_imei()
            data_byte = self.recv_total_msg(connection)
            if data_byte == None:
                Relay.client_close(client_sid)
                return
            if len(data_byte) == 0:
                Relay.client_close(client_sid)
                return
            print('接收数据长度',len(data_byte))
            # print('<---------------------------->')
            # 数据
            REC.receive_msg(client_sid,data_byte)

    def recv_total_msg(self,connection):
        # 获取消息
        try:
            data_byte = connection.recv(1024)
            if len(data_byte) == 0:
                return 
            data_frame = data_byte.split()
            if data_frame[0] == b'POST':
                if b'}' not in data_frame[-1]:
                    data_byte += connection.recv(1024)
            return data_byte
            # return data
        except Exception as e:
            print(str(e))
            return






        