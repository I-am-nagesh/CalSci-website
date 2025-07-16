import gc
gc.enable()
print("free ram initially=", gc.mem_free())
print("ram allocated initially=", gc.mem_alloc())
from application_modules.backlight import backlight_pin
backlight_pin.off() #3.0
