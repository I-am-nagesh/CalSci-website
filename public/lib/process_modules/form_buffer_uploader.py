class Tbf:
    def __init__(self, disp_out, chrs, f_b):
        self.disp_out=disp_out
        self.chrs=chrs
        self.f_b=f_b
        self.disp_out.clear_display()

    def refresh(self, state="default"):
        buf=self.f_b.buffer()
        ref_rows=self.f_b.ref_ar()
        for i in range(ref_rows[0], ref_rows[1]):
            self.disp_out.set_page_address(i)
            self.disp_out.set_column_address(0)
            if "inp_" in buf[i]:
                buf_current="=>"+self.f_b.inp_list()[self.f_b.buffer()[i]][self.f_b.inp_display_position():self.f_b.inp_display_position()+self.f_b.inp_cols()]
            else:
                buf_current = buf[i]
            if len(buf_current)<self.f_b.inp_cols():
                    buf_current+=" "*(self.f_b.inp_cols()-len(buf_current)+2)
            j_counter=0
            for j in buf_current:
                if i == self.f_b.cursor() and "inp_" not in buf[i]:
                    chtr_byte_data=self.chrs.invert_letter(j)
                    cursor_line=0b11111111
                    for k in chtr_byte_data:
                        self.disp_out.write_data(k)
                    self.disp_out.write_data(cursor_line)
                elif i == self.f_b.cursor() and "inp_" in buf[i]:
                    if j_counter+self.f_b.inp_display_position()==self.f_b.inp_cursor()+2:
                        chtr_byte_data=self.chrs.invert_letter(j)
                        cursor_line=0b11111111
                        for k in chtr_byte_data:
                            self.disp_out.write_data(k)
                        self.disp_out.write_data(cursor_line)
                    else:
                        chtr_byte_data=self.chrs.Chr2bytes(j)
                        cursor_line=0b00000000
                        for k in chtr_byte_data:
                            self.disp_out.write_data(k)
                        self.disp_out.write_data(cursor_line)
                else:
                    chtr_byte_data=self.chrs.Chr2bytes(j)
                    cursor_line=0b00000000
                    for k in chtr_byte_data:
                        self.disp_out.write_data(k)
                    self.disp_out.write_data(cursor_line)
                j_counter+=1
        
        self.disp_out.set_page_address(7)
        self.disp_out.set_column_address(0)
        j_counter=0
        for j in state:
            chtr=j
            chtr_byte_data=self.chrs.invert_letter(chtr)
            cursor_line=0b11111111
            for k in chtr_byte_data:
                self.disp_out.write_data(k)
            self.disp_out.write_data(cursor_line)
            j_counter+=1