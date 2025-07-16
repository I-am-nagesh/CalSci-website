class Menu:
    def __init__(self, rows=7, cols=21, menu_list = ["label_0", "label_1", "label_2"], menu_cursor = 0, menu_display_position = 0):
        self.rows=rows
        self.cols=cols
        self.menu_list=menu_list
        self.menu_cursor=menu_cursor
        self.menu_display_position=menu_display_position
        self.menu_display_size = min(self.rows, len(self.menu_list))
        self.display_buffer = self.menu_list[self.menu_display_position:self.menu_display_position + self.menu_display_size]
        self.display_cursor = self.menu_cursor - self.menu_display_position
        self.refresh_rows = (0, self.menu_display_size)

    def update_buffer(self, text):
        if text == "nav_d":
            self.menu_cursor += 1
            if self.menu_cursor == len(self.menu_list):  # Wrap to top if at the bottom
                self.menu_cursor = 0
                self.menu_display_position = 0
                self.refresh_rows = (0, self.menu_display_size)
            elif self.menu_cursor - self.menu_display_position == self.menu_display_size:
                self.menu_display_position += 1
                self.refresh_rows = (0, self.menu_display_size)
            else:
                self.refresh_rows = (self.menu_cursor - 1 - self.menu_display_position, self.menu_cursor - self.menu_display_position+1)
        elif text == "nav_u":
            self.menu_cursor -= 1
            if self.menu_cursor < 0:  # Wrap to bottom if at the top
                self.menu_cursor = len(self.menu_list) - 1
                self.menu_display_position = max(0, len(self.menu_list) - self.menu_display_size)
                self.refresh_rows = (0, self.menu_display_size)
            elif self.menu_cursor < self.menu_display_position:
                self.menu_display_position -= 1
                self.refresh_rows = (0, self.menu_display_size)
            else:
                self.refresh_rows = (self.menu_cursor - self.menu_display_position, self.menu_cursor - self.menu_display_position + 2)

        self.display_buffer = self.menu_list[self.menu_display_position:self.menu_display_position + self.menu_display_size]
        self.display_cursor = self.menu_cursor - self.menu_display_position
    
    def buffer(self):
        return self.display_buffer
    
    def cursor(self):
        return self.display_cursor
    
    def ref_ar(self):
        return self.refresh_rows
    
    def update(self):
        self.menu_cursor=0
        self.menu_display_position=0
        self.menu_display_size = min(self.rows, len(self.menu_list))
        self.display_buffer = self.menu_list[self.menu_display_position:self.menu_display_position + self.menu_display_size]
        self.display_cursor = self.menu_cursor - self.menu_display_position
        self.refresh_rows = (0, self.menu_display_size)