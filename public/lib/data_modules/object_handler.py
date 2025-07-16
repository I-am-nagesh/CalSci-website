from process_modules.text_buffer import Textbuffer
from process_modules.text_buffer_uploader import Tbf as text_tbf

from process_modules.menu_buffer import Menu
from process_modules.menu_buffer_uploader import Tbf as menu_tbf

from process_modules.form_buffer import Form
from process_modules.form_buffer_uploader import Tbf as form_tbf

from process_modules.typer import Typer
from input_modules.keypad import Keypad
from data_modules.keypad_map import Keypad_5X8

from output_modules.st7565_spi import Display

from data_modules.characters import Characters

from process_modules.navbar import Nav

current_app=["home", ""]
data_bucket={"ssid_g" : "", "connection_status_g" : False}
keypad_rows=[26, 25, 33, 32, 35, 34, 39, 36] #3.0
keypad_cols=[15, 13, 12, 14, 27] #3.0
st7565_display_pins={"cs1":2, "rs":16, "rst":4, "sda":5, "sck":17}  #3.0
display = Display(cs1=st7565_display_pins["cs1"], rs=st7565_display_pins["rs"], rst=st7565_display_pins["rst"], sda=st7565_display_pins["sda"], sck=st7565_display_pins["sck"])

keymap = Keypad_5X8()
keyin = Keypad(rows=keypad_rows, cols=keypad_cols)
typer = Typer(keypad=keyin, keypad_map=keymap)

chrs=Characters()

text=Textbuffer()
menu=Menu()
form=Form()

nav = Nav(disp_out=display, chrs=chrs)

text_refresh=text_tbf(disp_out=display, chrs=chrs, t_b=text)
menu_refresh=menu_tbf(disp_out=display, chrs=chrs, m_b=menu)
form_refresh=form_tbf(disp_out=display, chrs=chrs, f_b=form)

def keypad_state_manager(x):
    if keymap.state == "a" and x[0] == "a":
        keymap.key_change(state="d")
        nav.state_change(state="d")
    elif keymap.state == "b" and x[0] == "b":
        keymap.key_change(state="d")
        nav.state_change(state="d")
    else:
        keymap.key_change(state=x[0])
        nav.state_change(state=x[0])

def keypad_state_manager_reset():
    keymap.key_change(state="d")
    nav.state_change(state="d")
