import time
from datetime import datetime

from common.dev import dev_v2
from data.server import Data
from mgdb.mgdb import dbapi
from config import config



# ====================设备========================
# 获取设备状态 None为不存在设备，0离线 1在线 4关机
def get_device_status(imei):
    using_status = is_dev_using(imei)
    if using_status == True:
        return 65536
    # 使用中
    if using_status == 65536:
        return
    # 无法获取状态


    device = Data.find('CWS_APP.devices', [('imei', '=', imei)])
    if device is None:
        return None

    status = dbapi.get_cws_device_status(imei)
    online = -1
    if status:
        online = status.get('online', -1)

    latest_report = dbapi.get_device_latestreport(imei)
    if not latest_report:
        return None
    # dbg((datetime.now().timestamp(), latest_report['time'].timestamp()))
    if datetime.now().timestamp() - latest_report['time'].timestamp() > 150:
        if online == 1:
            online = 0

    return online


def can_dev_use(imei):
    res = Data.find('forbidden_dev', [('imei', '=', imei)])
    if res != None:
        return 1
    else:
        return 0


def get_device_info(device_line):
    imei = device_line['imei']
    online_status = get_device_status(imei)
    if online_status is None:
        return

    belong_info = Data.find('devices_belong', [('imei', '=', imei)])

    if belong_info is None:
        shop_name = ''
    else:
        shop_info = Data.find('openluat_user', [('id', '=', belong_info['shop_id'])])
        shop_name = shop_info['company']

    device_data = {
        'imei': imei,
        'online': online_status,
        'shop_name': shop_name,
        'add_time': device_line['valid_time'],
        'status': online_status
    }

    return device_data


def is_dev_using(imei):
    latest_rep = Data.find('CWS_APP.latestreport',[('imei','=',imei)])
    if latest_rep['status'] == 'heart':
        res = dev_v2.get_dev_status(imei)
        if res == None:
            return 65536
        if res['dev_status'] == 4:
            return False
        return True


    res = Data.find('devices_using_rec', [('imei', '=', imei)], order=['playing_time', 'desc'])
    if res is None:
        return False

    if int(time.time()) - res['playing_time'] < 30 * 60:
        return True

    return False


def get_dev_user(imei):
    res = Data.find('devices_using_rec', [('imei', '=', imei), ('playing_time', '>', int(time.time()) - (30 * 60))],
                    order=['playing_time', 'desc'])

    if res == None:
        return '无'

    player_id = res['player_id']
    return Data.find('player', [('id', '=', player_id)])['phone']


# ===================分润======================


def set_shares(service_pac_rec):
    # 购买的时候立刻进行分润
    # 判断设备的所属主公司
    service_pac_rec = update_service_pac_rec_by_semi_company(service_pac_rec)

    shop_id = service_pac_rec['buy_shop_id']
    share_line = get_share_rate(shop_id)
    write_my_share(service_pac_rec, share_line)
    # 写入店铺分润
    cal_share_distr(service_pac_rec, share_line)
    # 处理业务员分润
    cal_share_shop(service_pac_rec, share_line)
    # 处理店铺分润


def update_service_pac_rec_by_semi_company(service_pac_rec):
    return service_pac_rec


