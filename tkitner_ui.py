import tkinter as tk
from tkinter import ttk
import sys
import threading as th
from ctypes import windll
from time import sleep
from datetime import time
import textwrap

from tkinter import messagebox




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
text_details = [] # Name and id number and the time spent in the data
timer_working  = True 


#### Code for the local database : 
## Specific imports for the database : 
import sqlite3
import datetime

conn  = sqlite3.connect('chrono_track.db')
c  = conn.cursor()


def saving_details():
    conn.commit()

def inserting_data():
    clean_table()
    
    for each in text_details:
        c.execute('INSERT INTO task (task) VALUES ("%s" );' %(each))
    saving_details()
    # c.execute('INSERT INTO task (task) VALUES ("%d" , "%s" , "%s" );' %( text_details['task_id'] , text_details['task_name'] , text_details['task_time']))
    # saving_details()
    # print("Details Saved")
    window.after(3000 , inserting_data)


def clean_table():
    c.execute("DELETE FROM task;")


def loading_data():


    try:

        c.execute("SELECT * FROM task;")
        list  = c.fetchall()
        # for data in list:
        #     print(data)
        
        for each in list:
            current_id  = str(each).split(",")[0]
            current_task_name  = str(each).split(",")[1]
            current_time  = str(each).split(",")[2]
            char_length = len(current_task_name)
            text_control = current_text(scrollable_frame , current_task_name , current_id , char_length  , current_time) 

    except Exception as loading_error:
        messagebox.showerror("Chrono Track" , "Unable to Load the database")
        
    # char_length  = task_name_textbox.get()
    # if len(char_length) > 0 : 
    #     global current_text_id
    #     current_text_id  += 1
    #     text_details.append(str(current_text_id)+","+char_length +","+"00:00:00" )
    #     # for each in text_details:
    #     #     print(each)
    #     text_control  = current_text(scrollable_frame , char_length , current_text_id , len(char_length))
    #     task_name_textbox.delete( 0 , tk.END)
        
        # for each in text_details:
        #     print(each)
    
    



### Classes for Custom Controls ####  

class current_text():

    def wrap_text(self , text  , width):
        self.current_text =  "\n".join(textwrap.wrap(text, width=width))

    def timer_started(self):
        global window
        global timer_working
        global actual_timer

        self.current_seconds+=1

        if self.current_seconds == 60:
            self.current_seconds = 0
            self.current_minutes+=1
        
        if self.current_minutes == 60:
            self.current_hour+=1
            self.current_minutes = 0
            
        self.current_list_time  = f"{self.current_hour}:{self.current_minutes}:{self.current_seconds}"
        
        actual_timer.configure(text=f"{self.current_hour:02}:{self.current_minutes:02}:{self.current_seconds:02}")

        # for time in text_details:
        #     print(time)
        # for time in text_details:
        #     print(str(time[0].split(",")[2]))
        # timer_working = True
        index  = len(text_details)
        # print(index)

        # for i in range(index):
        #     print(text_details[i].split(",")[2])
        # print(self.text_i)
        for i in range(index):
            if int(text_details[i].split(",")[0]) == self.text_i:
                text_details[i] =  str(self.text_i)+","+str(self.text_name)+","+str(self.current_list_time)


        if timer_working == False:
            window.after(1000 , self.timer_started)
        else:
            actual_timer.configure(text="00:00:00")

        

    def timer_stopped (self):
        global text_details
        global actual_timer
        
        
        # for each in text_details:
        #     print(each)
       

        # for each in text_details:
        #     # print(each[0])
        #     if int(each[0]) == self.text_i:
        #         text_details.pop(int(each[0]))
            # print(len(text_details))

        # if self.text_i in text_details:
        #     text_details[self.text_i]["task_time"] = str(str(self.current_hour) + ":" + str(self.current_minutes) + ":" + str(self.current_seconds))

        # text_details.update({"task_id" : self.text_i , "task_name" : self.text_name , "task_time" : str(str(self.current_hour) + ":" + str(self.current_minutes) + ":" + str(self.current_seconds) )})
       
        
        actual_timer.configure(text="00:00:00")


    def start_stop(self):
        global timer_working
        if self.working == True:
            if timer_working == True:
                self.start_stop_button.configure(text="\u23F9")
                self.working = False
                self.text_label.configure(background=other_icons_back_color)
                timer_working = False
                self.timer_started()
        elif self.working == False: 
            if timer_working == False:
                self.start_stop_button.configure(text="\u25B6")
                self.text_label.configure(background=application_base)
                self.working = True
                timer_working = True
                self.timer_stopped()


    
    def delete_item_data(self):
        self.main_frame.destroy()


    def __init__(self , master_control , text_name , text_id , char_length = 64 , current_time = "00:00:00" ):
        self.master_control = master_control
        self.text_name = text_name
        self.text_i  = text_id
        self.char_length  = char_length
        
        # print(self.text_i)

        global timer_working
        
        current_time  = current_time.strip("'")
       

        self.current_hour  = int(str(current_time.split(":")[0]))
        self.current_minutes = int(str(current_time.split(":")[1]))
        self.current_seconds = int(str(current_time.split(":")[2]))

        self.working  = True
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

        self.main_frame  = tk.Frame(self.master_control , width=9 , height= self.current_height , background=application_base , bd=1 )
        self.main_frame.pack_propagate(0)

        self.text_label  = tk.Label(self.main_frame , text=self.current_text , height=self.current_height , width=49 , justify="left", anchor="w" , background=application_base , font=button_font , foreground=white_color)
        self.start_stop_button  = tk.Button(self.main_frame , text="\u25B6" , background=controls_base , foreground=icons_front_color_2 , activebackground=red_color , activeforeground=white_color , relief="sunken", bd = 2 , command=self.start_stop)
        ## Stp Button \u23F9

        self.delete_button  = tk.Button(self.main_frame , text="\U0001F5D1" , background=controls_base , foreground=icons_front_color_2 , activebackground=red_color , activeforeground=white_color , relief="sunken", bd = 2 , command=self.delete_item_data)
        self.main_frame.pack(padx=5 , pady = 5 )

        self.text_label.grid(row  = 0 , column=  0 , columnspan=4 , rowspan=2 ,sticky=tk.W)
        self.start_stop_button.grid(row= 0 , column= 5 ,  columnspan=1 , sticky=tk.NSEW )
        self.delete_button.grid(row = 1  , column=5 , columnspan=1   , sticky=tk.NSEW )



