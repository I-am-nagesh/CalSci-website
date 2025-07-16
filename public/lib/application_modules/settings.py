import time
from data_modules.object_handler import current_app, nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
from application_modules.backlight import backlight, backlight_pin

def settings(db={}):
    global current_app, display, menu, menu_refresh, typer, keymap, nav, backlight_pin
    display.clear_display()
    settins_list = ["wifi_app", "network_status", "backlight"]
    menu.menu_list=settins_list
    menu.update()
    menu_refresh.refresh()
    try:
        while True:
            inp_menu = typer.start_typing()

            if inp_menu == "back":
                current_app[0]="home"
                break  
        
            elif inp_menu == "alpha" or inp_menu == "beta":
                keypad_state_manager(x=inp_menu)
                menu.update_buffer("")
            elif inp_menu =="ok" and menu.menu_list[menu.menu_cursor]in ["backlight"]:
                backlight()
            elif inp_menu =="ok":
                current_app[0]=menu.menu_list[menu.menu_cursor]
                break
            menu.update_buffer(inp_menu)
            menu_refresh.refresh(state=nav.current_state())
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")