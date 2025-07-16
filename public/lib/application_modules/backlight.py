from machine import Pin # type: ignore

# Assuming the backlight is connected to a specific pin (e.g., Pin 15)
backlight_pin = Pin(19, Pin.OUT) #3.0
backlight_label=""
if backlight_pin.value() ==1:

    backlight_label="backlight off"
else:
    backlight_label="backlight on"
# Function to toggle the backlight
def backlight(db={}):
    current_state = backlight_pin.value()  # Read the current state
    if current_state == 1:  # If the backlight is ON
        backlight_pin.off()  # Turn it OFF
    else:  # If the backlight is OFF
        backlight_pin.on()  # Turn it ON
