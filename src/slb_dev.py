from config.config import dev_config
from app.http.http_server import HttpServer
from common import common
import time

host = dev_config['host']
port = dev_config['port']
print('http_server_running', host, port)
server = HttpServer(host, port)
print('['+common.time_to_str(int(time.time()))+']Server Run')
server.run()