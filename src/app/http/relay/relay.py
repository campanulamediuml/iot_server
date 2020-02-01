import time
import json
from common import common
from data.server import Data
from config import config
from common.Scheduler import IntervalTask


class Relay(object):
    server = None
    player_token_dict = {}
    admin_token_dict = {}

    @staticmethod
    def init(server):
        Relay.server = server
        # 创建初始用户
        all_admin = Data.select('admin', [('id', '!=', 0)])
        if all_admin != None:
            for line in all_admin:
                Relay.admin_token_dict[line['id']] = ''

        all_player = Data.select('player', [('id', '!=', 0)])
        if all_player != None:
            for line in all_player:
                Relay.player_token_dict[line['id']] = ''

        # if config.update_token == True:
        #     Relay.token_refresh()
        # token刷新定时器

    # 服务器核心操作放在这里
    @staticmethod
    def test():
        pass

    @staticmethod
    def get_admin_dict():
        return Relay.admin_token_dict




    # 用户退出
    @staticmethod
    def player_logout(player_id):
        if player_id in Relay.player_token_dict:
            Relay.player_token_dict[player_id] = ''
        return

    # 管理员退出
    @staticmethod
    def admin_logout(admin_id):
        if admin_id in Relay.admin_token_dict:
            Relay.admin_token_dict[admin_id] = ''
        return


    @staticmethod
    def get_admin_base(token):
        # if config.update_token == True:
        #     if token not in Relay.admin_token_dict:
        #         print('admindict中没有这个token')
        #         return None
        res = Data.find('admin', [('token', '=', token)])
        if res != None:
            return res
        for admin_id in Relay.admin_token_dict:
            if Relay.admin_token_dict[admin_id] == token:
                res = Data.find('admin',[('id','=',admin_id)])
                return res
        # Relay.update_admin_token_timeout(token)
        return

    @staticmethod
    def get_player_base(token):
        # if config.update_token == True:
        #     if token not in Relay.player_token_dict:
        #         return None
        res = Data.find('player', [('token', '=', token)])
        if res != None:
            return res
        for player_id in Relay.player_token_dict:
            if Relay.player_token_dict[player_id] == token:
                res = Data.find('player',[('id','=',player_id)])
                return res
        # Relay.update_player_token_timeout(token)
        return

    @staticmethod
    def is_god(token):
        if config.update_token == True:
            if token not in Relay.admin_token_dict:
                return False

        res = Data.find('admin', [('token', '=', token)])
        if res is None:
            return False
        # res = Data.find('god', [('admin_id', '=', res['id'])])
        # if res is None:
        #     return False

        return True
    # 判断是不是超级管理员
    @staticmethod
    def admin_login(user_id, token):
        Relay.admin_token_dict[user_id] = token
        return

    @staticmethod
    def player_login(player_id,token):
        Relay.player_token_dict[player_id] = token
        return


