from data_modules.object_handler import data_bucket, current_app, text, menu, form, keypad_state_manager_reset
import gc

app_dict={
    "home":"", 
    "calculate":"", 
    "graph":"", 
    "settings":"", 
    "chatbot_ai":"", 
    "backlight":"",
    "wifi_app":"",
    "wifi_connector":"",
    "network_status":""
    }


def app_handler():

    while True:
        
        del menu.menu_list[:]

        text.all_clear()

        del form.form_list[:]
        form.input_list.clear()

        keypad_state_manager_reset()

        exec(f"from application_modules.{current_app[0]} import {current_app[0]}")
        app_dict[current_app[0]]=eval(current_app[0])
        app_dict[current_app[0]](data_bucket)
        app_dict[current_app[0]]=""
        gc.collect()
        print(gc.mem_free(), gc.mem_alloc())