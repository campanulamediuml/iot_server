from app.http.mods.player.handlers import player_info
from app.http.mods.player.handlers.player_device import player_add_device, player_use_device, player_device_list, \
    player_chose_device, player_unbind_device
from app.http.mods.player.handlers.player_group import player_show_group, player_add_group, player_del_group, \
    player_change_group
from app.http.mods.player.handlers.player_info import player_change_nickname, player_change_phone
from app.http.mods.player.handlers.player_login import player_login, player_log_out, player_get_appid, get_wechat_cfg
from app.http.mods.player.handlers.player_member import player_add_member, player_show_member
from app.http.mods.player.handlers.player_report import player_report_list, player_report_phone_list

route_list = [
    (r'/player/getappid',player_get_appid),
    (r'/player/wechatcfg',get_wechat_cfg),

    (r'/player/login', player_login),
    (r'/player/logout', player_log_out),
    (r'/player/playerinfo', player_info),
    (r'/player/changenickname', player_change_nickname),
    (r'/player/changephone', player_change_phone),

    (r'/player/adddevice', player_add_device),
    (r'/player/usedevice', player_use_device),
    (r'/player/devicelist', player_device_list),
    (r'/player/chosedevice', player_chose_device),
    (r'/player/unbinddevice', player_unbind_device),

    (r'/player/showgroup', player_show_group),
    (r'/player/addgroup', player_add_group),
    (r'/player/delgroup', player_del_group),
    (r'/player/changegroup', player_change_group),

    (r'/player/addmember', player_add_member),
    (r'/player/showmember', player_show_member),

    (r'/player/usereport', player_report_list),
    (r'/player/phoneusereport', player_report_phone_list),
]
