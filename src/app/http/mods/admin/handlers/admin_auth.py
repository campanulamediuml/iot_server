import time
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from app.http.mods.admin.admin_tools import write_admin_record
from common.common import str_to_time, time_to_str
from data.server import Data
from error import error
from common import common


# 获取权限模板列表
class get_auth_template_list(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_auth_template')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        data = self.get_post_data()
        try:
            admin_temp_name = data['admin_temp_name']
            start_time = data['start_time']
            end_time = data['end_time']
            status = data['status']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if admin_temp_name == '':
            admin_temp_name = "%"
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

        res = Data.select('admin_temp', [('name', 'like', '%{}%'.format(admin_temp_name)), ('status', '=', 0)])
        admin_temp_list = []

        if res:
            for temp in res:
                if start_time <= int(temp['ctime']) <= end_time:
                    if status == temp['status']:
                        temp['ctime'] = time_to_str(int(temp['ctime']))
                        admin_temp_list.append(temp)

        result = {
            'auth_temp_list': admin_temp_list
        }
        self.send_ok(result)

        return


# 创建权限模板
class create_auth_template(HandlerBase):
    @run_on_executor
    def post(self):
        print('create_auth_template')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            name =data['name']
            auth = data['auth']
            comment = data['comment']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        params = {}
        params['name'] = name
        params['auth'] = auth
        params['comment'] = comment
        params['ctime'] = int(time.time())
        Data.insert('admin_temp', params)

        # 记录本条权限模板的id
        temp_info = Data.find_last('admin_temp', [('id', '!=', 0)], info='id', limit=1)

        result = {
            'commit': 1
        }

        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='创建权限模板', temp_id=temp_info['id'])
        return


# 修改权限模板
class update_auth_template(HandlerBase):
    @run_on_executor
    def post(self):
        print('update_auth_template')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            temp_id = data['temp_id']
            name = data['name']
            auth = data['auth']
            comment = data['comment']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        params = {}
        params['name'] = name
        params['auth'] = auth
        params['comment'] = comment
        params['utime'] = int(time.time())

        Data.update('admin_temp', [('id', '=', temp_id)], params)

        result = {
            'commit': 1
        }

        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='修改权限模板', temp_id=data['temp_id'])
        return


# 查看权限模板
class get_auth_template(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_auth_template')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)

        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            temp_id = data['temp_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        res = Data.find('admin_temp', [('id', '=', temp_id)])
        if res is None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)

        temp = {
            'temp_name': res['name'],
            'temp_auth': res['auth'],
            'comment': res['comment']
        }


        result = {
            'temp_info':temp
        }

        self.send_ok(result)
        return


# 删除权限模板
class delete_auth_template(HandlerBase):
    @run_on_executor
    def post(self):
        print('delete_auth_template')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if self.is_god() is False:
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            temp_id = data['temp_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        res = Data.find('admin_temp', [('id', '=', temp_id)])
        if res is None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)

        Data.update('admin_temp', [('id', '=', temp_id)], {'status': 1})

        result = {
            'commit': 1
        }

        self.send_ok(result)

        write_admin_record(operate_id=admin_base['id'], operate_desc='删除权限模板', temp_id=data['temp_id'])
        return
