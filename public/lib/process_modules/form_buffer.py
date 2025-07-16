class Form:
    def __init__(self, rows=7, menu_cursor=0, menu_display_position=0, input_list={"inp_0":" ", "inp_1":" ", "inp_2":" "}, form_list=["label_0", "inp_0", "label_1", "inp_1", "label_2", "inp_2"], input_cursor=0, input_display_position=0, input_cols=21-2):
        self.rows=rows
        self.input_list=input_list
        self.form_list=form_list
        self.input_cursor=input_cursor
        self.input_display_position=input_display_position
        self.input_cols=input_cols
        self.actual_rows=self.rows if len(self.form_list) >= self.rows else len(self.form_list)
        self.refresh_rows=(0,self.actual_rows)
        self.menu_display_size=self.actual_rows
        self.menu_display_position=menu_display_position
        self.display_buffer=self.form_list[self.menu_display_position:self.menu_display_position+self.menu_display_size]
        self.menu_cursor=menu_cursor
        self.display_cursor=self.menu_cursor-self.menu_display_position
    def update_buffer(self, inp):

        if inp=="nav_d":
            self.menu_cursor+=1

            if self.menu_cursor==len(self.form_list):
                self.menu_cursor=0
                self.menu_display_position=0
                # refresh_rows=(0,rows)
                self.refresh_rows=(0,self.actual_rows)

            elif self.menu_cursor-self.menu_display_position==self.actual_rows:
                self.menu_display_position+=1
                # refresh_rows=(0,rows)
                self.refresh_rows=(0,self.actual_rows)

            else:
                self.refresh_rows=(self.menu_cursor-1-self.menu_display_position,self.menu_cursor-self.menu_display_position+1)
            self.input_cursor=0
            self.input_display_position=0

        elif inp=="nav_u":
            self.menu_cursor-=1

            if self.menu_cursor<0:
                self.menu_cursor=len(self.form_list)-1
                self.menu_display_position=len(self.form_list)-self.actual_rows
                # refresh_rows=(0,rows)
                self.refresh_rows=(0,self.actual_rows)

            elif self.menu_cursor<self.menu_display_position:
                self.menu_display_position-=1
                # refresh_rows=(0,rows)
                self.refresh_rows=(0,self.actual_rows)

            else:
                self.refresh_rows=(self.menu_cursor-self.menu_display_position,self.menu_cursor-self.menu_display_position+2)

            self.input_cursor=0
            self.input_display_position=0

        else:
            if "inp_" in self.form_list[self.menu_cursor]:
                self.refresh_rows=(self.menu_cursor-self.menu_display_position,self.menu_cursor-self.menu_display_position+1)
                if inp == "nav_r":
                    self.input_cursor+=1

                    if self.input_cursor==len(self.input_list[self.form_list[self.menu_cursor]]):
                        self.input_cursor=0
                        self.input_display_position=0

                    elif self.input_cursor==self.input_display_position+self.input_cols:
                        self.input_display_position+=1
                    
                elif inp == "nav_l" or inp == "nav_b":
                    self.input_cursor-=1
                    
                    if self.input_cursor<0:
                        self.input_cursor=len(self.input_list[self.form_list[self.menu_cursor]])-1
                        self.input_display_position=len(self.input_list[self.form_list[self.menu_cursor]])-self.input_cols
                        if self.input_display_position<0:
                            self.input_display_position=0

                    elif self.input_cursor<self.input_display_position:
                        self.input_display_position-=1

                    if inp == "nav_b" and self.input_cursor!=len(self.input_list[self.form_list[self.menu_cursor]])-1:
                        self.input_list[self.form_list[self.menu_cursor]]=self.input_list[self.form_list[self.menu_cursor]][:self.input_cursor]+self.input_list[self.form_list[self.menu_cursor]][self.input_cursor+1:]
                        if len(self.input_list[self.form_list[self.menu_cursor]]) > self.input_cols and len(self.input_list[self.form_list[self.menu_cursor]][self.input_display_position:]) < self.input_cols:
                            self.input_display_position=len(self.input_list[self.form_list[self.menu_cursor]])-self.input_cols
                        elif len(self.input_list[self.form_list[self.menu_cursor]]) <=self.input_cols:
                            self.input_display_position=0
                elif inp == "AC":
                    self.input_list[self.form_list[self.menu_cursor]]=" "
                    self.input_cursor=0
                    self.input_display_position=0

                        
                else:
                    if len(inp)>1:
                        for chr in inp:
                            self.input_list[self.form_list[self.menu_cursor]]=self.input_list[self.form_list[self.menu_cursor]][:self.input_cursor]+chr+self.input_list[self.form_list[self.menu_cursor]][self.input_cursor:]
                            self.input_cursor+=len(chr)
                
                            if self.input_cursor==self.input_display_position+self.input_cols:
                                self.input_display_position+=1
                    else:
                        self.input_list[self.form_list[self.menu_cursor]]=self.input_list[self.form_list[self.menu_cursor]][:self.input_cursor]+inp+self.input_list[self.form_list[self.menu_cursor]][self.input_cursor:]
                        self.input_cursor+=len(inp)
                    
                        if self.input_cursor==self.input_display_position+self.input_cols:
                            self.input_display_position+=1
                self.input_list[self.form_list[self.menu_cursor]]=self.input_list[self.form_list[self.menu_cursor]].rstrip()+" "

        self.display_buffer=self.form_list[self.menu_display_position:self.menu_display_position+self.menu_display_size]
        self.display_cursor=self.menu_cursor-self.menu_display_position
    
    def ref_ar(self):
        return self.refresh_rows
    
    def buffer(self):
        return self.display_buffer
    
    def cursor(self):
        return self.display_cursor
    
    def act_rows(self):
        return self.actual_rows
    
    def inp_cursor(self):
        return self.input_cursor
    
    def inp_list(self):
        return self.input_list
    
    def inp_display_position(self):
        return self.input_display_position
    
    def inp_cols(self):
        return self.input_cols
    
    def update(self):
        self.actual_rows=self.rows if len(self.form_list) >= self.rows else len(self.form_list)
        self.refresh_rows=(0,self.actual_rows)
        self.menu_display_size=self.actual_rows
        self.menu_display_position=0
        self.display_buffer=self.form_list[self.menu_display_position:self.menu_display_position+self.menu_display_size]
        self.menu_cursor=0
        self.display_cursor=self.menu_cursor-self.menu_display_position
        
    def update_label(self,index_label, new_label):
        self.form_list[index_label] = new_label
    

def test2():
    form = Form()

    while True:
        print("Current form_list:", form.form_list)
        print("Current input_list:", form.inp_list())
        print("\n")

        for i in range(form.act_rows()):
            if "inp_" in form.buffer()[i]:
                print(f"{i}: Input Field ({form.buffer()[i]}): {form.inp_list()[form.buffer()[i]][form.inp_display_position():form.inp_display_position() + form.inp_cols()]}")
            else:
                print(f"{i}: Label: {form.buffer()[i]}")

        inp = input("Enter command (or text): ")
        form.update_buffer(inp)

        if inp == "ok":
            current_input_key = form.buffer()[form.cursor()]
            if "inp_" in current_input_key:
                input_text = form.inp_list()[current_input_key].strip()
                label_index = form.form_list.index(current_input_key) - 1
                form.update_label(label_index, input_text)
                form.input_list[current_input_key] = " "  
                print(f"Label updated: {form.form_list[label_index]}")
                print(f"Input field cleared: {current_input_key}")
