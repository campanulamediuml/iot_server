from urllib import request
from urllib import parse
import time
import json
import random
import requests
import string
from config import wechat_config
from config.wechat_config import WST
from data.server import Data
from common import common
import hashlib
import xmltodict

# from data.server import Data
TableFirstKey_WX_WEB = 100
AdvanceRefreshTime = 300


def get_split_joint_by_case_sensitivity(dct):
    return '&'.join(['%s=%s' % (key, dct[key]) for key in sorted(dct)])


def getxml(kwargs):
    xml = ''
    for key, value in kwargs.items():
        xml += '<{0}>{1}</{0}>'.format(key, value)
    xml = '<xml>{0}</xml>'.format(xml)

    return xml


def get_pay_sign(dct):
    s = get_split_joint_by_case_sensitivity(dct) + '&key=' + WST.WECHAT_MCH_KEY
    print(s)
    sign = hashlib.md5(s.encode("utf8")).hexdigest().upper()
    print(sign)
    return sign


def get_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def get_unifiedorder(remote_ip, openid, gooddesc, money, out_trade_no, buyer=None):
    # money *= 100
    # 测试
    # money = 1
    # 微信浏览器：公众号支付
    trade_type = 'JSAPI'
    appid = WST.APP_ID

    unifieOrderRequest = {
        'appid': appid,  # 公众账号ID
        'body': wechat_config.PAY_GOODDESC + '-' + gooddesc,  # 商品描述
        'mch_id': WST.WECHAT_MCH_ID,  # 商户号
        'nonce_str': get_nonce_str(),  # 随机字符串
        'notify_url': WST.REDIRECT_URI,  # 微信支付结果异步通知地址
        # 'openid': openid,  # trade_type为JSAPI时，openid为必填参数！此参数为微信用户在商户对应appid下的唯一标识, 统一支付接口中，缺少必填参数openid！
        'out_trade_no': out_trade_no,  # 商户订单号
        'sign_type': 'MD5',
        'spbill_create_ip': remote_ip,  # 终端IP
        'total_fee': int(money),  # 标价金额
        'trade_type': trade_type,  # 交易类型
        # 'attach': 'attach_test',  # 附加数据，在查询API和支付通知中原样返回，可作为自定义参数使用。
    }

    if buyer is not None:
        unifieOrderRequest['notify_url'] = WST.PLAYER_PAY_REDIRECT

    unifieOrderRequest['openid'] = openid

    url = wechat_config.PAY_URL + 'unifiedorder'
    res = get_value_by_url_pay_secret(url, unifieOrderRequest)
    return res


def get_value_by_url_pay_secret(url, data):
    data['sign'] = get_pay_sign(data)
    data = getxml(data)
    # print(data)
    # 33333333333333
    resp = requests.post(url, data.encode('utf-8'),
                         headers={'Content-Type': 'text/xml'})

    readDct = resp.text.encode('ISO-8859-1').decode('utf-8')

    return xmltodict.parse(readDct)['xml']


def get_timestamp():
    return int(time.time())


def get_pay_sign_return_dct(odDict):
    retDct = {
        'appId': WST.APP_ID,
        'timeStamp': str(get_timestamp()),
        'nonceStr': get_nonce_str(),
        'package': 'prepay_id=' + odDict['prepay_id'],
        'signType': 'MD5'
    }

    retDct['paySign'] = get_pay_sign(retDct)

    return retDct


def get_pay_sign_dummy(odDict):
    retDct = {
        'appid': WST.APP_ID,
        'partnerid': WST.WECHAT_MCH_ID,
        'prepayid': odDict['prepay_id'],
        'package': 'Sign=WXPay',
        'nonceStr': get_nonce_str(),
        'timeStamp': str(get_timestamp()),
    }
    retDct['paySign'] = get_pay_sign(retDct)

    return retDct


def wechat_login(code):
    readDct = get_access_token(code)
    if not readDct or 'errcode' in readDct:
        print('err wx_login readDct %s' % readDct)
        return

    access_token = readDct['access_token']
    # expires_in = readDct['expires_in']
    # refresh_token = readDct['refresh_token']
    openid = readDct['openid']
    scope = readDct['scope']

    if scope != 'snsapi_userinfo' and scope != 'snsapi_login':
        print('err wx_login scope readDct %s' % readDct)
        return

    res = wx_get_userinfo(access_token, openid)
    return res


def get_args_str(args):
    argStr = ''
    for p, v in args.items():
        argStr = argStr + p + '=' + str(v) + '&'

    argStr = argStr[:-1]

    return argStr


def get_access_token_by_code(code):
    readDct = get_access_token(code)
    # return readDct['openid']
    if not readDct or 'errcode' in readDct:
        print('err wx_login readDct %s' % readDct)
        return

    # return readDct['openid']

    access_token = readDct['access_token']
    expires_in = readDct['expires_in']
    refresh_token = readDct['refresh_token']
    openid = readDct['openid']
    scope = readDct['scope']

    return readDct


def get_open_id_by_code(code):
    # readDct = get_access_token(code)
    readDct = get_access_token(code)

    if not readDct or 'errcode' in readDct:
        print('err wx_login readDct %s' % readDct)
        return

    return readDct['openid']