def write_my_share(service_pac_rec, share_line):
    shop_info = Data.find('openluat_user', [('id', '=', service_pac_rec['buy_shop_id'])])

    shop_share_info = Data.find('shop_distr', [('user_id', '=', service_pac_rec['buy_shop_id'])])

    if service_pac_rec['can_upgrade'] == 1:
        params = {
            'upgrade_times': shop_share_info['upgrade_times'] + 1
        }
        Data.update('shop_distr', [('user_id', '=', service_pac_rec['buy_shop_id'])], params)

    # shop_share_info = Data.find('shop_distr', [('user_id', '=', service_pac_rec['buy_shop_id'])])

    if shop_share_info['upgrade_times'] >= shop_share_info['max_upgrade_times']:
        shop_share = shop_share_info['shop_share_max'] - share_line['arrival_share']
    else:
        shop_share = shop_share_info['shop_share_min'] - share_line['arrival_share']

    #
    # arrival_share = (10000 - share_line['arrival_share']) / 10000

    arrival_share = (share_line['arrival_share'] * service_pac_rec['cost']) / 10000
    # 保存到店消费

    print('arrival_share', arrival_share)
    shop_share_raw = (shop_share * service_pac_rec['cost']) / 10000
    print('shop_share_raw', shop_share_raw)

    distr_agent_params = {
        'user_id': service_pac_rec['buy_shop_id'],
        'share': int(shop_share_raw),
        # 到店分润要处理
        'withdraw_status': config.withdraw_status_no,
        'withdraw_type': config.shop_share,
        # 分润类型，业务员还是店铺
        'buy_time': service_pac_rec['buy_time'],
        # 分润时间
        'withdraw_id': service_pac_rec['id'],
        # 对应的那条用户消费的id
    }

    Data.insert('withdraw_record', distr_agent_params)
    print('门店自己的分润', distr_agent_params['share'])
    write_arrival_share(service_pac_rec, shop_share_raw, arrival_share)
    # 写入直属店家的分润


def write_arrival_share(service_pac_rec, shop_share_raw, arrival_share):
    params = {
        'ctime': int(time.time()),
        'max_use_time': service_pac_rec['can_use_quantity'],
        'money': arrival_share,
        'service_rec_id': service_pac_rec['id'],
    }
    Data.insert('arrival_share', params)


def create_insert_params(params):
    insert_params = {
        'user_id': params[0],
        'share': params[1],
        'withdraw_status': params[2],
        'withdraw_type': params[3],
        # 分润类型，业务员还是店铺
        'buy_time': params[4],
        # 分润时间
        'withdraw_id': params[5],
        # 对应的那条用户消费的id
    }
    return insert_params


# 计算来自店铺系统的分润
def cal_share_shop(service_pac_rec, share_line):
    shop_id = service_pac_rec['buy_shop_id']
    res = Data.find('openluat_user', [('id', '=', shop_id)])
    shop_zone_code = res['zone_code']
    print('店铺所在区号', shop_zone_code)

    zone_distr_id = get_zone_distr_shop(shop_zone_code)
    print('店铺所在区代理', zone_distr_id)

    city_and_province_distr = get_city_distr_shop(shop_zone_code)
    print('店铺所在市代理', city_and_province_distr)

    city_distr_list = city_and_province_distr[0]
    province_distr_id = city_and_province_distr[1]
    # 获取区域代理，省代理，市代理的用户id
    distr_dict = {
        'province': province_distr_id,
        'city': city_distr_list,
        'zone': zone_distr_id,
    }
    set_distr_dict_rec(distr_dict, share_line, service_pac_rec)
    # 储存店铺分润

    set_distr_agent_rec(distr_dict, share_line, service_pac_rec)
    # 店铺推荐人分润


