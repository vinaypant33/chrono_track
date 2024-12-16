import tkinter as tk
import sys
import threading as th
from ctypes import windll


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


app_width  = 400
app_height  = 600
minimized  = True
main_x = 0 
main_y = 0




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


#### Title bar and related buttons ( minimize and close )
title_bar  = tk.Frame(window , height=30 , width=app_width , background=controls_base)
close_button  = tk.Button(title_bar , text='\u2716' , command=close_application)
minimized_button  =tk.Button(title_bar , text=u'\u2014' , command=minimize_application )
application_name  = tk.Label(title_bar , text  = "Chrono Track" )




##### Configuring the controls #### 
def button_styles(master , height , width , background , foreground , activebg , activefg , bd = 0 ):
    master.configure(height=height , width=width , background=background , foreground=foreground , activebackground=activebg , activeforeground=activefg , bd = 0 , relief='flat')

window.configure(background=application_base)
title_bar.pack_propagate(False)
# button_styles(close_button , 1 , 1 , icons_front_color , None , None , None , 0 )
close_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd=0 , activebackground=red_color , activeforeground=white_color )
minimized_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd = 0 , activebackground=other_icons_back_color , activeforeground=white_color)
application_name.configure(background=controls_base , foreground=white_color)




##### Binding the controls ##### 
title_bar.bind("<ButtonPress-1>" , mouse_click)
title_bar.bind("<B1-Motion>" , mouse_move)
close_button.bind("<Enter>" , lambda x : close_button.configure(background=red_color))
close_button.bind("<Leave>" , lambda x  :  close_button.configure(background=controls_base))
minimized_button.bind("<Enter>" , lambda x : minimized_button.configure(background=other_icons_back_color))
minimized_button.bind("<Leave>" , lambda x  : minimized_button.configure(background=controls_base))


##### Packing the controls #### 
title_bar.pack()
close_button.pack(side=tk.RIGHT ,padx=(0,0) , fill=tk.Y)
minimized_button.pack(side=tk.RIGHT , padx=(0 , 0) , fill=tk.Y)
application_name.pack(side = tk.LEFT , padx=(5 , 0))




window.mainloop()