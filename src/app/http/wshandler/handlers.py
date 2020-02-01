import json

from app.http.relay.ws_relay import Relay
import time

from common import common


class interface(object):

    @staticmethod
    def dev_reg(sid, data):
        imei = data['imei']
        client = Relay.get_client_by_sid(sid)
        if client == None:
            print('sid不存在')
            return

        client.login(imei)
        event = Relay.ACK_CONNECT
        msg = {
            'sid': common.get_md5(client.get_sid())
        }
        client.send_msg(event, msg)
        return

    @staticmethod
    def get_dev_check_result(sid,data):
        imei = data['imei']
        # {
        #     'imei':'',
        #     'test_time':'', //1900-01-01-00:00:00
        #     'left':0, // 右眼
        #     'right':0, // 左眼
        #     'member_id':0, // 使用者id
        #     'test_type':1  // 测试类型 1-视力 2-散光
        #     'astigmia_left':1 // 散光  1-有 0-没有
        #     'astigmia_right': 1  // 散光  1-有 0-没有
        #     'status':0  // 状态 0-正常 1-异常错误
        # }
        client_from_sid = Relay.get_client_by_sid(sid)
        client_from_imei = Relay.get_client_by_imei(imei)
        if id(client_from_imei) != id(client_from_sid):
            print('通过imei和sid取得的客户端不同')
            return

        client = client_from_imei
        if client != None:
            client.update_user_test_info(data)
        return

    @staticmethod
    def update_dev_info(sid,data):
        pos = data['pos']
        client = Relay.get_client_by_sid(sid)
        if client != None:
            client.update_heartbeat()
            client.update_dev_pos(pos)
        return


    # @staticmethod
    # def machine_run(imei,type,member_id):
    #     data = [
    #         'ACK_START',
    #         {
    #             'type':type
    #             'member_id':member_id
    #         }
    #     ]
    #     msg = '42'+json.dumps(data)
    #     client = Relay.get_client_by_imei(imei)
    #     if client != None:
    #         client.send_msg(msg)
    #     return



