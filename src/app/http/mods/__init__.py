from app.http.mods import test_mod
from app.http.mods import shop
from app.http.mods import agent
from app.http.mods import player
from app.http.mods import admin
from app.http.mods import admin_common
from app.http.mods import dev_admin
from app.http.mods import dev

def create_route():
    route_list = []
    route_list.extend(test_mod.route_list)
    route_list.extend(shop.route_list)
    route_list.extend(agent.route_list)
    route_list.extend(player.route_list)
    route_list.extend(admin.route_list)
    route_list.extend(admin_common.route_list)
    route_list.extend(dev_admin.route_list)
    route_list.extend(dev.route_list)

    return route_list
