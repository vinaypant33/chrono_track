import tkinter as tk
from tkinter import ttk
import sys
import threading as th
from ctypes import windll
import time
from datetime import time
import textwrap



### Classes for Custom Controls ####  
'''
make the custom list for the current tasks - task naem with the closer and other button cose adn completed button
another frame with the scrollable frame and data which is to be saved 
make the textbox multiline - in any case the textbox text sentences are increased.  
 

'''

class current_text():


    def wrap_text(self , text  , width):
        self.current_text =  "\n".join(textwrap.wrap(text, width=width))



    def __init__(self , master_control , text_name , text_id , char_length = 64):
        self.master_control = master_control
        self.text_name = text_name
        self.text_i  = text_id
        self.char_length  = char_length
        


        self.current_text  = ""


        if char_length <= 64:
            self.current_height  = 3
            self.current_text = self.text_name
        elif    60 <= char_length <= 100:
            self.current_height = 6
            self.wrap_text(self.text_name , 60)
            
        elif char_length >= 105:
            self.current_height = 7
            self.wrap_text(self.text_name , 90)
           

        
        self.main_frame  = tk.Frame(self.master_control , width=10 , height= self.current_height , background="white")
        self.main_frame.pack_propagate(0)

        self.text_label  = tk.Label(self.main_frame , text=self.current_text , height=self.current_height , width=49 , justify="left", anchor="w")
        self.start_stop_button  = tk.Button(self.main_frame , text="St")
        self.pause_button  = tk.Button(self.main_frame , text="Pa")


        self.main_frame.pack(padx=5 , pady = 5 )

        self.text_label.grid(row  = 0 , column=  0 , columnspan=4 , rowspan=2 ,sticky=tk.W)
        self.start_stop_button.grid(row= 0 , column= 5 ,  columnspan=1 , sticky=tk.N)
        self.pause_button.grid(row = 1  , column=5 , columnspan=1   ,sticky=tk.N )


        


    



### Constants ###
application_base = '#1E1E1E'
controls_base = '#2F2F2F'
controls_non_use_base = '#101010'
controls_base_2 = '#1F1F1F'
icons_front_color = '#A7A7A7'
icons_front_color_2 = '#458DFF'
other_icons_back_color = '#222B39'
red_color  = "#ff0000"
white_color  = '#ffffff'
current_text_id  = 0
text_class_data = []



app_width  = 400
app_height  = 600
minimized  = True
main_x = 0 
main_y = 0
timer_seconds  = 0
timer_minutes = 0 
timer_hours = 0
actual_timer  = 0
text_font=("Futura", 50 , 'bold')
entry_font = ("helvetica" , 14)
class_task_font = ("Helvetica" , 15)


window  = tk.Tk()

### Window details ###
window.overrideredirect(True)  # titlebar removed
screen_height  = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()



