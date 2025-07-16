class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, id, mode=-1, pull=-1):
        self.id = id
        self.mode = mode
        self.pull = pull
        self._value = 0
        # print(f"Pin({id}) initialized: mode={mode}, pull={pull}")

    def value(self, x=None):
        if x is not None:
            self._value = x
            # print(f"Pin({self.id}) set to {x}")
        return self._value

    def on(self):
        self.value(1)

    def off(self):
        self.value(0)

class SPI:
    def __init__(self, id, baudrate=1000000, polarity=0, phase=0, sck=None, mosi=None):
        self.id = id
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.sck = sck
        self.mosi = mosi
        self._initialized = False

        if sck and isinstance(sck, Pin):
            sck.mode = Pin.OUT
            sck.off()
            self._initialized = True
        if mosi and isinstance(mosi, Pin):
            mosi.mode = Pin.OUT
            mosi.off()
        

    def write(self, data):
        if not self._initialized:
            return
        if isinstance(data, (bytes, bytearray)):
            if self.sck:
                self.sck.on()
            self.sck.off()
            if self.mosi:
                self.mosi.on()
            self.mosi.off()

    def deinit(self):
        if self._initialized:
            if self.sck:
                self.sck.off()
            if self.mosi:
                self.mosi.off()
            self._initialized = False