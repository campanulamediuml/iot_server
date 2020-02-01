import time

from werkzeug.security import generate_password_hash

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from common import common
from config.config import VERIFY_CODE
from data.server import Data
from error import error
from sdk import tel_vetify


class sign_in(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            inv_code = data['inv_code']
            phone = data['phone']
            passwd = data['passwd']
            passwd_confirm = data['passwd_confirm']
            verify_code = data['verify_code']
            name = data['name']
        except Exception as e:
            print(e)
            print('有没填的信息')
            return self.send_faild(error.ERROR_PARAM)

        if inv_code == '':
            print('没有邀请码')
            return self.send_faild(error.ERROR_PARAM)
        # 没有邀请码拒绝注册
        if VERIFY_CODE != '1234':
            res = Data.find('tel_verify', [('tel', '=', phone), ('code', '=', verify_code), ('status', '=', 0)])
            if res is None:
                return self.send_faild(error.ERROR_CODE_WRONG)
                # 验证码错误
            if int(time.time()) - res['c_time'] > 600:
                return self.send_faild(error.ERROR_CODE_WRONG)
                # 验证超时，十分钟

            # 验证失败
            Data.update('tel_verify', [('tel', '=', phone), ('code', '=', verify_code)], {'status': 1})

        res = Data.find('openluat_user', [('phone', '=', phone)])
        if res is not None:
            return self.send_faild(error.ERROR_PHONE_EXISTS)
        # 账号已经存在

        inv_info = Data.find('invite_code', [('inv_code', '=', inv_code)])
        if inv_info is None:
            print('邀请码不存在')
            return self.send_faild(error.ERROR_PARAM)
        # 邀请码不存在

        if passwd != passwd_confirm:
            return self.send_faild(error.ERROR_PW_DIFF)
        # 密码不同

        passwd = generate_password_hash(passwd)
        openluat_user_params = {
            'name': name,
            'phone': phone,
            'password_hash': passwd,
            'creation_time': common.time_to_str(int(time.time())),
            'realname':name,
            'have_shop': 1,
        }
        Data.insert('openluat_user', openluat_user_params)
        # 写入记录
        # 写入openluat_user表
        user_base = Data.find('openluat_user', [('phone', '=', phone)])

        inv_params = {
            'user_id': user_base['id'],
            'inv_code': common.create_invite_code(),
            'inviter': inv_info['user_id'],
        }
        Data.insert('invite_code', inv_params)
        # 创建商家专属邀请码
        distr_param = {
            'user_id': user_base['id'],
            'upper_id': inv_info['user_id'],
            'is_super': 0
        }
        Data.insert('distr_relation', distr_param)
        # 写入业务员关系数据表

        shop_distr_params = {
            'user_id': user_base['id'],
        }

        # 查询分润比例
        share_info = Data.find('share_record', [('id', '!=', 0)],order=['id','desc'])
        if share_info is None:
            shop_distr_params['shop_share_min'] = share_info['shop_share_min']
            shop_distr_params['shop_share_max'] = share_info['shop_share_max']
            
        Data.insert('shop_share_type',{'shop_id': user_base['id'],'share_id':1})    

        Data.insert('shop_distr', shop_distr_params)
        # 写入商户分润表
        Data.insert('shop_machine_setting', {'shop_id': user_base['id']})
        print('插入')
        # Data.insert('shop_machine_setting', {'shop_id': user_base['id']})
        reply = {
            'sign_status': 0
        }
        self.send_ok(reply)

        return