app_width  = 400
app_height  = 600
minimized  = True
main_x = 0 
main_y = 0
timer_seconds  = 0
timer_minutes = 0 
timer_hours = 0
actual_timer  = 0
text_font=("Futura", 55 , 'bold')
entry_font = ("Helvetica" , 10)
class_task_font = ("Helvetica" , 15)
button_font  = ("Helvetica" , 8 , "bold")



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
        text_details.append(str(current_text_id)+","+char_length +","+"00:00:00" )
        text_control  = current_text(scrollable_frame , char_length , current_text_id , len(char_length))
        task_name_textbox.delete( 0 , tk.END)

    
def add_text_task_temp(event):
     
    char_length  = task_name_textbox.get()
    if len(char_length) > 0 : 
        global current_text_id
        current_text_id  += 1
        text_details.append(str(current_text_id)+","+char_length +","+"00:00:00" )
        # for each in text_details:
        #     print(each)
        text_control  = current_text(scrollable_frame , char_length , current_text_id , len(char_length))
        task_name_textbox.delete( 0 , tk.END)
        
        # for each in text_details:
        #     print(each)
        
        



#### Title bar and related buttons ( minimize and close )
title_bar  = tk.Frame(window , height=30 , width=app_width , background=controls_base)
close_button  = tk.Button(title_bar , text='\u2716' , command=close_application)
minimized_button  =tk.Button(title_bar , text=u'\u2014' , command=minimize_application )
application_name  = tk.Label(title_bar , text  = "Chrono Track" )



##### Application Main Controls  #######  
'''
Only Tkinter is being used for this - Timer would be used instead of clock animation

'''
timer_frame  = tk.Frame(window , height=app_height / 3 , width=app_width , background=application_base )
task_frame = tk.Frame(window , height=app_height - app_height / 3 , width=app_width , background=controls_base ) 
actual_timer  = tk.Label(timer_frame , text="00:00:00" , font=text_font , background=application_base , foreground=icons_front_color , relief="sunken" , bd = 1  )
add_button = tk.Button(task_frame ,  text="\u2795"  , height=2 , width=4 , command=add_text_task , font=button_font, foreground=red_color)
canvas_frame = tk.Frame(task_frame  , height=329 , width=400 ,background=application_base)
canvas = tk.Canvas(canvas_frame , background=white_color,  height=329 , width = 400)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview )
scrollable_frame = tk.Frame(canvas )
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") 

task_name_textbox = tk.Entry(task_frame , bd = 2 , relief="sunken" , width=55 , background= controls_base , font=entry_font , foreground=white_color , insertbackground=white_color)
 

##### Configuring the controls #### 
def button_styles(master , height , width , background , foreground , activebg , activefg , bd = 0 ):
    master.configure(height=height , width=width , background=background , foreground=foreground , activebackground=activebg , activeforeground=activefg , bd = 0 , relief='flat')

window.configure(background=application_base)
title_bar.pack_propagate(False)
# button_styles(close_button , 1 , 1 , icons_front_color , None , None , None , 0 )
close_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd=0 , activebackground=red_color , activeforeground=white_color )
minimized_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd = 0 , activebackground=other_icons_back_color , activeforeground=white_color)
application_name.configure(background=controls_base , foreground=white_color)
add_button.configure(background=controls_base , foreground=icons_front_color_2 , activebackground=red_color , activeforeground=white_color , relief="sunken", bd = 2)
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


task_name_textbox.pack(side=tk.LEFT  , padx=(3 , 0) , pady=(9 , 0) , anchor=tk.NE)



# Call the database and load the details in the application and keep recurring the data and save the details in the database : 
window.after(5000 , inserting_data)
loading_data()
window.mainloop()