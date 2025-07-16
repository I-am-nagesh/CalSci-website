from machine import Pin  # type: ignore
import utime as time #type: ignore

class Keypad:
    def __init__(self, rows, cols):
        self.rows=rows
        self.cols=cols
        for pin in rows:
            Pin(pin, Pin.IN, Pin.PULL_UP)
        for pin in cols:
            p = Pin(pin, Pin.OUT)
            p.value(1)
        self.state=True
    def keypad_loop(self):    
        while self.state==True:
            for col in range(len(self.cols)):
                Pin(self.cols[col], Pin.OUT).value(0)
                for row in range(len(self.rows)):
                    buttonState = Pin(self.rows[row], Pin.IN, Pin.PULL_UP).value()
                    
                    if buttonState == 0:
                        Pin(self.cols[col], Pin.OUT).value(1)
                        col_row=(col, row)
                        print(col_row)
                        return col_row
                Pin(self.cols[col], Pin.OUT).value(1)
    def keypad_stop(self):
        self.state=False

    def keypad_start(self):
        self.state=True
