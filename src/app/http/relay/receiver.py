import json
from app.http.relay.ws_relay import Relay
from app.http.wshandler.handlers import interface


class Rec(object):
    api_table = {
        'REQ_REG' : interface.dev_reg,
        'REQ_UPDATE_DEV_INFO':interface.update_dev_info,
        'REQ_RESULT':interface.get_dev_check_result,
    }

    @staticmethod
    def recv(connection,msg):
        message = str(msg)
        sid = id(connection)
        if message == '2':
            Relay.update_heartbeat_by_sid(sid)
            # 更新心跳包
            return
        if message[:2] == '42':
            content = message[2:]
            print(content)
            print(type(content))
            msg_body_list = json.loads(content)
            interface = msg_body_list[0]
            if interface in Rec.api_table:
                Rec.api_table[interface](sid,msg_body_list[1])
        return
