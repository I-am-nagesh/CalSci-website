import utime as time  # type:ignore
from data_modules.object_handler import display, form, nav, form_refresh, typer, keypad_state_manager, keypad_state_manager_reset
from data_modules.object_handler import current_app


def chatbot_ai(db={}):
    global display, form, form_refresh, typer, nav, current_app
    display.clear_display()
    form.input_list = {"inp_0":" "}
    form.form_list = ["name:", "inp_0"]
    form.update()
    form_refresh.refresh()
    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="home"
            break
        elif inp == "ok":
            current_input_key = form.buffer()[form.cursor()]
            input_text = form.inp_list()["inp_0"]
            label_index = form.form_list.index(current_input_key) - 1
            new_text = f"{form.form_list[label_index]} {input_text}"
            form.update_label(label_index, new_text)
            form.input_list[current_input_key] = " "
            form.inp_cursor = 0
            form_refresh.refresh()
            form.update_buffer("nav_u")
            form.update_buffer("nav_d")


        elif inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")
        elif inp not in ["alpha", "beta", "ok"]:
            form.update_buffer(inp)
        form_refresh.refresh(state=nav.current_state())
        time.sleep(0.1)
