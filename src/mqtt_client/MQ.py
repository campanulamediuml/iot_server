from mqtt_client.client import mqtt_connection
from config import config
from common import common
from mgdb.mgdb import dbapi
import time
import json
from common.common import dbg
from common.dev import dev_v2
from data.server import Data

class MQ(object):
    # mq_client = mqtt_connection(config.mqtt_server,1883,client_name='web_admin_server')

    @staticmethod
    def send_mqtt_info(mq_client, imei, topic, data):
        return mq_client.send_message(imei, topic, data)

    @staticmethod
    def get_send_result(mq_client, event_id):
        return mq_client.get_send_result(event_id)

    @staticmethod
    def disconnect(mq_client):
        return mq_client.disconnect()

    @staticmethod
    def send_data(imei, topic, data):
        # event_id = str(event_id)
        event_id = common.get_event_id()
        mq_client = mqtt_connection(config.mqtt_server,1883,event_id,topic)

        rec = MQ.send_mqtt_info(mq_client, imei, topic, data)
        if rec is False:
            return None

        start_time = int(time.time())
        while 1:
            res = MQ.get_send_result(mq_client, event_id)
            if res is not None:
                break
            time.sleep(0)
            if int(time.time()) - start_time > config.mq_time_out:
                break

        MQ.disconnect(mq_client)
        return res
        # 监听信息

    @staticmethod
    def machine_start(imei, pulse=12, high=100, low=100):
        # res = dev_v2.get_dev_status(imei)
        # if res != None:
        rep = Data.find('CWS_APP.latestreport',[('imei','=',imei)])
        if int(time.time()) - common.str_to_time(str(rep['time'])) < config.dev_heart_beat:
            v2 = dev_v2.get_dev_start(imei)
            if v2 != None:
                if v2 == 0:
                    print(v2)
                    return True
                if v2 == -1:
                    print(v2)
                    return False
            # 先走v2信号
        if rep['status'] == 'heart':
            return False

        print('V2信号没有走通')
        imei = imei
        pulse = 12
        money = pulse
        device_type = 1
        duration = 5
        high = high
        low = low
        topic = 'deveventreq'

        data = bytearray([0x54, device_type])
        data += money.to_bytes(4, 'big')
        data += duration.to_bytes(4, 'big')
        data += high.to_bytes(4, 'big')
        data += low.to_bytes(4, 'big')
        data += pulse.to_bytes(4, 'big')
        dbg('发送的信号', data)

        mongodata = {
            'imei': imei,
            'datagram_type': 1,
            'device_type': device_type,
            'duration': duration,
            'high': high,
            'low': low,
            'pulse': pulse
        }

        result = MQ.send_data(imei, topic, data)
        if result and result['result']:
            mongodata['result'] = 0  # 成功
            dbapi.insert_datagram(mongodata)
            # device = dbapi.get_device(imei=imei)
            return True
        else:
            mongodata['result'] = 1  # 设备正在运行
            dbapi.insert_datagram(mongodata)
            return False

    @staticmethod
    def send_pulse(imei,pulse,high,low):
        topic = 'deveventreq'
        duration = 5
        money = pulse
        device_type = 1

        data = bytearray([0x54, device_type])
        data += money.to_bytes(4, 'big')
        data += duration.to_bytes(4, 'big')
        data += high.to_bytes(4, 'big')
        data += low.to_bytes(4, 'big')
        data += pulse.to_bytes(4, 'big')

        result = MQ.send_data(imei,topic, data)
        if result and result['result']:
            return True
        else:
            return False

        return
