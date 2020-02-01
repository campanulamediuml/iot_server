from app.sock.sock_base import socket_base
from config.config import socket_config

host = socket_config['host']
port = socket_config['port']
server = socket_base(host,port)
server.run()
