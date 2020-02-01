import time
from app.sock.relay import Relay
from data.server import Data

def check_clients(client_id,data):
    result = Relay.get_all_client_info()
    res = {
        'client_num':len(result),
        'clients':result,
    }
    Relay.send_ok(client_id,res)
    return

def check_info(client_id,data):
    imei = data['imei']
    result = Relay.get_client_info(imei)
    if result == None:
        result = {}
    res = {
        'client_info':result
    }
    Relay.send_ok(client_id,res)
    return

def check_db(client_id,data):
    imei = data['imei']
    res = Data.find('CWS_APP.devices',[('imei','=',imei)])
    if res == None:
        result = {
            'client_in_base':0
        }
        
    else:
        result = {
            'client_in_base':1
        }
    Relay.send_ok(client_id,result)
    return


