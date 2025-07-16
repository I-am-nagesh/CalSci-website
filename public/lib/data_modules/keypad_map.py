class Keypad_5X8:
    def __init__(self, state="d"):
        keypad_5X8_layout_default=[
            ["alpha", "beta", "nav_u", "home", "on"],
            ["back", "nav_l", "ok", "nav_r", "tab"],
            ["\"", "'", "nav_d", "(", ")"],
            ["pow(", "sin(", "cos(", "tan(", "log("],
            ["7", "8", "9", "nav_b", "AC"],
            ["4", "5", "6", "*", "/"],
            ["1", "2", "3", "+", "-"],
            [".", "0", "*pow(10,", "ans", "exe"],
        ]
        keypad_5X8_layout_alpha=[
            ["alpha", "beta", "nav_u", "opt", "on"],
            ["alpha_on", "nav_l", "ok", "nav_r", "<"],
            ["y", "z", "nav_d", "[", "]"],
            ["t", "u", "v", "w", "x"],
            ["o", "p", "q", "r", "s"],
            ["j", "k", "l", "m", "n"],
            ["e", "f", "g", "h", "i"],
            ["a", "b", "c", "d", " "],
        ]
        keypad_5X8_layout_beta=[
            ["alpha", "beta", "nav_u", "backlight", "on"],
            ["beta_on", "nav_l", "ok", "nav_r", ">"],
            ["off", "caps", "nav_d", "{", "}"],
            ["pi", "asin(", "acos(", "atan(", ""],
            ["&", "~", "\\", "", ""],
            ["$", "%", "^", "|", ""],
            ["!", "@", "#", "=", "_"],
            [",", "?", ":", ";", ""],
        ]

        
        self.state=state
        self.states={"d":keypad_5X8_layout_default, "a":keypad_5X8_layout_alpha, "b": keypad_5X8_layout_beta}
    def key_out(self, col, row):
        return self.states[self.state][row][col]
    def key_change(self, state):
        self.state=state
