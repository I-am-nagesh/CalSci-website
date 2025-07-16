import network # type: ignore
from data_modules.object_handler import nav, keypad_state_manager, menu, menu_refresh, form, form_refresh, typer, keymap, display
import time
from data_modules.object_handler import current_app, data_bucket

connection_status = False
sta_if = network.WLAN(network.STA_IF)



if not sta_if.active():
    sta_if.active(True)
    time.sleep(1)

def display_error_message(ssid):
    display.clear_display()
    menu.menu_list=["Failed to connect to:", ssid]
    menu.update()
    menu_refresh.refresh()


    while True:
        error_inp = typer.start_typing()
        if error_inp:
            current_app[0]="settings"
            break

def display_ip_addresses(ssid):
    ssid=data_bucket["ssid_g"]
    ip_addresses = list(sta_if.ifconfig())
    ip_addresses.insert(0, "Connected to:")
    ip_addresses.insert(1, ssid)
    ip_addresses.insert(2, "IP Addresses:")
    ip_addresses.append("Press OK to continue")
    menu.menu_list=ip_addresses
    menu.update()
    display.clear_display()
    menu_refresh.refresh()

    while True:
        inp_menu = typer.start_typing()

        if inp_menu == "ok" or inp_menu == "back":
            current_app[0]="settings"
            break
        menu.update_buffer(inp_menu)
        menu_refresh.refresh()
        time.sleep(0.1)

def wifi_connector(ssid):
    ssid=data_bucket["ssid_g"]
    form.input_list={"inp_0": " "}
    form.form_list=["Password:", "inp_0", "Wi-Fi Name:", ssid]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="settings"
            break

        if inp == "ok":
            password = form.input_list["inp_0"]
            password = password[:-1]
            print(ssid, password, len(password))

            display.clear_display()
            menu.menu_list=["Trying to connect to:", ssid]
            menu.update()
            menu_refresh.refresh()

            do_connect(ssid, password)

            connection_status = False
            connection_status = sta_if.isconnected()
            data_bucket["connection_status_g"] = connection_status
            if connection_status:
                display_ip_addresses(ssid)
            else:
                display_error_message(ssid)
            display.clear_display()
            break
        if inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")
        if inp not in ["alpha", "beta", "ok"]:
            form.update_buffer(inp)
        form_refresh.refresh(state=nav.current_state())
        time.sleep(0.15)
        

def do_connect(ssid, password):
    sta_if.active(True)
    if sta_if.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    sta_if.connect(ssid, password)
    for retry in range(100):
        connected = sta_if.isconnected()
        if connected:
            break
        time.sleep(0.1)
    if connected:
        print('\nConnected. Network config: ', sta_if.ifconfig())
        
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

