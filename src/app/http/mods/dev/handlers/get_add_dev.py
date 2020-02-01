# import json
from app.http.handler_base import HandlerBase
from app.http.relay.ws_relay import Relay
from data.server import Data


class get_all_imei(HandlerBase):
    def get(self):
        Relay.get_all_clients()

        all_clients = Relay.get_all_clients()
        clients_list = []
        for client in  all_clients:
            clients_list.append(client.get_imei())
        res = {
            'imei_list':clients_list
        }
        self.send_ok(res)
        return

class send_bind_status(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        Relay.send_bind_status(imei)

        self.send_ok({})
        return

class get_dev_info(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        result = {}

        client = Relay.get_client_by_imei(imei)
        if client != None:
            result['imei'] = client.get_imei()
            result['sid'] = client.get_sid()
            result['last_connect_time'] = client.get_last_connect_time()

        self.send_ok(result)
        return

class machine_start(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        user_info = data['user_info']
        test_type = data['type']
        res = Relay.machine_run(test_type,imei,user_info)
        result = {
            'test_number':res
        }
        self.send_ok(result)
        return





