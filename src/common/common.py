import datetime
import time
import pymysql
import config
import hashlib
from data.server import Data
from gevent import getcurrent
from math import radians, sin, cos, asin, sqrt
import random
import os,sys

rand_string = 'qwertyuiopasdfghjklzxcvbnm1234567890'


# 时间戳转2018-01-01 8:00:00
def time_to_str(times=time.time()):
    if times == 0:
        return '2019-09-24 00:00:00'
    date_array = datetime.datetime.utcfromtimestamp(times + (8 * 3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")


def str_to_time(time_str):
    timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(timeArray))
    return time_stamp


# 相反
def create_rand_string(length):
    code = ''
    for i in range(0, length):
        code += random.choice(rand_string)
    return code

def get_md5(string):
    md5 = hashlib.md5(string.encode('ascii')).hexdigest()
    return md5
    # 计算md5校验
    # 这里python作为一个弱类型语言的坑就出现了
    # 竟然传入值需要解码成ascii


def get_file_md5(binary):
    '''
    文件md5转换
    :param binary: 
    :return: 
    '''
    md5 = hashlib.md5(binary).hexdigest()
    return md5


def get_event_id():
    id_string = str(id(getcurrent()))
    res = ''
    for i in range(0,len(rand_string)):
        res += random.choice(rand_string)

    res += id_string
    res += str(time.time())
    return get_md5(res)
    # 获得事件id编码


def create_invite_code(table_tail=''):
    # 创建邀请码
    res = Data.select('invite_code' + table_tail, [('id', '!=', 0)])
    inv_code_list = []
    if res is not None:
        for line in res:
            inv_code_list.append(line['inv_code'])

    while 1:
        code = create_rand_string(8)
        if code not in inv_code_list:
            return code


def create_verify_code(table_tail=''):
    all_code = list(range(100000, 1000000))

    res_1 = Data.select('tel_verify' + table_tail, [('id', '!=', 0), ('status', '=', 0)])
    res = []
    if res_1 is not None:
        for i in res:
            all_code.remove(int(i['code']))

    return str(random.choice(all_code))


# 计算两点之间的距离,LBS 球面距离公式
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，单位为公里
    dis = int(dis)
    return dis
    # 返回单位为米


def create_invite_code_player():
    # 创建邀请码
    res = Data.select('invite_code_player', [('id', '!=', 0)])
    inv_code_list = []
    if res is not None:
        for line in res:
            inv_code_list.append(line['inv_code'])


    while 1:
        code = create_rand_string(8)
        if code not in inv_code_list:
            return code



def create_coupon_num():
    res = Data.select('coupon_main',[('id', '!=', 0)])
    num_list = []
    if res is not None:
        for line in res:
            num_list.append(line['c_number'])

    while 1:
        code = create_rand_string(12)
        if code not in num_list:
            return code

def create_son_cnum(coupon_id):
    main_number = Data.find('coupon_main',[('id','=',coupon_id)])['c_number']
    res = Data.select('coupon_player',[('coupon_id', '=', coupon_id)])
    num_list = []
    if res is not None:
        for line in res:
            num_list.append(line['coupon_num'])

    while 1:
        code = create_rand_string(8)
        if main_number+code not in num_list:
            return main_number+code

def dbg(*args):
    info = ''
    for i in args:
        info += str(i)
        info += ' '
    print(*args)
    logging('dev.log', info)

def logging(file, info):
    info = '[' + time_to_str(int(time.time())) + '-' + str(int(time.time())) + ']' + info + '\n'
    # print(info)
    open(file, 'a').write(info)



