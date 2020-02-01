import json
import time
from common import common
from data.server import Data


# 获取单个玩家信息
def get_player_list(player_line):
    player_info = {
        'player_id': player_line['id'],
        'name': json.loads(player_line['nickname']),
        'phone': player_line['phone'],
        'join_time': common.time_to_str(player_line['add_time']),
        'status': 0,
    }

    return player_info


# 记录后台操作
def write_admin_record(operate_id, operate_desc, shop_id=0, shop_phone='', player_phone='', activity_id=0, player_id=0,
                       coupon_id=0, temp_id=0, admin_id=0, pac_id=0,adv_id=0,device_id=0):
    params = {
        'operate_id': operate_id,
        'admin_id': admin_id,
        'temp_id': temp_id,
        'operate_desc': operate_desc,
        'player_id': player_id,
        'player_phone': player_phone,
        'adv_id':adv_id,
        'operate_time': int(time.time())
    }
    Data.insert('admin_operate_record', params)