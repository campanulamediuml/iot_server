import time
from app.http.client_manager.client import dev_client

class dev_manager(object):
    def __init__(self):
        self.dev_dict = {}

    def create_connection(self, connection):
        sid = id(connection)
        new_client = dev_client(connection,sid)
        self.dev_dict[sid] = new_client

        return new_client
    # 添加新的链接

    def kill_connection(self, connection):
        sid = id(connection)
        client = self.get_client_by_sid(sid)
        if client != None:
            client.close_connection()
        if sid in self.dev_dict:
            self.dev_dict.pop(sid)
        return
    # 关闭链接

    def get_client_by_sid(self, sid):
        if sid in self.dev_dict:
            client = self.dev_dict[sid]
            return client
        return
    # 根据sid获取客户端
    def get_client_by_imei(self, imei):
        for client in self.dev_dict.values():
            if client.get_imei() == imei:
                return client
        return

    def update_heartbeat_by_sid(self, sid):
        client = self.get_client_by_sid(sid)
        if client != None:
            client.update_heartbeat()
        return

    def get_all_clients(self):
        all_clients = []
        for clients in self.dev_dict.values():
            if clients != None:
                all_clients.append(clients)
        return all_clients
        # 获取全部客户端连接

