import network # type: ignore
from data_modules.object_handler import nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
import time
from data_modules.object_handler import current_app, data_bucket

def wifi_app(db={}):
    global display, menu, menu_refresh, typer, keymap, nav, current_app
    display.clear_display()
    menu_list = ["Scanning..."]
    menu.menu_list=menu_list
    menu.update()
    menu_refresh.refresh()

    network_names = scan_networks()

    menu_list=network_names[:15] if len(network_names) >= 15 else network_names
    menu.menu_list=menu_list
    menu.update()
    menu_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "ok":
            data_bucket["ssid_g"] = network_names[menu.cursor()][3:]
            current_app[0]="wifi_connector"
            break

        if inp == "back":
            current_app[0]="settings"
            break

        menu.update_buffer(inp)
        menu_refresh.refresh()
        time.sleep(0.1)

def scan_networks():
    network_names = []
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    networks = sta_if.scan()
    for i, network_info in enumerate(networks):
        ssid = network_info[0].decode()
        network_names.append(f'{i + 1}. {ssid}')

    return network_names
