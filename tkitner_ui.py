import tkinter as tk
import sys
import threading as th



### Constants ###
application_base = '#1E1E1E'
controls_base = '#2F2F2F'
controls_non_use_base = '#101010'
controls_base_2 = '#1F1F1F'
icons_front_color = '#A7A7A7'
icons_front_color_2 = '#458DFF'
other_icons_back_color = '#222B39'
red_color  = "#F72C5B"

app_width  = 600
app_height  = 400


window  = tk.Tk()

### Window details ###
window.overrideredirect(True)  # titlebar removed
screen_height  = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()



current_x_location  = ( screen_width // 2 )  - (app_width // 2)
current_y_locaiton  = (screen_height // 2) - (app_height // 2)

window.geometry(f"{app_width}x{app_height}+{current_x_location}+{current_y_locaiton}")




###### Functions ######### 

def close_application():
    window.destroy()
    sys.exit()
    




#### Title bar and related buttons ( minimize and close )
title_bar  = tk.Frame(window , height=30 , width=app_width , background=controls_base)
close_button  = tk.Button(title_bar , text='\u2716' , command=close_application)






##### Configuring the controls #### 
def button_styles(master , height , width , background , foreground , activebg , activefg , bd = 0 ):
    master.configure(height=height , width=width , background=background , foreground=foreground , activebackground=activebg , activeforeground=activefg , bd = 0 , relief='flat')

window.configure(background=application_base)
title_bar.pack_propagate(False)
# button_styles(close_button , 1 , 1 , icons_front_color , None , None , None , 0 )
close_button.configure(background=controls_base , foreground=icons_front_color , relief='flat' , bd=0 , activebackground=red_color , activeforeground=icons_front_color_2 )





##### Binding the controls ##### 




##### Packing the controls #### 
title_bar.pack()
close_button.pack(side=tk.RIGHT ,padx=(0,0))





window.mainloop()