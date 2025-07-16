import utime as time  # type:ignore
from math import *
from data_modules.object_handler import display, text, nav, text_refresh, typer, keypad_state_manager, keypad_state_manager_reset
from data_modules.object_handler import current_app
def calculate(db={}):
    keypad_state_manager_reset()
    global display, text, text_refresh, typer, nav, current_app
    display.clear_display()
    text.all_clear()
    text_refresh.refresh()
    try:
        while True:

            x = typer.start_typing()

            if x == "back":
                current_app[0]="home"
                break
            
            if x == "ans" and text.text_buffer[0] != "𖤓":
                try:
                    res = str(eval(text.text_buffer[:text.text_buffer_nospace]))
                except Exception as e:
                    res = "Invalid Input"
                text.all_clear()
                display.clear_display()
                text.update_buffer(res)

            elif x == "alpha" or x == "beta":
                keypad_state_manager(x=x)
                text.update_buffer("")

            elif x != "ans":
                text.update_buffer(x)

            if text.text_buffer[0] == "𖤓":
                display.clear_display()
                text.all_clear()

            text_refresh.refresh(state=nav.current_state())
            time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
