from data_modules.object_handler import nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
import time
from data_modules.object_handler import current_app
def home(db={}):
    display.clear_display()
    menu_list = ["calculate", "graph", "chatbot_ai", "settings"]
    menu.menu_list=menu_list
    menu.update()
    menu_refresh.refresh()
    try:
        while True:
            inp = typer.start_typing()
            if inp == "back":
                pass
            elif inp == "alpha" or inp == "beta":
                keypad_state_manager(x=inp)
                menu.update_buffer("")
            elif inp =="ok":
                current_app[0]=menu.menu_list[menu.menu_cursor]
                break
            menu.update_buffer(inp)
            menu_refresh.refresh(state=nav.current_state())
            time.sleep(0.15)
    except Exception as e:
        print(f"Error: {e}")