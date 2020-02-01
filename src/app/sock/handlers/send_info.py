import time
from app.sock.relay import Relay
from app.sock.tools import tools

def send_info(client_id,data):
    imei = data['imei']
    content = data['content']
    print('需要传输的imei为:',imei)
    print('需要传输的信号为:',content)
    Relay.send_msg_by_imei(imei,content)
    Relay.send_ok(client_id,{})
    return

def send_byte(client_id,data):
    imei = data['imei']
    content = data['content']
    # data_length = data['length']

    byte_data = bytes.fromhex(content)
    print('发送十六进制信息',byte_data)
    print('发送给',imei)

    data_length = tools.get_return_length(byte_data)

    Relay.send_byte_by_imei(imei,byte_data)

    status = 65536
    dev_info = ''
    if data['need_return'] == 1:
        result = Relay.listen_call_back(imei,data_length)
        print(result)
        if result == 65536:
            dev_info = 'device offline!'
        elif result != None:
            if b'OK' in result:
                status = 0
            if b'ER' in result:
                status = -1
            if b'BV' in result:
                status = 0
                dev_info = bytes.hex(result)
    res = {
        'dev_status':status,
        'dev_info':dev_info
    }
    Relay.send_ok(client_id,res)
    return

def send_start(client_id,data):
    # print()
    imei = data['imei']
    content = b'\x55\x00\x0c\x4f\x50\x04\x00\x00\xff\xff\xff\xaa'
    print('发送启动指令,imie:',imei,content)
    Relay.send_byte_by_imei(imei,content)
    Relay.send_ok(client_id,{})
    return

