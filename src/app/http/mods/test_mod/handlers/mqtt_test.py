from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from mqtt_client.MQ import MQ


class mqtt_test(HandlerBase):
    @run_on_executor
    def get(self):

        # event_id = get_event_id()
        data = self.get_data()
        imei = data['imei']
        mq_res = MQ.machine_start(imei)

        if mq_res == True:
            # res = Data.find('test',[('id','!=',0)])
            self.send_ok({'status':0})

        else:
            self.write({'status':65536})
        return
