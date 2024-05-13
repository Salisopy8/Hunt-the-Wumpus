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
        instructions_text = ct.CTkLabel(instructions_frame,  text="""You are a hunter lost in a complex cave system. 
There is a Wumpus lurking somewhere in the caves, 
waiting for you to walk into his arms. 
Apart from the Wumpus there are also bats that live in the caves,
teleporting you to a random cave if you happen to run into them. 
You only have 5 arrows.
Your objective is to locate and shoot the Wumpus with one of your arrows. 
But beware, if you run out of arrows, YOU LOSE! 
You can travel through the caves in the four cardinal directions (N,E,S,W). 
Some caves can be tricky, looping back to itself, or even lead to dead ends. 
Shooting an arrow into any of these may result in killing yourself. 
BE CAUTIOUS, AND GOOD LUCK!""", anchor='w', justify='left', font=("", 14))
        instructions_text.place(x=50, y=350)
        
        
    def leaderboard_display():
        leaderboard_text = "Leaderboard:\nName\t\tScore\t\tTime\n"
        for i, row in df.iterrows():
            leaderboard_text += f"{row['Name']}\t\t{row['Score']}\t\t{row['Time']}\n"
            leaderboard_label = ct.CTkLabel(instructions_frame, text=leaderboard_text, font=("", 16))
            leaderboard_label.place(x=540, y=160)
    
    
    username_entry = ct.CTkEntry(instructions_frame, placeholder_text="Username")
    username_entry.place(x=50, y=100)

    enter_button = ct.CTkButton(instructions_frame, text="Enter", font=('', 14), fg_color=('#ff4400'), command=enter)
    enter_button.place(x=250, y=100)
    
        
    instructions_prompt = ct.CTkLabel(instructions_frame, text="Do you want to read the instructions?", font=("", 20),)
    instructions_prompt.place(x=50, y=200)  
    
    instructions_yes = ct.CTkButton(instructions_frame, text="Yes", font=('', 14), fg_color=('#ff4400'), command=instructions_display)
    instructions_yes.place(x=50, y=250)
    instructions_no = ct.CTkButton(instructions_frame, text="No", font=('', 14), fg_color=('#ff4400'), )
    instructions_no.place(x=250, y=250)
    
    leaderboard_prompt = ct.CTkLabel(instructions_frame, text="Do you want to view the leaderboards?", font=("", 20))
    leaderboard_prompt.place(x=520, y=50)

    leaderboard_yes = ct.CTkButton(instructions_frame, text="Yes", font=('', 14), fg_color=('#ff4400'), command=leaderboard_display    )
    leaderboard_yes.place(x=520, y=100)
    leaderboard_no = ct.CTkButton(instructions_frame, text="No", font=('', 14), fg_color=('#ff4400'), )
    leaderboard_no.place(x=720, y=100)
    
   
    
    
    
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
