import random
import time
from tornado.escape import json_decode
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor

from common import common
from common.common import get_md5
from data.server import Data
from error import error
from app.http.relay.relay import Relay
from config.config import thread_pool_num
import json


class HandlerBase(RequestHandler):
    executor = ThreadPoolExecutor(thread_pool_num)
    def set_default_headers(self):
        origin = self.request.headers.get('Origin')
        if origin == None:
            origin = '*'

        print('添加响应标头')
        self.set_header('Access-Control-Allow-Origin',origin)
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With,Origin,Content-Type')
        self.set_header('Server', 'eyewave-server/v2.0')


    def options(self):
        print('<---------收到跨域请求，返回空值--------->')
        # self.set_default_headers()
        return self.write({})

    def get_result(self):
        '''
        返回结构基本模板
        :return:
        '''
        result = {}
        result['code'] = 0
        result['msg'] = ''
        result['data'] = {}
        return result

    def get_user_base(self, user_id):
        return Data.find('admin', [('id', '=', user_id)])


    def get_admin_base(self):
        '''
        获取用户基本信息
        :return:
        '''
        # self.token_time_out()
        token = self.get_argument('token')
        if token == '' or token is None:
            print('没有携带token')
            return

        res = Relay.get_admin_base(token)
        return res

    def get_player_base(self):
        '''
        获取用户基本信息
        :return:
        '''
        # self.token_time_out()
        token = self.get_argument('token')
        if token == '' or token is None:
            print('没有携带token')
            return

        res = Relay.get_player_base(token)
        # Relay.update_token(token)
        return res

    def is_god(self):
        '''
        获取用户基本信息
        :return:
        '''
        token = self.get_argument('token')
        if token == '' or token is None:
            print('没有携带token')
            return
        res = Relay.is_god(token)
        return res

    def player_logout(self):
        '''
        获取post请求内容
        :return:
        '''
        token = self.get_argument('token')
        if token == '' or token is None:
            print('没有携带token')
            return
        res = Relay.player_logout(token)
        return res

    def admin_logout(self):
        '''
        获取post请求内容
        :return:
        '''
        token = self.get_argument('token')
        if token == '' or token is None:
            print('没有携带token')
            return
        res = Relay.admin_logout(token)
        return res

    def send_ok(self, data={}):
        """
        正确信息返回
        :param data:
        :return:
        """
        result = self.get_result()
        result['data'] = data
        print('<---------请求成功，返回值--------->')
        if len(json.dumps(data))>10240:
            print()
        else:
            print(result)
        # 打印日志
        # self.set_default_headers()
        self.write(result)

    def send_faild(self, code):
        '''
        失败信息返回
        :param code:
        :return:
        '''
        result = self.get_result()
        unit = error.error_info[code]
        result['code'] = code
        result['msg'] = unit[0]
        print('<---------请求失败，返回值--------->')
        print(result)
        # self.set_default_headers()
        self.write(json.dumps(result))

    def get_data(self):
        '''
        获取get请求内容
        :return:
        '''
        data = self.get_argument('data')
        if data is None:
            print('没有收到get参数')
            return data
        res = json.loads(data)
        print(data)
        return res

    def get_files(self, key):
        if key in self.request.files:
            file_metas = self.request.files[key][0]['body']
            return file_metas

        else:
            return None

    def get_post_data(self):
        '''
        获取post请求内容
        :return:
        '''
        # if len(self.request.body) < 1024:
        #     print(self.request.body)
        data = json_decode(self.request.body)
        if len(self.request.body) < 1024:
            print(self.request.body)
            print('收到post数据', data)
            # res = json.loads(data)
        return data

    def create_token(self, user_id, table_name):
        '''
        创建token
        :param user_id:
        :param table_name:
        :return:
        '''
        nonce_string = common.create_rand_string(12)+str(time.time())
        token = get_md5(nonce_string)
        params = {
            'token': token
        }
        Data.update(table_name, [('id', '=', user_id)], params)
        if table_name == 'admin':
            Relay.admin_login(user_id,token)
        if table_name == 'player':
            Relay.player_login(user_id,token)
        return token

    def create_code(self):
        all_code = list(range(100000, 1000000))

        res_1 = Data.select('tel_verify', [('id', '!=', 0), ('status', '=', 0)])
        res = []
        if res_1 is not None:
            for i in res:
                all_code.remove(int(i['code']))

        return str(random.choice(all_code))
