from config.config import admin_config
from app.http.http_server import HttpServer
from common import common
import time


host = admin_config['host']
port = admin_config['port']
print('admin_server_running', host, port)
server = HttpServer(host, port)
print('['+common.time_to_str(int(time.time()))+']Server Run')
server.run()
