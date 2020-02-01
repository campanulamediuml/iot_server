from werkzeug.security import generate_password_hash

from data.server import Data



def admin():
    Data.query('drop table admin')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('username', 'varchar(128)','default ""'),
        # 用户名
        ('pwhash', 'varchar(512)','default ""'),
        # 密码哈希
        ('token','varchar(128)','default ""'),
        # token
        ('auth_id','int','default 1'),
        # 权限
        ('ctime', 'int', 'default "0"'),
        # 创建时间
        ('utime', 'int', 'default "0"'),
        # 更新时间
        ('comment', 'varchar(1024)', 'default ""'),
        # 备注
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('admin', colums)
    params = {
        'username':'yanbokeji',
        'pwhash':generate_password_hash('123456')
    }
    Data.insert('admin',params)
    # 后台账号


def player():
    Data.query('drop table player')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('open_id', 'varchar(128)', 'default ""'),
        # openid
        ('union_id', 'varchar(128)', 'default ""'),
        # unionid
        ('phone', 'varchar(128)', 'default ""'),
        # 电话
        ('nickname', 'varchar(128)', 'default ""'),
        # 昵称
        ('sex', 'int', 'default "0"'),
        # 性别
        ('add_time', 'int', 'default "0"'),
        # 创建时间
        ('avatar', 'varchar(512)', 'default ""'),
        # 头像
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('player', colums)
    # 用户账号


def auth():
    Data.query('drop table admin_temp')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('name', 'varchar(64)', 'default ""'),
        # 模板名称
        ('auth', 'varchar(1024)', 'default ""'),
        # 权限模板
        ('comment', 'varchar(1024)', 'default ""'),
        # 备注
        ('ctime', 'int', 'default "0"'),
        # 创建时间
        ('utime', 'int', 'default "0"'),
        # 更新时间
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('admin_temp', colums)
    params = {
        'name': '超级管理员',
        'comment': '超级管理员权限模板',
        'ctime': 0,
        'auth': '1111,1111,1111,111,1111,1111,11,11,111,111,111,111,1111,1111,1111'
    }
    Data.insert('admin_temp', params)
    # 权限模板

    Data.query('drop table admin_auth')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('auth_id', 'int', 'default "0"'),
        ('god_id', 'int', 'default "0"'),
    ]
    Data.create('admin_auth', colums)
    params = {
        'god_id': 1,
        'auth_id': '1',
    }
    Data.insert('admin_auth', params)


def operate():
    # 存储后台操作记录
    Data.query('drop table admin_operate_record')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('operate_id', 'int', 'default "0"'),
        # 操作者id
        ('admin_id', 'int', 'default "0"'),
        # 被操作管理员的id
        ('temp_id', 'int', 'default "0"'),
        # 被操作管理员模板的id
        ('player_phone', 'varchar(64)', 'default "0"'),
        # 被操作用户的手机号
        ('player_id', 'int', 'default "0"'),
        # 被操作用户的id
        ('adv_id', 'int', 'default "0"'),
        # 被操作的广告id
        ('operate_desc', 'varchar(1024)', 'default ""'),
        # 操作描述
        ('operate_time', 'int', 'default "0"'),
        # 操作时间

    ]
    Data.create('admin_operate_record', colums)

def advertisement():
    # 广告
    Data.query('drop table adv')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('adv_name', 'varchar(64)', 'default ""'),
        # 广告名
        ('postion', 'varchar(64)', 'default ""'),
        # 位置
        ('url', 'varchar(64)', 'default ""'),
        # 链接
        ('ctime', 'int', 'default "0"'),
        # 创建时间
        ('utime', 'int', 'default "0"'),
        # 更新时间
        ('comment', 'varchar(1024)', 'default ""'),
        # 备注
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('adv', colums)

    Data.query('drop table adv_photo')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('adv_id', 'varchar(64)', 'default ""'),
        # 广告id
        ('photo_url', 'varchar(64)', 'default ""'),
        # 图片链接
    ]
    Data.create('adv_photo', colums)
    # 广告图片

def devices():
    # 设备
    Data.query('drop table devices')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('imei', 'varchar(64)', 'default ""'),
        # 设备号
        ('ctime', 'int', 'default "0"'),
        # 创建时间
        ('times', 'int', 'default "0"'),
        # 使用次数
        ('user_id', 'int', 'default "0"'),
        # 绑定的账号id
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('devices', colums)
    # 设备表

def dev_main():
    Data.query('drop table dev_main')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('imei', 'varchar(64)', 'default ""'),
        # 设备号
        ('ctime', 'int', 'default "0"'),
        # 创建时间
        ('last_connect_time','int', 'default "0"'),
        # 上次通讯时间
        ('lo','varchar(64)','default "0"'),
        ('la', 'varchar(64)', 'default "0"'),
        # 位置信息

        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('dev_main', colums)
    # 设备信息表


def user_test_result():
    Data.query('drop table user_test_result')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('test_number','varchar(128)', 'default ""'),
        ('imei', 'varchar(64)', 'default ""'),
        # 设备号
        ('test_time', 'int', 'default "0"'),
        # 创建时间
        ('test_finish_time', 'int', 'default "0"'),
        # 创建时间
        ('member_id','int', 'default "0"'),
        # 测试用户id
        ('user_id', 'int', 'default "0"'),
        # 绑定机器的账号id
        ('test_type', 'int', 'default "0"'),
        # 0自动 1近视测试 2散光测试

        ('left_eye','varchar(64)','default "0"'),
        ('astigmatism_left', 'int', 'default "0"'),
        ('right_eye', 'varchar(64)', 'default "0"'),
        ('astigmatism_right', 'int', 'default "0"'),
        # 测试结果
        ('comment', 'varchar(512)', 'default ""'),
        # 使用备注
        ('status', 'int', 'default "0"'),
        # 状态  0-正常结束  1-异常结束
    ]
    Data.create('user_test_result', colums)
    # 测试结果

def player_member():
    Data.query('drop table player_member')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('name', 'varchar(512)', 'default ""'),
        # 用户名
        ('birth_day', 'varchar(128)', 'default ""'),
        # 出生日期
        ('sex', 'int', 'default "0"'),
        # 性别
        ('phone', 'varchar(128)', 'default ""'),
        # 电话
        ('group_id','varchar(512)', 'default ""'),
        # 用户组
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('player_member', colums)
    # 用户资料

def player_group():
    Data.query('drop table player_group')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('name', 'varchar(512)', 'default ""'),
        # 用户组名
        ('comment','varchar(512)', 'default ""'),
        # 用户组备注
        ('add_time', 'int', 'default "0"'),
        # 创建时间
        ('status', 'int', 'default "0"'),
        # 状态
        ('player_id', 'int', 'default "0"'),
        # 绑定的用户的id
    ]
    Data.create('player_group', colums)
    # 用户资料


def init_tables():
    admin()
    player()
    auth()
    operate()
    advertisement()
    devices()
    player_member()
    dev_main()
    user_test_result()
    player_group()

