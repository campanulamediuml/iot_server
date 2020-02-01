import base64
import json
import time
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from app.http.mods.admin import admin_tools
from common import common
from common.common import str_to_time
from config import config
from data.server import Data
from error import error
from app.http.mods.admin.admin_tools import write_admin_record


# 广告列表
class get_adv_list(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_adv_list')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_name = data['adv_name']
            postion = data['postion']
            start_time = data['start_time']
            end_time = data['end_time']
            status = data['status']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        if adv_name == '':
            adv_name = "%"
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

        adv = []
        adv_list = Data.select('adv', [('adv_name', 'like', '%{}%'.format(adv_name))],
                               order=('add_time', 'desc'))

        if adv_list:
            for ad in adv_list:
                if start_time <= int(ad['add_time']) <= end_time:
                    params = {}
                    params['adv_name'] = ad['adv_name']
                    params['postion'] = ad['postion']
                    params['img'] = ad['img']
                    params['url'] = ad['url']
                    params['ctime'] = ad['ctime']
                    params['comment'] = ad['comment']
                    params['status'] = ad['status']
                    adv.append(params)

        res = []
        if adv:
            for i in adv:
                if i == None:
                    continue
                if postion != '':
                    if postion in i['postion']:
                        res.append(i)
                else:
                    res.append(i)

        res1 = []
        for i in res:
            if int(status) == i['status']:
                res1.append(i)

        result = {
            'adv_info_list': res1
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='广告列表')

        return


# 广告详细信息
class get_adv_info(HandlerBase):
    @run_on_executor
    def post(self):
        print('get_adv_info')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_id = data['adv_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)
        adv = Data.find('adv', [('id', '=', adv_id)])
        adv_info = {}
        if adv:
            adv_info['adv_name'] = adv['adv_name']
            adv_info['postion'] = adv['postion']
            adv_info['url'] = adv['url']
            adv_info['ctime'] = adv['ctime']
            adv_info['comment'] = adv['comment']
            adv_info['status'] = adv['status']
            img = Data.find('adv_photo', [('adv_id', '=', adv_id)])
            adv_info['img'] = img['photo_url']

        result = {
            'adv_info': adv_info
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='广告详细信息', adv_id=adv_id)

        return


# 添加广告
class add_adv(HandlerBase):
    @run_on_executor
    def post(self):
        print('add_adv')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_name = data['adv_name']
            postion = data['postion']
            url = data['url']
            comment = data['comment']
            status = data['status']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        ctime = int(time.time())

        adv_info = {}
        adv_info['adv_name'] = adv_name
        adv_info['postion'] = postion
        adv_info['ctime'] = ctime
        adv_info['comment'] = comment
        adv_info['status'] = status

        Data.insert('adv', adv_info)
        adv = Data.find_last('adv', [('id', '!=', 0)], info='id', limit=1)
        result = {
            'commit': 1
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='新增广告', adv_id=adv['id'])

        return


class send_advphoto(HandlerBase):
    @run_on_executor
    # 上传广告图片
    def post(self):
        print('send_advphoto')
        admin_base = self.get_admin_base()
        if admin_base is None:
            self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_id = data['adv_id']
            pic_body = data['title']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        adv_info = Data.find('adv', [('id', '=', adv_id)])
        if adv_info is None:
            return self.send_faild(error.ERROR_NO_USER)

        adv_id = adv_info['id']

        img_data = pic_body.split(',')[1]

        img_data = base64.b64decode(img_data)
        path = 'pics/' + common.get_file_md5(img_data) + '_title' + '.jpg'

        open(path, 'wb').write(img_data)

        title_line = Data.find('adv_photo', [('adv_id', '=', adv_id), ('is_title', '=', 1)])

        if title_line is None:
            params = {
                'adv_id': adv_id,
                'photo_url': config.logical_url + '/' + path.split('/')[-1],
            }
            Data.insert('adv_photo', params)
        else:
            params = {
                'photo_url': config.logical_url + '/' + path.split('/')[-1],
            }
            Data.update('adv_photo', [('adv_id', '=', adv_id)], params)
            # 记录进数据库

        reply = {
            'pic_done': 0
        }
        self.send_ok(reply)
        write_admin_record(operate_id=admin_base['id'], operate_desc='上传广告图片', adv_id=adv_id)

        return




# 修改广告
class update_adv(HandlerBase):
    @run_on_executor
    def post(self):
        print('update_adv')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_id = data['adv_id']
            adv_name = data['adv_name']
            postion = data['postion']
            url = data['url']
            comment = data['comment']
            status = data['status']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)

        adv_info = {}
        adv_info['adv_name'] = adv_name
        adv_info['postion'] = postion

        adv_info['utime'] = int(time.time())
        adv_info['comment'] = comment
        adv_info['status'] = status

        Data.update('adv', [('id', '=', adv_id)], adv_info)
        result = {
            'commit': 1
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='修改广告', adv_id=adv_id)

        return


# 删除广告
class del_adv(HandlerBase):
    @run_on_executor
    def post(self):
        print('del_adv')
        admin_base = self.get_admin_base()
        if admin_base is None:
            return self.send_faild(error.ERROR_NO_LOGIN)
        if not self.is_god():
            return self.send_faild(error.ERROR_AUTH_PERMISSION)

        try:
            data = self.get_post_data()
            adv_id = data['adv_id']
        except Exception as e:
            print(e)
            return self.send_faild(error.ERROR_PARAM)
        info = Data.find('adv', [('id', '=', adv_id)])
        if info is None:
            return self.send_faild(error.ERROR_DATA_NOT_FOUND)

        if info['status'] == 0:
            status = 1
        else:
            status = 0

        Data.update('adv', [('id', '=', adv_id)], {'status': status})
        result = {
            'commit': 1
        }
        self.send_ok(result)
        write_admin_record(operate_id=admin_base['id'], operate_desc='启用/禁用广告', adv_id=adv_id)

        return