def get_access_token(code):
    if code is None:
        now = get_timestamp()
        dct = _get_wx_db_dct(TableFirstKey_WX_WEB)
        if dct and dct['create_time'] and now < dct['create_time']:
            return dct['auth_token']

        url = wechat_config.API_URL + 'cgi-bin/token'
        args = {
            'grant_type': 'client_credential',
            'appid': WST.APP_ID,
            'secret': WST.APP_SECRET,
        }

        dct = get_value_by_url(url, args)
        if 'access_token' not in dct:
            print('get_access_token err %s' % dct)
            return None

        update_db(TableFirstKey_WX_WEB, auth_token=dct['access_token'],
                  create_time=dct['expires_in'] + now - AdvanceRefreshTime)

        return dct['access_token']

    url = wechat_config.API_URL + 'sns/oauth2/access_token'
    args = {
        'appid': WST.APP_ID,
        'secret': WST.APP_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    return get_value_by_url(url, args)


def get_value_by_url(url, args):
    time_1 = int(time.time())

    url = url + '?' + get_args_str(args)

    response = request.urlopen(url)
    readDct = response.read().decode('utf-8')

    print('get_value_by_url %s %s %s' % (url, args, readDct))

    time_2 = int(time.time())

    print(time_2 - time_1, '打开微信的url花的时间')

    return json.loads(readDct)


def wx_get_userinfo(access_token, openid):
    readDct = get_userinfo_by_web(access_token, openid)

    print('wx_get_userinfo----%s' % readDct)
    if 'errcode' in readDct:
        print('err wx_get_userinfo readDct %s' % readDct)
        return

    nickname = readDct['nickname'].replace('"','')
    nickname = nickname.replace("'","")
    sex = readDct['sex']
    iconUrl = readDct['headimgurl']
    openid = readDct['openid']

    if int(sex) == 2:
        sex = 1
    else:
        sex = 0

    login_status = update_user(nickname, sex, iconUrl, openid)
    return login_status


def update_user(nickname, sex, iconUrl, openid, unionid=''):
    params = {
        'nickname': json.dumps(nickname).replace('\\', '\\\\'),
        'sex': sex,
        'avatar': iconUrl,
        'open_id': openid,
        'union_id': unionid,
    }

    res = Data.find('player', [('open_id', '=', openid)])
    if res is None:
        params['join_time'] = int(time.time())
        Data.insert('player', params)
    else:
        Data.update('player', [('open_id', '=', openid)], params)

    # token = admin_common.get_md5(openid + unionid + str(int(time.time())))
    # Data.update('player', [('open_id', '=', openid)], {'token': token})
    # 插入token

    # print(token)
    res = Data.find('player', [('open_id', '=', openid)])
    print('user_info_in_table----', res)

    return res


def get_userinfo_by_web(access_token, openid):
    url = WST.API_URL + 'sns/userinfo'
    args = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN',
    }

    return get_value_by_url(url, args)


def __getCfg(jsapi_ticket, url):
    # 其中jsapi_ticket需要通过
    # http: // api.weixin.qq.com / cgi - bin / ticket / getticket?type = jsapi & access_token = ACCESS_TOKEN
    # 接口获取，url 为调用页面的完整 url 。
    # 但要注意如果已有其他业务需要使用access_token的话，应修改获取
    # access_token部分代码从全局缓存中获取，防止重复获取access_token ，超过调用频率。
    #
    # 注意事项：
    # 1.jsapi_ticket的有效期为7200秒，开发者必须全局缓存jsapi_ticket ，防止超过调用频率。
    return {
        'jsapi_ticket': jsapi_ticket,
        'nonceStr': get_nonce_str(),
        'timestamp': get_timestamp(),
        'url': url,
    }


def sign_wechat(url):
    jsapi_ticket = get_jsapi_ticket()
    cfg = __getCfg(jsapi_ticket, url)
    cfg['signature'] = sign_md5(cfg)
    return cfg


def sign_md5(cfg):
    s = '&'.join(['%s=%s' % (key.lower(), cfg[key]) for key in sorted(cfg)])
    print(s)

    res = hashlib.sha1(s.encode("utf8")).hexdigest()
    print(res)
    return res


def get_jsapi_ticket():
    now = get_timestamp()
    dct = _get_wx_db_dct(TableFirstKey_WX_WEB)
    if dct and dct['sign_time'] and now < dct['sign_time']:
        return dct['wechat_sign']

    url = wechat_config.API_URL + 'cgi-bin/ticket/getticket'
    access_token = get_access_token(None)

    args = {
        'access_token': access_token,
        'type': 'jsapi',
    }
    dct = get_value_by_url(url, args)
    if dct['errcode'] != 0:
        print('err get_jsapi_ticket %s %s' % (url, args))
        return ''
    update_db(TableFirstKey_WX_WEB, wechat_sign=dct['ticket'],
              sign_time=dct['expires_in'] + now - AdvanceRefreshTime)

    return dct['ticket']


def _get_wx_db_dct(id):
    conditions = [('id', '=', id)]
    res = Data.find('wechat_auth_table', conditions)
    return res


def update_db(id, auth_token=None, refresh_token=None, create_time=None,
              wechat_sign=None, sign_time=None):
    if not _get_wx_db_dct(id):
        Data.insert('wechat_auth_table', {'id': id})

    conditions = [('id', '=', id)]

    params = {}

    if auth_token:
        if not create_time:
            print('err update_db not refresh_token or not create_time ')
            return

        params['auth_token'] = auth_token
        params['create_time'] = create_time

    if wechat_sign:
        if not sign_time:
            print('err update_db not sign_time ')
            return

        params['wechat_sign'] = wechat_sign
        params['sign_time'] = sign_time

    if not params:
        print('err update_db not sign_time not auth_token or not wechat_sign')
        return

    res = Data.update('wechat_auth_table', conditions, params)
    return res
