import customtkinter as ct
import tkinter as tk
from PIL import Image
import pandas as pd
import random


app = ct.CTk()
app.resizable(False, False)
app.geometry("1200x800+420+120")
app.title("Hunt The Wumpus")
df = pd.read_csv("Users.csv")

cave_system = [
    (1,5,98,98),  # Cave 0
    (2,5,99,0),     # Cave 1
    (1,3,4,5),       # Cave 2
    (2,98,98,4),   # Cave 3
    (3,9,8,2),   # Cave 4
    (1,2,6,0),  # Cave 5
    (5,8,99,7),
    (6,8,10,99),
    (4,9,7,6),
    (4,10,99,8),
    (7,9,98,98)
]
current_cave = random.randint(0,10)
count = 4
arrows = 0
moves = 0
time = 0
ct.set_appearance_mode("Dark")  
ct.set_default_color_theme("blue")   


def write_csv():
    df.loc[len(df)] = [username, 0, 0]
    #SCORE
    #TIME
    df.to_csv('Users.csv', index=False)

def play_screen():
    cave_connections = cave_system[current_cave]
    
    def north_selection():
        global current_cave
        current_cave = cave_connections[0]
        if current_cave == 99:
            current_cave == 91  
        elif current_cave == 98:
            
        else:

        play_window.withdraw()
        play_screen()
        
    def east_selection():
        global current_cave
        current_cave = cave_connections[1]
        play_window.withdraw()
        play_screen()
        
    def south_selection():
        global current_cave
        current_cave = cave_connections[2]
        play_window.withdraw()
        play_screen()
        
    def west_selection():
        global current_cave
        current_cave = cave_connections[3]
        play_window.withdraw()
        play_screen()
    
    instructions_window.withdraw()
    play_window = ct.CTkToplevel(app)
    play_window.title("Instructions")
    play_window.geometry("1200x800+420+120")
    play_window.resizable(False, False)
    
    play_frame = ct.CTkFrame(play_window, width=960, height=640)
    play_frame.place(relx=0.1, rely=0.1)
    play_frame.pack_propagate(False)
    
    current_cave_display = ct.CTkLabel(play_frame, text=f"Cave: {current_cave} ", font=("", 20))
    current_cave_display.place(x=50, y=20) 
    arrow_num = ct.CTkLabel(play_frame, text=f"Arrows left: {arrows}", font=("", 20))
    arrow_num.place(x=200, y=20) 
    move_num = ct.CTkLabel(play_frame, text=f"Moves made: {moves} " , font=("", 20))
    move_num.place(x=400, y=20) 
    
    cave_image = ct.CTkImage(light_image=Image.open("cave.png"), size=(200, 200))
    cave_image2 = ct.CTkImage(light_image=Image.open("cave.png"), size=(200, 200))
    cave_image3 = ct.CTkImage(light_image=Image.open("cave.png"), size=(200, 200))
    cave_image4 = ct.CTkImage(light_image=Image.open("cave.png"), size=(200, 200))
    
    cave_image_label = ct.CTkLabel(play_frame, image=cave_image, text=("")) 
    cave_image_label2 = ct.CTkLabel(play_frame, image=cave_image2, text=("")) 
    cave_image_label3 = ct.CTkLabel(play_frame, image=cave_image3, text=("")) 
    cave_image_label4 = ct.CTkLabel(play_frame, image=cave_image4, text=("")) 
    
    cave_image_label.place(x=380, y=130,)
    cave_image_label2.place(x=170, y=280,)
    cave_image_label3.place(x=580, y=280,)
    cave_image_label4.place(x=380, y=430,)
    
    
    north_button = ct.CTkButton(play_frame, text="N", font=('', 16), fg_color=('#ff4400'), command=north_selection, width=40, height=40   )
    north_button.place(x=460, y=325)
    east_button = ct.CTkButton(play_frame, text="E", font=('', 16), fg_color=('#ff4400'), command=east_selection, width=40, height=40 )
    east_button.place(x=530, y=355)
    south_button = ct.CTkButton(play_frame, text="S", font=('', 16), fg_color=('#ff4400'), command=south_selection, width=40, height=40   )
    south_button.place(x=460, y=385)
    west_button = ct.CTkButton(play_frame, text="W", font=('', 16), fg_color=('#ff4400'), command=west_selection, width=40, height=40  )
    west_button.place(x=390, y=355)
    
       

def middle_screen():
    app.withdraw()
    global instructions_window
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
        if username.strip():  # Check if username is not blank or only whitespace
            usernames.append(username)
            count += 1
            write_csv()
        else:
            pass  
                    
    def instructions_display():
        instructions_text = ct.CTkLabel(instructions_frame,  text="""You are a hunter lost in a complex cave system. 
There is a Wumpus lurking somewhere in the caves, 
waiting for you to walk into his arms. 
Apart from the Wumpus there are also bats that live in the caves,
teleporting you to a random cave if you happen to run into them. 
You only have 5 arrows.
Your objective is to locate and shoot the Wumpus with one of your arrows. 
But beware, if you run out of arrows; 
YOU LOSE! 
You can travel through the caves in four cardinal directions (N,E,S,W). 
Some caves are tricky, looping back to itself, or even lead to dead ends. 
Shooting an arrow into any of these may result in killing yourself. 
BE CAUTIOUS, AND GOOD LUCK!""", anchor='w', justify='left', font=("", 14))
        instructions_text.place(x=50, y=350)
        
        
    def leaderboard_display():
        df_score_sorted = df.sort_values(by='Score', ascending=False).head(10)
        leaderboard_text = "Score Leaderboard:\nName\t\tScore\t\tTime\n"
        for i, row in df_score_sorted.iterrows():
            leaderboard_text += f"{row['Name']}\t\t{row['Score']}\t\t{row['Time']}\n"
            leaderboard_label = ct.CTkLabel(instructions_frame, text=leaderboard_text, font=("", 15))
            leaderboard_label.place(x=540, y=150)    
        df_time_sorted = df.sort_values(by='Time', ascending=True).head(10)
        leaderboard_text2 = "Time Leaderboard:\nName\t\tScore\t\tTime\n"
        for i, row in df_time_sorted.iterrows():
            leaderboard_text2 += f"{row['Name']}\t\t{row['Score']}\t\t{row['Time']}\n"
            leaderboard_label2 = ct.CTkLabel(instructions_frame, text=leaderboard_text2, font=("", 15))
            leaderboard_label2.place(x=540, y=380)
    
    
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
    
    play_button = ct.CTkButton(instructions_frame, text="Play", font=('', 14), fg_color=('#ff4400'), command=play_screen )
    play_button.place(x=400, y=600)
    
      
    
   
    
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

yes_button = ct.CTkButton(app_frame, text="Play", font=('Arial', 18), fg_color=('#ff4400'), command=middle_screen)
yes_button.place(x=300, y=500)

no_button = ct.CTkButton(app_frame, text="Exit", font=('Arial', 18), fg_color=('#ff4400'), command=exit)
no_button.place(x=540, y=500)

 
 
                
app.mainloop()
