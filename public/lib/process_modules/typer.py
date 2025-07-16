class Typer:
    def __init__(self, keypad, keypad_map):
        self.keypad=keypad
        self.keypad_map=keypad_map

    def start_typing(self):
        key_inp=self.keypad.keypad_loop()
        text=self.keypad_map.key_out(col=int(key_inp[0]), row=int(key_inp[1]))
        return text
