
from app.http.mods.dev.handlers.get_add_dev import get_all_imei, get_dev_info, machine_start, send_bind_status

route_list = [
    ('/dev/get_all_imei',get_all_imei),
    ('/dev/get_dev_info',get_dev_info),
    ('/dev/machine_start',machine_start),
    ('/dev/send_bind_status',send_bind_status),
]