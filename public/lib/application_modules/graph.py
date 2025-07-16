import framebuf # type: ignore
import math
import utime as time  # type:ignore
from data_modules.object_handler import display, form, nav, form_refresh, typer, keypad_state_manager, keypad_state_manager_reset
from data_modules.object_handler import current_app
import gc

eval_globals = {
    # Functions
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'atan2': math.atan2,
    'ceil': math.ceil,
    'copysign': math.copysign,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
    'ldexp': math.ldexp,
    'log': math.log,
    'modf': math.modf,
    'pow': math.pow,
    'radians': math.radians,
    'sqrt': math.sqrt,
    'trunc': math.trunc,
    
    # Constants
    'pi': math.pi,
    'e': math.e,
}

def graph(db={}):
    print("start of graph", gc.mem_free())
    keypad_state_manager_reset()
    global display, form, form_refresh, typer, nav, current_app, eval_globals
    form.input_list={"inp_0": "x*sin(x) ", "inp_1": "-20 ", "inp_2": "20 ", "inp_3": "-10 ", "inp_4": "10 "}
    form.form_list=["enter function:f(x)", "inp_0", "enter x_min:", "inp_1", "enter x_max:", "inp_2", "enter y_min:", "inp_3", "enter y_max:", "inp_4"]
    form.update()
    form_refresh.refresh()

    buffer1 = bytearray((128 * 64) // 8)
    fb1 = framebuf.FrameBuffer(buffer1, 128, 64, framebuf.MONO_VLSB)

    while True:
        inp = typer.start_typing()
        if inp == "back":
            del buffer1, fb1
            current_app[0]="home"
            break

        elif inp == "ok":
            plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                         x_min=eval(form.inp_list()["inp_1"], eval_globals), 
                         x_max=eval(form.inp_list()["inp_2"], eval_globals), 
                         y_min=eval(form.inp_list()["inp_3"], eval_globals), 
                         y_max=eval(form.inp_list()["inp_4"], eval_globals), 
                         width=128, height=64)
            display.clear_display()
            display.graphics(buf=buffer1)
            print("after plotting", gc.mem_free())
            while True:
                inp_breaker = typer.start_typing()

                break
            fb1.fill(0)
            form.refresh_rows = (0, form.actual_rows)
            display.clear_display()
            form_refresh.refresh()

        elif inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")
        elif inp not in ["alpha", "beta", "ok"]:
            form.update_buffer(inp)
        form_refresh.refresh(state=nav.current_state())
    
        time.sleep(0.1)
    print("end of graph", gc.mem_free())
def plot_function(fb, func, exp_str, x_min, x_max, y_min, y_max, width, height):
    # global x_past, y_past
    fb.line(0,31,127,31, 1)
    fb.line(63,0,63,63,1)
    global eval_globals
    x_past=0
    y_past=0
    # Scale factors to map function values to the display's pixel coordinates
    x_scale = (x_max - x_min) /(width)
    y_scale = (y_max - y_min) / (height)

    # Loop through each x pixel
    for x_pixel in range(width):
        
        # Convert the pixel x-coordinate to the mathematical x-value
        x_value = x_min + (x_pixel) * x_scale

        # Calculate the corresponding y-value for the function
        y_value = func(exp=exp_str,x=x_value)

        # Scale the y-value to the display height and invert it (because displays usually have y=0 at the top)
        y_pixel = int(height - (y_value - y_min) / y_scale)
        
        if func(exp=exp_str,x=x_value)>y_max or func(exp=exp_str,x=x_value)<y_min:

            # print(" pixel= ",x_pixel," ", y_pixel," value= ",x_value," ", y_value ," past= ",x_past," ",y_past)
            x_past=0
            y_past=0
            # fb.vline(x_pixel,y_pixel, 100,1)

        # Ensure y_pixel is within the display range
        if 0 <= y_pixel < height:
            
            fb.pixel(x_pixel-1, y_pixel-1, 1)
            # if x_past!=0 and y_past!=0:
            if x_past*y_past!=0:
                fb.line(x_past, y_past, x_pixel-1, y_pixel-1, 1)
            x_past=x_pixel-1
            y_past=y_pixel-1

def polynom1(exp, x):
    global eval_globals
    # Add 'x' to the dictionary for evaluation
    eval_globals["x"]=x
    # Combine global and local dictionaries
    # context = eval_globals + eval_locals
    # Evaluate the expression
    y = eval(exp, eval_globals)

    return y

