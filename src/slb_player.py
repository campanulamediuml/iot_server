from config.config import player_config
from app.http.http_server import HttpServer
from common import common
import time

host = player_config['host']
port = player_config['port']
print('http_server_running', host, port)
server = HttpServer(host, port)
print('['+common.time_to_str(int(time.time()))+']Server Run')
server.run()