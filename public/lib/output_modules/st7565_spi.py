from machine import Pin, SPI  # type: ignore
import utime as time #type: ignore

class Display:

    def __init__(self, cs1, rs, rst, sda, sck):
        self.cs1 = Pin(cs1, Pin.OUT)
        self.rs = Pin(rs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.sda = Pin(sda, Pin.OUT)
        self.sck = Pin(sck, Pin.OUT)
        self.spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=self.sck, mosi=self.sda)

        self.rst.value(0)  # Reset the display
        time.sleep_ms(50)
        self.rst.value(1)  # End reset

        self.write_instruction(0xAE)  # Display OFF
        self.write_instruction(0xA2)  # Set Bias 1/9 (default)
        self.write_instruction(0xA0)  # Set ADC normal
        self.write_instruction(0xC8)  # Set COM output direction, normal mode
        self.write_instruction(0xA6)  # Display normal (not inverted)
        self.write_instruction(0x2F)  # Power control: Booster, Regulator, Follower on
        self.write_instruction(0x27)  # Set contrast (0x27 can be adjusted)
        self.write_instruction(0x81)  # Set contrast
        self.write_instruction(0x00)  # Contrast level (set to 0x16 here)
        self.write_instruction(0xAF)  # Display ON

    def write_instruction(self, cmd):
        self.rs.value(0)  # Set RS to 0 for command
        self.cs1.value(0)  # Activate chip select
        self.spi.write(bytearray([cmd]))  # Write command via SPI
        self.cs1.value(1)  # Deactivate chip select

    def write_data(self, data):
        self.rs.value(1)  # Set RS to 1 for data
        self.cs1.value(0)  # Activate chip select
        self.spi.write(bytearray([data]))  # Write data via SPI
        self.cs1.value(1)  # Deactivate chip select

    def set_page_address(self, page):
        self.write_instruction(0xB0 | page)  # Set page address (B0h to B7h)

    def set_column_address(self, column):
        self.write_instruction(0x10 | (column >> 4))  # Set higher column address
        self.write_instruction(0x00 | (column & 0x0F))  # Set lower column address


    # Clear the entire display
    def clear_display(self):
        for page in range(8):  # Assuming an 8-page display
            self.set_page_address(page)
            self.set_column_address(0)
            for column in range(128):  # Assuming 128 columns
                self.write_data(0x00)  # Clear all columns
    
    def graphics(self, buf):
        # self.clear_display()
        for i in range(8):
            self.set_page_address(i)
            self.set_column_address(0)
            for j in range(128):
                # self.write_data(eval(buf[i*128+j]))
                self.write_data(buf[i*128+j])

