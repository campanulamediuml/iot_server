import time
from app.sock.relay import Relay

def test_http(client_id,data):
    # data = data
    # print(data['imei'])
    # print(data['content'])
    # print(type(data))

    result = {
        'time':int(time.time()),
        'res':data
    }

    Relay.send_ok(client_id,result)
    return