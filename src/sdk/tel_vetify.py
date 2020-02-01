import json, time, hashlib, random, string
from datetime import datetime
import requests
import urllib.parse
import urllib.request
from config import config
from common import common
from data.server import Data

tel_verify = config.tel_verify




def send_inv_code(code, tel):
    info = '' + code + ''
    return send_info(info, tel)


def send_normal_msg(msg, tel):
    info = msg
    return send_info(info, tel)


def send_info(info, tel):
    # return 0
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    encode = 'UTF-8'
    url = tel_verify[
        'url']  # 如连接超时，可能是您服务器不支持域名解析，请将下面连接中的：【m.5c.com.cn】修改为IP：【115.28.23.78】                                   #页面编码和短信内容编码为GBK。重要说明：如提交短信后收到乱码，请将GBK改为UTF-8测试。如本程序页面为编码格式为：ASCII/GB2312/GBK则该处为GBK。如本页面编码为UTF-8或需要支持繁体，阿拉伯文等Unicode，请将此处写为：UTF-8
    username = tel_verify['username']  # 用户名
    password_md5 = common.get_md5(tel_verify['pw'])  # 32位MD5密码加密，不区分大小写
    apikey = tel_verify['api_key']  # apikey秘钥（请登录 http://m.5c.com.cn 短信平台-->账号管理-->我的信息 中复制apikey）
    mobile = tel  # 手机号,只发一个号码：13800000001。发多个号码：13800000001,13800000002,...N 。使用半角逗号分隔。
    content = info  # 要发送的短信内容，特别注意：签名必须设置，网页验证码应用需要加添加【图形识别码】。
    values = {'username': username,
              'password_md5': password_md5,
              'apikey': apikey,
              'mobile': mobile,
              'content': content,
              'encode': encode}
    headers = {'User-Agent': user_agent}
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url + '?' + data)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    res = the_page.decode('utf-8').split(':')[0]
    print(res)
    if res == 'success':
        return 0
    else:
        return -1


def buy_dev(dev_num, tel):
    phone_list = [
        '13806075825',
        '13376923027',
        '17850503194',
        '13600965785',
        '18359114760',
        '15305043166',
    ]
    shop_info = Data.find('openluat_user', [('phone', '=', tel)])
    address = shop_info['address']
    name = shop_info['realname']

    zone_root = Data.find('zone_root', [('zone_code', '=', shop_info['zone_code'])])
    if zone_root != None:
        phone_list.append(Data.find('openluat_user', [('id', '=', zone_root['user_id'])])['phone'])

    city_code = Data.find('region', [('code', '=', shop_info['zone_code'])])['parent_code']
    city_root = Data.find('city_root', [('city_code', '=', city_code)])
    if city_root != None:
        phone_list.append(Data.find('openluat_user', [('id', '=', city_root['user_id'])])['phone'])

    info = '' + str(dev_num) + ''+name + tel + '' + address
    for i in phone_list:
        send_info(info, i)
