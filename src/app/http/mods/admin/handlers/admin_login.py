from werkzeug.security import check_password_hash

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from app.http.relay.relay import Relay
from data.server import Data
from error import error

class admin_login(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        username = data['username']
        pw = data['pswd']

        user = Data.find('admin',[('username','=',username)])
        if user == None:
            self.send_faild(error.ERROR_NO_USER)
            return
        if not check_password_hash(user['pwhash'], pw):
            self.send_faild(error.ERROR_WRONG_PSWD)
            return

        token = self.create_token(user['id'], table_name="admin")
        res = {
            'token':token
        }
        # Relay.admin_login(user['id'],token)
        self.send_ok(res)
        return

class admin_logout(HandlerBase):
    @run_on_executor
    def get(self):
        admin_base = self.get_admin_base()
        if admin_base == None:
            self.send_faild(error.ERROR_NO_LOGIN)
            return

        admin_id = admin_base['id']
        if admin_id in Relay.admin_token_dict:
            Relay.admin_token_dict[admin_id] = ''
        Data.update('admin',[('id','=',admin_id)],{'token','=',''})
        return