def set_distr_agent_rec(distr_dict, share_line, service_pac_rec):
    if distr_dict['province'] is not None:
        distr_agent_line = Data.find('distr_relation', [('user_id', '=', distr_dict['province'])])
        distr_agent_id = distr_agent_line['upper_id']
        print('省推荐人', distr_agent_id)
        if distr_agent_id != 0:
            distr_agent_params = {
                'user_id': distr_agent_id,
                'share': int((share_line['province_agent_share'] * service_pac_rec['cost']) / 10000),
                'withdraw_status': config.withdraw_status_no,
                'withdraw_type': config.zone_agent_reward,
                # 分润类型，业务员还是店铺
                'buy_time': service_pac_rec['buy_time'],
                # 分润时间
                'withdraw_id': service_pac_rec['id'],
                # 对应的那条用户消费的id
            }
            Data.insert('withdraw_record', distr_agent_params)
            print('省代推荐人的分润', distr_agent_params['share'], distr_agent_id)
            # 省代理推荐人分润记录

    if distr_dict['city'] is not None:
        for city_distr_id in distr_dict['city']:
            distr_agent_line = Data.find('distr_relation', [('user_id', '=', city_distr_id)])
            distr_agent_id = distr_agent_line['upper_id']
            print('市推荐人', distr_agent_id)
            if distr_agent_id != 0:
                distr_agent_params = {
                    'user_id': distr_agent_id,
                    'share': int((share_line['city_agent_share'] * service_pac_rec['cost']) / 10000),
                    'withdraw_status': config.withdraw_status_no,
                    'withdraw_type': config.zone_agent_reward,
                    # 分润类型，业务员还是店铺
                    'buy_time': service_pac_rec['buy_time'],
                    # 分润时间
                    'withdraw_id': service_pac_rec['id'],
                    # 对应的那条用户消费的id
                }
                Data.insert('withdraw_record', distr_agent_params)
                print('市代推荐人的分润', distr_agent_params['share'], distr_agent_id)
                # 市代理推荐人分润记录

    if distr_dict['zone'] is not None:
        for zone_distr_id in distr_dict['zone']:
            distr_agent_line = Data.find('distr_relation', [('user_id', '=', zone_distr_id)])
            distr_agent_id = distr_agent_line['upper_id']
            print('区域推荐人', distr_agent_id)
            if distr_agent_id != 0:
                distr_agent_params = {
                    'user_id': distr_agent_id,
                    'share': int((share_line['zone_agent_share'] * service_pac_rec['cost']) / 10000),
                    'withdraw_status': config.withdraw_status_no,
                    'withdraw_type': config.zone_agent_reward,
                    # 分润类型，业务员还是店铺
                    'buy_time': service_pac_rec['buy_time'],
                    # 分润时间
                    'withdraw_id': service_pac_rec['id'],
                    # 对应的那条用户消费的id
                }
                Data.insert('withdraw_record', distr_agent_params)
                print('区代推荐人的分润', distr_agent_params['share'], distr_agent_id)
            # 区代理推荐人分润记录


def set_distr_dict_rec(distr_dict, share_line, service_pac_rec):
    if distr_dict['province'] is not None:
        params_province = {
            'user_id': distr_dict['province'],
            'share': int((share_line['privince_share'] * service_pac_rec['cost']) / 10000),
            'withdraw_status': config.withdraw_status_no,
            'withdraw_type': config.zone_reward,
            # 分润类型，业务员还是店铺
            'buy_time': service_pac_rec['buy_time'],
            # 分润时间
            'withdraw_id': service_pac_rec['id'],
            # 对应的那条用户消费的id
        }
        Data.insert('withdraw_record', params_province)
        print('省代的分润', params_province['share'], distr_dict['province'])

    if distr_dict['city'] is not None:
        for city in distr_dict['city']:
            params_city = {
                'user_id': city,
                'share': int((share_line['city_share'] * service_pac_rec['cost']) / 10000),
                'withdraw_status': config.withdraw_status_no,
                'withdraw_type': config.zone_reward,
                # 分润类型，业务员还是店铺
                'buy_time': service_pac_rec['buy_time'],
                # 分润时间
                'withdraw_id': service_pac_rec['id'],
                # 对应的那条用户消费的id
            }
            Data.insert('withdraw_record', params_city)
            print('市代的分润', params_city['share'], city)

    if distr_dict['zone'] is not None:
        for zone in distr_dict['zone']:
            params_zone = {
                'user_id': zone,
                'share': int((share_line['zone_share'] * service_pac_rec['cost']) / 10000),
                'withdraw_status': config.withdraw_status_no,
                'withdraw_type': config.zone_reward,
                # 分润类型，业务员还是店铺
                'buy_time': service_pac_rec['buy_time'],
                # 分润时间
                'withdraw_id': service_pac_rec['id'],
                # 对应的那条用户消费的id
            }
            Data.insert('withdraw_record', params_zone)
            print('区代的分润', params_zone['share'], zone)

    # 省市区分代理润记录


