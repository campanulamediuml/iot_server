from app.http.mods.admin.handlers.admin_device import get_devices_list, get_device_detail, get_device_test
from app.http.mods.admin.handlers.admin_login import admin_login, admin_logout
from app.http.mods.admin.handlers.admin_admin import get_admin_list, get_admin_detail, add_admin, update_admin_detail, \
    delete_admin
from app.http.mods.admin.handlers.admin_adv import get_adv_list, get_adv_info, add_adv, update_adv, del_adv
from app.http.mods.admin.handlers.admin_auth import get_auth_template_list, create_auth_template, update_auth_template, \
    get_auth_template, delete_auth_template
# from app.http.mods.admin.handlers.admin_device import get_devices_list, get_device_detail
from app.http.mods.admin.handlers.admin_player import get_player_list, get_player_info

route_list = [
    (r'/admin/adminlogin', admin_login),
    (r'/admin/adminlogout', admin_logout),
    # 会员管理
    (r'/admin/playerlist', get_player_list),
    (r'/admin/playerinfo', get_player_info),
    # 管理员管理
    (r'/admin/adminlist', get_admin_list),
    (r'/admin/admininfo', get_admin_detail),
    (r'/admin/adminadd', add_admin),
    (r'/admin/adminupdate', update_admin_detail),
    (r'/admin/admindel', delete_admin),
    # 权限模板
    (r'/admin/templist', get_auth_template_list),
    (r'/admin/tempadd', create_auth_template),
    (r'/admin/tempupdate', update_auth_template),
    (r'/admin/tempcheck', get_auth_template),
    (r'/admin/tempdel', delete_auth_template),
    # 广告
    (r'/admin/advlist', get_adv_list),
    (r'/admin/advinfo', get_adv_info),
    (r'/admin/advadd', add_adv),
    (r'/admin/advupdate', update_adv),
    (r'/admin/advdel', del_adv),
    # 设备
    (r'/admin/deviceslist', get_devices_list),
    (r'/admin/devicesinfo', get_device_detail),
    (r'/admin/devicestestinfo', get_device_test),

]
