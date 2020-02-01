import json
import time

from app.http.client_manager.client_manager import dev_manager
from common import common
from data.server import Data


class Relay(object):


    ACK_START = 'ACK_START'
    ACK_BIND = 'ACK_BIND'
    ACK_CONNECT = 'ACK_REG'

    manager = dev_manager()

    @staticmethod
    def regist_ws_connection(connection):
        Relay.manager.create_connection(connection)

        return

    @staticmethod
    def send_message_by_sid(sid, event, msg=None):
        if msg is None:
            msg = {}

        client = Relay.get_client_by_sid(sid)
        if client != None:
            client.send_msg(event,msg)
        return

    @staticmethod
    def send_message_by_imei(imei, event, msg=None):
        if msg is None:
            msg = {}

        client = Relay.get_client_by_imei(imei)
        if client != None:
            client.send_msg(event,msg)
        return

    @staticmethod
    def machine_run(test_type,imei,user_info):
        event = Relay.ACK_START
        data = {
            'type':test_type, # 使用类型
            'user_info':user_info,  # 使用者id
            'test_number':common.get_md5(str(time.time())+common.create_rand_string(12)),
        }
        params = {
            'test_number':data['test_number'],
            'test_type':test_type
        }
        Data.insert('user_test_result',params)
        Relay.send_message_by_imei(imei,event,data)
        return data['test_number']

    @staticmethod
    def send_bind_status(imei):
        bind_status = {}
        bind_info = Data.find('devices',[('imei','=',imei)])
        if bind_info == None:
            bind_status['bind_status'] = 0
            # 没绑定
        else:
            bind_status['bind_status'] = 1
            # 已经被绑定
        event = Relay.ACK_BIND
        Relay.send_message_by_imei(imei,event,bind_status)

    @staticmethod
    def send_message_to_all_dev(msg):
        all_clients = Relay.get_all_clients()
        for client in all_clients:
            client.send_msg(event='',msg=msg)
        return

    @staticmethod
    def get_all_clients():
        return Relay.manager.get_all_clients()


    @staticmethod
    def get_client_by_sid(sid):
        return Relay.manager.get_client_by_sid(sid)

    @staticmethod
    def get_client_by_imei(imei):
        return Relay.manager.get_client_by_imei(imei)

    @staticmethod
    def disconnect(connection):
        Relay.manager.kill_connection(connection)
        return


    @staticmethod
    def update_heartbeat_by_sid(sid):
        Relay.manager.update_heartbeat_by_sid(sid)
        return
