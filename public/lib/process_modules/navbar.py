class Nav:
    def __init__(self, disp_out, chrs):
        self.state="d"
        self.states={"d":"default", "a":"alpha", "b":"beta"}
        self.disp_out=disp_out
        self.chrs=chrs

    def state_change(self, state):
        self.state=state

    def current_state(self):
        return self.states[self.state]