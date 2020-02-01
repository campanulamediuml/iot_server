from common.dev import dev_v2
from app.http.handler_base import HandlerBase

class dev_start(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        res = dev_v2.get_dev_start(imei)
        if res == None:
            result = {
                'dev_info':'设备不在线'
            }
        if res == 0:
            result = {
                'dev_info':'开机成功'
            }
        if res == -1:
            result = {
                'dev_info':'开机失败，设备报错'
            }
        self.send_ok(result)
        return


class dev_stop(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        res = dev_v2.get_dev_stop(imei)
        if res == None:
            result = {
                'dev_info':'设备不在线'
            }
        if res == 0:
            result = {
                'dev_info':'停止成功'
            }
        if res == -1:
            result = {
                'dev_info':'停止失败，设备报错'
            }
        self.send_ok(result)
        return


class check_dev(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        res = dev_v2.get_dev_status(imei)
        
        result = {
            'data':res
        }
        
        self.send_ok(result)
        return


class check_db(HandlerBase):
    def post(self):
        data = self.get_post_data()
        imei = data['imei']
        res = dev_v2.check_db(imei)
        if res == 1:
            result = {
                'dev_info':'设备在数据库中'
            }
        else:
            result = {
                'dev_info':'设备不在数据库中'
            }

        self.send_ok(result)
        return




        
        