def get_zone_distr_shop(shop_zone):
    distr_line = Data.select('zone_root', [('zone_code', '=', shop_zone)])
    if distr_line is None:
        return

    res = []
    for line in distr_line:
        res.append(line['user_id'])
    # zone_distr_id = distr_line['user_id']
    return res

    # 获取区域代理


def get_city_distr_shop(shop_zone):
    region = Data.find('region', [('code', '=', shop_zone)])
    city = region['parent_code']
    distr_line = Data.select('city_root', [('city_code', '=', city)])
    if distr_line is None:
        city_distr_id = None
    else:
        city_distr_id = []
        for line in distr_line:
            city_distr_id.append(line['user_id'])
    # city_distr_id 应该是一个列表

    region = Data.find('region', [('code', '=', city)])
    province = region['parent_code']
    distr_line = Data.find('province_root', [('province_code', '=', province)])
    if distr_line is None:
        province_distr_id = None
    else:
        province_distr_id = distr_line['user_id']

    return (city_distr_id, province_distr_id)
    # 找到省和市区的代理


def get_share_rate(shop_id):
    # 获取份额
    share_rec = Data.find('shop_share_type', [('shop_id', '=', shop_id)])
    share_line = Data.find('share_record', [('id', '=', share_rec['share_id'])])
    return share_line


def cal_share_distr(service_pac_rec, share_line):
    shop_id = service_pac_rec['buy_shop_id']
    # distr_line = find_distr_line([shop_id])
    # distr_line = distr_line[1:-1]
    # # 获取业务员链
    # if distr_line == []:
    #     return
    # else:
    res = Data.find('distr_relation', [('user_id', '=', shop_id)])
    if res is not None:
        distr_id = res['upper_id']
        insert_distr_share_info(distr_id, service_pac_rec, share_line)
        # 插入业务员链
    return


def find_distr_line(distr_id):
    # result = [distr_id]
    while 1:
        res = Data.find('distr_relation', [('user_id', '=', distr_id)])
        if res is None:
            return

        if res['is_super'] == 1:
            return res
        else:
            distr_id = res['upper_id']
            continue


def insert_distr_share_info(distr_id, service_pac_rec, share_line):
    # for distr_id in distr_line:
    res = find_distr_line(distr_id)
    if res is not None:
        # 超级业务员
        params = {
            'user_id': res['user_id'],
            'share': int((share_line['super_distr_share'] * service_pac_rec['cost']) / 10000),
            'withdraw_status': config.withdraw_status_no,
            'withdraw_type': config.spec_distr_share,
            # 分润类型，业务员还是店铺
            'buy_time': service_pac_rec['buy_time'],
            # 分润时间
            'withdraw_id': service_pac_rec['id'],
            # 对应的那条用户消费的id
        }
        Data.insert('withdraw_record', params)
        print('超级业务员的分润', params['share'], res['user_id'])
    # else:

    # 上一级业务员
    params = {
        'user_id': distr_id,
        'share': int((share_line['distr_share'] * service_pac_rec['cost']) / 10000),
        'withdraw_status': config.withdraw_status_no,
        'withdraw_type': config.distr_share,
        # 分润类型，业务员还是店铺
        'buy_time': service_pac_rec['buy_time'],
        # 分润时间
        'withdraw_id': service_pac_rec['id'],
        # 对应的那条用户消费的id
    }
    Data.insert('withdraw_record', params)
    print('业务员的分润', params['share'], distr_id)
    return


# =====================分润结束=============================


