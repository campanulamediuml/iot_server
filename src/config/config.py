thread_num = 8
# 服务器线程数量
debug_mode = False
# 是否debug
update_token = False
# 是否开启更新token
thread_pool_num = 40
# 线程池数量
VERIFY_CODE = '1234'
# 万能邀请码
jump_paid = True
show_sql = False
dev_heart_beat = 45

logical_url = ''
# 服务端地址

db_config = {
    'host': '127.0.0.1',
    'user': '',
    'password': '',
    'database': '',
    'port': 3306,
}

tel_verify = {
    'url': 'http://m.5c.com.cn/api/send/index.php',
    'api_key': '',
    'username': '',
    'pw': '',
}

mongo_address = "mongodb://127.0.0.1:27017"
refresh_time = '00:00:00'

# socket_config = {
#     'host': '0.0.0.0',
#     'port': 7780
# }


admin_config = {
    'host': '0.0.0.0',
    'port': 7777
}
player_config = {
    'host': '0.0.0.0',
    'port': 7778
}
dev_config = {
    'host': '0.0.0.0',
    'port': 7779
}
socket_config = {
    'host': '0.0.0.0',
    'port': 10086
}

dev_server = ':'+str(dev_config['port'])
mqtt_server = ''
dev_v2_server = ':10086'
default_pic = ''

mq_time_out = 15

push_config = {
    'host': '0.0.0.0',
    'port': 9001,
    'client_host': '127.0.0.1'
}
# ws超时时间
ws_time_out = 15
# token超时时间
token_time_out = 60 * 10

# 用户类型
admin_type = 9
player_type = 10



# agent setting
MIN_WTIHDRAW = 200

# 提现相关参数
withdraw_status_no = 0
withdraw_status_doing = 1
withdraw_status_done = 2

new_package_id = [65536]
# 新用户首充套餐id