current_x_location  = ( screen_width // 2 )  - (app_width // 2)
current_y_locaiton  = (screen_height // 2) - (app_height // 2)

window.geometry(f"{app_width}x{app_height}+{current_x_location}+{current_y_locaiton}")




###### Functions ######### 

def set_appwindow(root):
        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())

def close_application():
    window.destroy()
    sys.exit()
    
def minimize_application():
    window.overrideredirect(False)
    window.wm_iconify()
    window.bind('<FocusIn>' , on_deiconify)

def on_deiconify(event):
    if window.wm_state() =='normal' and window.overrideredirect() != True:
            window.overrideredirect(True)
            set_appwindow(window)

def mouse_click(event):
    # print(event)
    global main_x
    global main_y
    main_x  = event.x
    main_y = event.y

def mouse_move(event):
    # print(event)
    global main_x 
    global main_y 
    main_x = main_x
    main_y = main_y
    deltax = event.x - main_x
    deltay = event.y - main_y
    x_location = window.winfo_x() + deltax
    y_location  = window.winfo_y() + deltay
    window.geometry(f"{app_width}x{app_height}+{x_location}+{y_location}")


def add_text_task():

    char_length  = task_name_textbox.get()
    if len(char_length) > 0 : 
        global current_text_id
        current_text_id  += 1
        text_class_data.append(current_text_id)
        text_control  = current_text(scrollable_frame , char_length , current_text_id , len(char_length))
        task_name_textbox.delete( 0 , tk.END)

    
def add_text_task_temp(event):
     
    char_length  = task_name_textbox.get()
    if len(char_length) > 0 : 
        global current_text_id
        current_text_id  += 1
        text_class_data.append(current_text_id)
        text_control  = current_text(scrollable_frame , char_length , current_text_id , len(char_length))
        task_name_textbox.delete( 0 , tk.END)
   






#### Title bar and related buttons ( minimize and close )
title_bar  = tk.Frame(window , height=30 , width=app_width , background=controls_base)
close_button  = tk.Button(title_bar , text='\u2716' , command=close_application)
minimized_button  =tk.Button(title_bar , text=u'\u2014' , command=minimize_application )
application_name  = tk.Label(title_bar , text  = "Chrono Track" )



##### Application Main Controls  #######  
'''
Only Tkinter is being used for this - Timer would be used instead of clock animation

'''
timer_frame  = tk.Frame(window , height=app_height / 3 , width=app_width , background = red_color)
task_frame = tk.Frame(window , height=app_height - app_height / 3 , width=app_width , background=white_color)
actual_timer  = tk.Label(timer_frame , text="00:00:00" , font=text_font )
add_button = tk.Button(task_frame ,  text="+"  , height=2 , width=4 , command=add_text_task)
canvas_frame = tk.Frame(task_frame , background=red_color , height=329 , width=400)
canvas = tk.Canvas(canvas_frame , background=red_color , height=329 , width = 400)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

task_name_textbox = tk.Entry(task_frame , bd = 1 , relief="sunken" , width=59 , background= icons_front_color_2 , font=entry_font)


##### Configuring the controls #### 
def button_styles(master , height , width , background , foreground , activebg , activefg , bd = 0 ):
    master.configure(height=height , width=width , background=background , foreground=foreground , activebackground=activebg , activeforeground=activefg , bd = 0 , relief='flat')

window.configure(background=application_base)
title_bar.pack_propagate(False)
# button_styles(close_button , 1 , 1 , icons_front_color , None , None , None , 0 )
close_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd=0 , activebackground=red_color , activeforeground=white_color )
minimized_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd = 0 , activebackground=other_icons_back_color , activeforeground=white_color)
application_name.configure(background=controls_base , foreground=white_color)
add_button.configure(background=controls_base , foreground=white_color , activebackground=red_color , activeforeground=white_color , relief='flat' , bd = 0)
canvas_frame.pack_propagate(0)
timer_frame.pack_propagate(0)
task_frame.pack_propagate(0)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


##### Binding the controls ##### 
title_bar.bind("<ButtonPress-1>" , mouse_click)
title_bar.bind("<B1-Motion>" , mouse_move)
close_button.bind("<Enter>" , lambda x : close_button.configure(background=red_color))
close_button.bind("<Leave>" , lambda x  :  close_button.configure(background=controls_base))
minimized_button.bind("<Enter>" , lambda x : minimized_button.configure(background=other_icons_back_color))
minimized_button.bind("<Leave>" , lambda x  : minimized_button.configure(background=controls_base))
scrollable_frame.bind("<Configure>", on_configure)
task_name_textbox.bind("<Return>" , add_text_task_temp)


##### Packing the controls #### 
title_bar.pack()
close_button.pack(side=tk.RIGHT ,padx=(0,0) , fill=tk.Y)
minimized_button.pack(side=tk.RIGHT , padx=(0 , 0) , fill=tk.Y)
application_name.pack(side = tk.LEFT , padx=(5 , 0))

timer_frame.pack()
task_frame.pack()
actual_timer.pack(pady=(48 , 0))
add_button.pack(side = tk.RIGHT , pady=(2) , padx=(2) , anchor=tk.NE)
canvas_frame.place(x=0 , y = 40)
scrollbar.pack(side="right", fill="y")
# canvas_frame.pack(side="left" , fill="both" , expand=True)
canvas.pack()

canvas.configure(yscrollcommand=scrollbar.set)


task_name_textbox.pack(side=tk.LEFT  , padx=(2 , 0) , pady=(9 , 0) , anchor=tk.NE)



window.mainloop()