def return_pg(shop_id, service_info):
    total_pg = 0
    if_return = Data.select('shop_machines',
                            [('shop_id', '=', shop_id), ('paid_pg', '!=', 0), ('had_return_pg', '=', 0)])
    if if_return:
        for info in if_return:
            total_pg += info['paid_pg']

    machine_setting = Data.find('shop_machine_setting', [('shop_id', '=', shop_id)])

    if total_pg != 0:
        params = {
            'bought_rt_times': machine_setting['bought_rt_times'] + 1
        }
        Data.update('shop_machine_setting', [('shop_id', '=', shop_id)], params)
        machine_setting['bought_rt_times'] += 1
        # 保证金不等于的情况下才能统计次数

    # 获取当前可退质保金店铺的次数
    can_upgrade = Data.find('shop_distr', [('user_id', '=', shop_id)])['return_pg_times']

    return_pg_rec = Data.select('withdraw_record',
                                [('user_id', '=', shop_id), ('withdraw_type', '=', config.pg_return)])
    if return_pg_rec is None:
        length = 0
    else:
        length = len(return_pg_rec)
    # 记录返还过几次保证金
    #
    can_return_times = int(machine_setting['bought_rt_times'] / int(can_upgrade))

    if can_return_times > length:
        # can_return_pg = Data.select('shop_machines',
        #                             [('shop_id', '=', shop_id), ('paid_pg', '!=', 0), ('had_return_pg', '=', 0)])
        # if can_return_pg:
        Data.update('shop_machines', [('id', '=', int(if_return[0]['id']))], {'had_return_pg': 1})
        insert_return_pg_rec(shop_id, if_return[0]['paid_pg'], service_info['id'])


def can_return(machine_info, pg_once):
    if machine_info['addition_paid_pg'] < pg_once and machine_info['init_paid_pg'] < pg_once:
        print('鉴定失败')
        return False
    print('可以退钱')
    return True


def update_pg_status(pg_once, machine_info):
    if machine_info['init_paid_pg'] != 0:
        params = {
            'init_paid_pg': machine_info['init_paid_pg'] - pg_once,
            'init_return_pg': machine_info['init_return_pg'] + pg_once,
        }
    else:
        params = {
            'addition_paid_pg': machine_info['addition_paid_pg'] - pg_once,
            'addition_return_pg': machine_info['addition_return_pg'] + pg_once,
        }
    # 更新返还质保金的记录
    Data.update('shop_machines', [('id', '=', machine_info['id'])], params)


def add_agent_reward(shop_id, service_id):
    distr_info = Data.find('distr_relation', [('user_id', '=', shop_id)])
    if distr_info is not None:
        distr_id = distr_info['upper_id']
        if distr_id != 0:
            shop_machines = Data.select('shop_machines',
                                        [('shop_id', '=', shop_id), ('distr_reward', '=', 0), ('status', '=', 0)],
                                        order=('add_time', ''))
            print(shop_machines)
            print(shop_machines[0])
            if shop_machines[0]:
                if shop_machines[0]['paid_pg'] != 0:
                    params = {
                        'user_id': distr_id,
                        'share': 50000,
                        'withdraw_status': config.withdraw_status_no,
                        'withdraw_type': config.distr_reward,
                        'buy_time': int(time.time()),
                        'withdraw_id': service_id,
                    }
                    Data.insert('withdraw_record', params)
                Data.update('shop_machines', [('id', '=', shop_machines[0]['id'])], {'status': 1, 'distr_reward': 1})
    # 插入奖励业务员的记录


def insert_return_pg_rec(shop_id, pg_once, service_id):
    params = {
        'user_id': shop_id,
        'share': pg_once,
        'withdraw_status': config.withdraw_status_no,
        'withdraw_type': config.pg_return,
        'buy_time': int(time.time()),
        'withdraw_id': service_id,
    }

    Data.insert('withdraw_record', params)
    # 插入退回保证金的记录
