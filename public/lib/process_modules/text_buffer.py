class Textbuffer:
    def __init__(self, text_buffer="𖤓", rows=7, cols=21):
        if text_buffer != "𖤓":
            text_buffer += "𖤓"
        self.text_buffer = text_buffer
        self.menu_buffer_size = len(self.text_buffer)
        self.menu_buffer = list(range(self.menu_buffer_size))
        self.menu_buffer_cursor = 0
        self.rows = rows
        self.cols = cols
        self.display_buffer_position = 0
        self.display_buffer = self.menu_buffer[
            self.display_buffer_position : self.display_buffer_position
            + self.rows * self.cols
        ]
        self.no_last_spaces = 0
        self.buffer_length = self.menu_buffer_size
        self.text_buffer_with_spaces = self.menu_buffer_size
        self.extra_spaces = 0
        self.text_buffer_nospace = 0
        self.refresh_area = (0, self.rows * self.cols)
        self.buffer()
        self.update_buffer("")

    def buffer(self):

        # Calculate the number of spaces needed to make the buffer length a multiple of cols
        self.buffer_length = len(self.text_buffer)
        self.text_buffer_nospace = len(self.text_buffer) - 1
        remaining_spaces = (
            self.cols - (self.buffer_length % self.cols)
            if self.buffer_length % self.cols != 0
            else 0
        )
        self.no_last_spaces = remaining_spaces

        # Append all necessary spaces at once to avoid repeated string concatenation
        if remaining_spaces > 0:
            self.text_buffer += " " * remaining_spaces
        # Calculate the menu_buffer only once
        self.menu_buffer_size = self.buffer_length + remaining_spaces
        # self.menu_buffer = list(range(self.menu_buffer_size))
        # Ensure text_buffer has enough characters to fill display buffer
        total_buffer_size = self.rows * self.cols
        if self.menu_buffer_size < total_buffer_size:
            self.extra_spaces = total_buffer_size - self.menu_buffer_size
            self.text_buffer += " " * self.extra_spaces
            self.menu_buffer_size = self.menu_buffer_size + self.extra_spaces
        else:
            self.extra_spaces = 0
        self.menu_buffer = list(range(self.menu_buffer_size))

        # Slicing menu_buffer to create the display buffer
        self.display_buffer = self.menu_buffer[
            self.display_buffer_position : self.display_buffer_position
            + total_buffer_size
        ]
        new_rows_list = []

        for i in range(self.rows):
            rownew = self.text_buffer[
                self.display_buffer[self.cols * i] : self.display_buffer[
                    self.cols * i + self.cols - 1
                ]
                + 1
            ]
            new_rows_list.append(rownew)
        return new_rows_list

    def update_buffer(self, text):
        self.refresh_area = (0, self.rows * self.cols)
        past_buffer_cursor = self.menu_buffer_cursor
        txt_buf_size = self.menu_buffer[-1] + 1
        if text == "nav_d" or text == "nav_r":
            if text == "nav_d":
                self.menu_buffer_cursor += self.cols
            else:
                self.menu_buffer_cursor += 1
            self.refresh_area = (
                (past_buffer_cursor - self.display_buffer_position) % self.cols
                + ((past_buffer_cursor - self.display_buffer_position) // self.cols)
                * self.cols,
                ((self.menu_buffer_cursor - self.display_buffer_position) // self.cols)
                * self.cols
                + self.cols,
            )

            if self.menu_buffer_cursor >= self.buffer_length:
                self.menu_buffer_cursor = 0
                self.display_buffer_position = 0
                self.refresh_area = (0, self.rows * self.cols)
            elif self.menu_buffer_cursor > self.display_buffer[-1]:
                self.display_buffer_position += self.cols
                self.refresh_area = (0, self.rows * self.cols)
        elif text == "nav_u" or text == "nav_l" or text == "nav_b":
            going_bottom = False

            if text == "nav_u":
                self.menu_buffer_cursor -= self.cols
            else:
                self.menu_buffer_cursor -= 1
            if text == "nav_b":
                self.refresh_area = (
                    (self.menu_buffer_cursor - self.display_buffer_position) % self.cols
                    + (
                        (self.menu_buffer_cursor - self.display_buffer_position)
                        // self.cols
                    )
                    * self.cols,
                    self.rows * self.cols,
                )
            else:
                self.refresh_area = (
                    (self.menu_buffer_cursor - self.display_buffer_position) % self.cols
                    + (
                        (self.menu_buffer_cursor - self.display_buffer_position)
                        // self.cols
                    )
                    * self.cols,
                    ((past_buffer_cursor - self.display_buffer_position) // self.cols)
                    * self.cols
                    + self.cols,
                )

            if self.menu_buffer_cursor < 0:
                self.refresh_area = (0, self.rows * self.cols)
                going_bottom = True
                if txt_buf_size <= self.rows * self.cols:
                    self.menu_buffer_cursor = self.buffer_length - 1
                else:
                    self.menu_buffer_cursor = txt_buf_size - self.no_last_spaces - 1
                self.display_buffer_position = txt_buf_size - self.rows * self.cols
            elif self.menu_buffer_cursor < self.display_buffer[0]:
                self.refresh_area = (0, self.rows * self.cols)
                self.display_buffer_position -= self.cols
            if text == "nav_b":
                if (
                    txt_buf_size - self.no_last_spaces - self.extra_spaces - 1
                ) == self.display_buffer[-self.cols] and (
                    txt_buf_size - self.no_last_spaces - self.extra_spaces - 1
                ) >= self.rows * self.cols:
                    self.display_buffer_position -= self.cols
                    self.refresh_area = (0, self.rows * self.cols)
                self.text_buffer = (
                    self.text_buffer[: self.menu_buffer_cursor]
                    + self.text_buffer[self.menu_buffer_cursor + 1 :]
                )
                if going_bottom == False:
                    self.text_buffer_nospace -= 1
                    if self.text_buffer_nospace < 0:
                        self.text_buffer_nospace = 0
        elif text == "AC":
            self.all_clear()
        else:
            past_buffer_cursor = self.menu_buffer_cursor
            self.text_buffer = (
                self.text_buffer[0 : self.menu_buffer_cursor]
                + text
                + self.text_buffer[self.menu_buffer_cursor : txt_buf_size]
            )
            self.text_buffer_nospace += len(text)
            self.menu_buffer_size += len(text)
            self.menu_buffer = list(range(self.menu_buffer_size))
            self.menu_buffer_cursor += len(text)
            self.refresh_area = (
                (past_buffer_cursor - self.display_buffer_position) % self.cols
                + ((past_buffer_cursor - self.display_buffer_position) // self.cols)
                * self.cols,
                self.rows * self.cols,
            )

            if self.menu_buffer_cursor > self.display_buffer[-1]:
                self.display_buffer_position = (
                    self.menu_buffer_cursor
                    - self.menu_buffer_cursor % self.cols
                    - ((self.rows - 1) * self.cols)
                )
                self.refresh_area = (0, self.rows * self.cols)
        self.text_buffer = self.text_buffer[0 : self.text_buffer_nospace] + "𖤓"

    def all_clear(self):
        self.refresh_area = (0, self.rows * self.cols)
        self.text_buffer = "𖤓"
        self.text_buffer_nospace = 0
        self.menu_buffer_size = 1
        self.menu_buffer = list(range(self.menu_buffer_size))
        self.menu_buffer_cursor = 0
        self.display_buffer_position = 0
        self.no_last_spaces = 0

    def ref_ar(self):
        return self.refresh_area

    def cursor(self):
        return self.menu_buffer_cursor - self.display_buffer_position
    

    
