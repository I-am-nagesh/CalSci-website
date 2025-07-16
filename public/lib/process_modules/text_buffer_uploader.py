class Tbf:
    def __init__(self, disp_out, chrs, t_b):
        self.disp_out=disp_out
        self.chrs=chrs
        self.t_b=t_b
        self.disp_out.clear_display()
    def update(self, t_b_new):
        self.t_b=t_b_new
    def refresh(self, state="default"):
        buf=self.t_b.buffer()
        ref_ar=self.t_b.ref_ar()
        for i in range(ref_ar[0]//self.t_b.cols, ref_ar[1]//self.t_b.cols):
            self.disp_out.set_page_address(i)
            self.disp_out.set_column_address(0)      
            if buf[i].strip() != "" or self.t_b.cursor()//self.t_b.cols==i:
                j_counter=0
                for j in buf[i]:
                    chtr=j
                    cursor_line=0b00000000
                    chtr_byte_data=self.chrs.Chr2bytes(chtr)
                    if j_counter+i*self.t_b.cols==self.t_b.cursor():
                        chtr_byte_data=self.chrs.invert_letter(chtr)
                        cursor_line=0b11111111
                    for k in chtr_byte_data:
                        self.disp_out.write_data(k)
                    self.disp_out.write_data(cursor_line)
                    j_counter+=1
            else   :
                for k in range(6):
                    self.disp_out.write_data(0b00000000)
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