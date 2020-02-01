import time
from tornado.concurrent import run_on_executor
from werkzeug.security import generate_password_hash
from common import common
from common.common import str_to_time
from data.server import Data
from error import error
from app.http.handler_base import HandlerBase
from app.http.mods.admin.admin_tools import write_admin_record


# 获取管理员列表
class get_admin_list(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_admin_list')

        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            username = data['username']
            start_time = data['start_time']
            end_time = data['end_time']
            status = data['status']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if username == '':
            username = "%"
        if start_time != '':
            start_time += ' 00:00:00'
            start_time = str_to_time(start_time)
        else:
            start_time = 0
        if end_time != '':
            end_time += ' 00:00:00'
            end_time = str_to_time(end_time)
        else:
            end_time = int(time.time())

        god_info = Data.select('admin', [('username', 'like', '%{}%'.format(username))])

        admins = []
        for item in god_info:
            params = {}
            admin_data = Data.find('admin_auth', [('god_id', '=', item['id'])])
            if admin_data:
                if start_time <= str_to_time(item['ctime']) <= end_time:
                    if status == item['status']:
                        params['admin_id'] = item['admin_id']
                        params['username'] = item['username']
                        params['ctime'] = str(item['ctime'])
                        params['status'] = item['status']
                        params['temp_id'] = admin_data['auth_id']
                        temp_data = Data.find('admin_temp', [('id', '=', admin_data['auth_id']), ('status', '=', 0)])
                        if temp_data:
                            params['temp_name'] = temp_data['name']
                        else:
                            params['temp_name'] = '无权限'
                        admins.append(params)

        result = {
            'admin_list': admins
        }

        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='获取管理员列表')

        return


# 获取管理员详情
class get_admin_detail(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_admin_detail')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            admin_id = data['admin_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        admin_info = Data.find('admin_auth', [('god_id', '=', admin_id)])
        if admin_info is None:
            return self.send_faild(error.ERROR_NO_USER)

        god_info = Data.find('admin', [('id', '=', admin_info['god_id'])])
        if god_info is None:
            return self.send_faild(error.ERROR_NO_USER)
        admin = {
            'username': god_info['username'],
            'status': god_info['status'],
            'ctime': god_info['ctime'],
            'admin_temp_id': admin_info['auth_id']
        }

        result = {
            'admin_info':admin
        }

        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='获取管理员详情', admin_id=admin_id)

        return


# 添加管理员
class add_admin(HandlerBase):
    @run_on_executor
    def post(self):
        print('add_admin')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            username = data['username']
            pw = data['pswd']
            status = data['status']
            auth_temp = data['admin_temp_id']
            comment = data['comment']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if_user = Data.find('admin', [('username', '=', username)])
        if if_user is not None:
            return self.send_faild(error.ERROR_INSERT_USER)

        admin_params = {
            'username': username,
            'password_hash': generate_password_hash(pw),
            'status': status,
            'comment': comment,
            'ctime': common.time_to_str(int(time.time())),
            'auth_id': auth_temp,
        }

        Data.insert('admin', admin_params)
        new_admin_info = Data.find('admin', [('username', '=', username)])
        if new_admin_info is None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)
        admin_id = new_admin_info['id']

        admin_auth_info = {
            'auth_id': auth_temp,
            'god_id': admin_id
        }
        Data.insert('admin_auth', admin_auth_info)
        result = {
            'commit': 1
        }
        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='添加管理员', admin_id=admin_id)
        return


# 更新管理员详情
class update_admin_detail(HandlerBase):
    @run_on_executor
    def post(self):
        print('update_admin_detail')

        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            admin_id = data['admin_id']
            status = data['status']
            auth_temp = data['admin_temp_id']
            comment = data['comment']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if admin_id == 1:
            print('初始账号不能改信息')
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        admin_info = Data.find('admin_auth', [('admin_id', '=', admin_id)])
        if admin_info is None:
            return self.send_faild(error.ERROR_NO_USER)

        god_info = Data.find('admin', [('id', '=', admin_id)])
        if god_info is None:
            return self.send_faild(error.ERROR_NO_USER)

        # 更新模板
        Data.update('admin_auth', [('id', '=', admin_id)], {'auth_id': auth_temp})

        god_info = {
            'utime': common.time_to_str(int(time.time())),
            'status': status,
            'comment': comment
        }

        try:
            Data.update('admin', [('id', '=', admin_id)], god_info)
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_TIMEOUT)

        result = {
            'commit': 1
        }
        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='更新管理员详情', admin_id=admin_id)
        return


# 禁用/启用管理员
class delete_admin(HandlerBase):
    @run_on_executor
    def post(self):
        print('delete_admin')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            admin_id = data['admin_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        admin_info = Data.find('admin_auth', [('id', '=', admin_id)])
        if admin_info is None:
            return self.send_faild(error.ERROR_NO_USER)

        god_info = Data.find('admin', [('id', '=', admin_info['god_id'])])
        if god_info['status'] == 0:
            params = {
                'utime': common.time_to_str(int(time.time())),
                'status': 1,
            }
            Data.update('admin', [('id', '=', admin_info['god_id'])], params)
        else:
            params = {
                'utime': common.time_to_str(int(time.time())),
                'status': 0,
            }
            Data.update('admin', [('id', '=', admin_info['god_id'])], params)

        result = {
            'commit': 1
        }
        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='禁用/启用管理员', admin_id=admin_id)
        return
