import customtkinter as ct
import tkinter as tk
from PIL import Image
import pandas as pd


app = ct.CTk()
app.resizable(False, False)
app.geometry("1200x800+420+120")
app.title("Hunt The Wumpus")
df = pd.read_csv("Users.csv")
count = 4
ct.set_appearance_mode("Dark")  
ct.set_default_color_theme("blue")   


def write_csv():
    df.loc[len(df)] = [username, 0, 0]
    #SCORE
    #TIME
    df.to_csv('Users.csv', index=False)
    

def instructions_button():
    app.withdraw()
    instructions_window = ct.CTkToplevel(app)
    instructions_window.title("Instructions")
    instructions_window.geometry("1200x800+420+120")
    instructions_window.resizable(False, False)
    
    instructions_frame = ct.CTkFrame(instructions_window, width=960, height=640)
    instructions_frame.place(relx=0.1, rely=0.1)
    instructions_frame.pack_propagate(False)
   
    username_prompt = ct.CTkLabel(instructions_frame, text="Please enter your username and press enter:", font=("", 20))
    username_prompt.place(x=50, y=50)  
    
    usernames = df['Name'].to_list()
    score = df['Score'].to_list()
    time = df['Time'].to_list()
    
    def enter():
        global username, count
        username = username_entry.get()
        usernames.append(username)
        count = count + 1
        print(username)
        print(usernames)
        write_csv()
                    
    def instructions_display():
        instructions_text = ct.CTkTextbox(instructions_frame, width=400, height=500, font=("", 10), )
        instructions_text.place(x=50, y=400)
        instructions_text2 = ct.CTkLabel(instructions_text,  text="hello" )
        instructions_text2.pack()
        
        
        
    username_entry = ct.CTkEntry(instructions_frame, placeholder_text="Username")
    username_entry.place(x=50, y=100)

    enter_button = ct.CTkButton(instructions_frame, text="Enter", font=('', 14), fg_color=('#ff4400'), command=enter)
    enter_button.place(x=250, y=100)
    
        
    leaderboard_prompt = ct.CTkLabel(instructions_frame, text="Do you want to read the instructions?", font=("", 20),)
    leaderboard_prompt.place(x=50, y=200)  
    
    leaderboard_yes = ct.CTkButton(instructions_frame, text="Yes", font=('', 14), fg_color=('#ff4400'), command=instructions_display)
    leaderboard_yes.place(x=50, y=250)
    leaderboard_no = ct.CTkButton(instructions_frame, text="No", font=('', 14), fg_color=('#ff4400'), )
    leaderboard_no.place(x=250, y=250)
    

    ct.CTkLabel(instructions_frame, text="Name", font=("", 14)).grid_propagate(False,row=0, column=0, padx=10, pady=5)
    ct.CTkLabel(instructions_frame, text="Score", font=("", 14)).grid_propagate(False,row=0, column=1, padx=10, pady=5)
    ct.CTkLabel(instructions_frame, text="Time", font=("", 14)).grid_propagate(False,row=0, column=2, padx=10, pady=5)

   
    for i, row in df.iterrows():
        ct.CTkLabel(instructions_frame, text=row["Name"]).grid_propagate(False, row=i+1, column=0, padx=10, pady=5)
        ct.CTkLabel(instructions_frame, text=row["Score"]).grid_propagate(False,row=i+1, column=1, padx=10, pady=5)
        ct.CTkLabel(instructions_frame, text=row["Time"]).grid_propagate(False,row=i+1, column=2, padx=10, pady=5)
    
    
    
    
app_frame = ct.CTkFrame(app, width=960, height=640)
app_frame.place(relx=0.1, rely=0.1)
app_frame.pack_propagate(False)

textbox = ct.CTkLabel(app_frame, text="Welcome to Hunt the Wumpus", font=("", 30))
textbox.pack(padx=10, pady=20)  

textbox2 = ct.CTkLabel(app_frame, text="Would you like to play?", font=("", 20))
textbox2.pack(padx=10, pady=0)  

wumpus = ct.CTkImage(light_image=Image.open("wumpus.png"), size=(245, 215))

image_label = ct.CTkLabel(app_frame, image=wumpus, text=("")) 
image_label.place(relx=0.38, rely=0.2,)

yes_button = ct.CTkButton(app_frame, text="Play", font=('Arial', 18), fg_color=('#ff4400'), command=instructions_button)
yes_button.place(x=300, y=500)

no_button = ct.CTkButton(app_frame, text="Exit", font=('Arial', 18), fg_color=('#ff4400'), command=exit)
no_button.place(x=540, y=500)

 
 
                
app.mainloop()
