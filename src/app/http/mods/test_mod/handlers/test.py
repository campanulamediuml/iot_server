import json

from app.http.handler_base import HandlerBase
from app.http.relay.ws_relay import Relay



class test(HandlerBase):
    def get(self):
        msg = json.dumps(['ACK_EXIT',{'msg':'收到消息'}])
        msg = '42'+msg
        Relay.send_message_to_all_dev(msg)

        all_clients = Relay.get_all_clients()
        clients_list = []
        for client in  all_clients:
            clients_list.append(client.get_imei())
        res = {
            'imei_list':clients_list
        }
        self.send_ok(res)
        return

class refresh_login_info(HandlerBase):
    def get(self):
        return