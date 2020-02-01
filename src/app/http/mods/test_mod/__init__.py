from app.http.mods.test_mod.handlers.test import test
from app.http.mods.test_mod.handlers.gen_test import gen_test
from app.http.mods.test_mod.handlers.ws_sender import ws_sender
from app.http.mods.test_mod.handlers.mqtt_test import mqtt_test
from app.http.mods.test_mod.handlers.pic_test import pic_test

from app.http.mods.test_mod.handlers.dev_run import dev_start,dev_stop,check_dev,check_db


route_list = [
    (r'/test/test', test),
    (r'/test/gen_test', gen_test),
    (r'/test/ws_sender', ws_sender),
    (r'/test/mqtt_test', mqtt_test),
    (r'/test/pic_test', pic_test),

    (r'/test/dev_start', dev_start),
    (r'/test/dev_stop', dev_stop),
    (r'/test/check_dev', check_dev),
    (r'/test/check_db', check_db),

]