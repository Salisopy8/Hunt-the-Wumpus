import customtkinter as ct
import tkinter as tk
from PIL import Image
import pandas as pd
import random
import time
#All imported modules

# Reads user data from the User CSV file
df = pd.read_csv("Users.csv")

# Cave system structure
cave_system = [
    (1, 5, 98, 98),  # Cave 0
    (2, 5, 99, 0),   # Cave 1
    (1, 3, 4, 5),    # Cave 2
    (2, 98, 98, 4),  # Cave 3
    (3, 9, 8, 2),    # Cave 4
    (1, 2, 6, 0),    # Cave 5
    (5, 8, 99, 7),   # Cave 6
    (6, 8, 10, 99),  # Cave 7
    (4, 9, 7, 6),    # Cave 8
    (4, 10, 99, 8),  # Cave 9
    (7, 9, 98, 98)   # Cave 10
]

# Initialized game variables
arrows = 5
moves = 0
wumpus_location = 9
current_cave = random.randint(0, 10)
start_time = 0
win = 0

# Custom Tkinter GUI colour theme
ct.set_appearance_mode("Dark") 


# Creates main tltle game window
app = ct.CTk()
app.resizable(False, False)
app.geometry("1200x800+420+120")
app.title("Hunt The Wumpus")

#Function for adding a users name, score, and time of completion to the leaderboard
def write_csv():
    global username
    score = moves + (5 - arrows) #Calculates the users score which is equal to num of moves + arrows used
    df.loc[len(df)] = [username, score, elapsed_time]
    df.to_csv('Users.csv', index=False) #writes to 'users.csv' file

#Function for the ending screen window, once the user has either won or lost
def end_screen():
    global win, end_window
    play_window.withdraw()  #closes previous window
    
    if win == 5: #only adds users details to the leadearboards if they won
        write_csv()
        
    #creates the ending screen window
    end_window = ct.CTkToplevel(app)
    end_window.title("End Screen")
    end_window.geometry("1200x800+420+120")
    end_window.resizable(False, False)
    
    end_frame = ct.CTkFrame(end_window, width=960, height=640)
    end_frame.place(relx=0.1, rely=0.1)
    end_frame.pack_propagate(False)
    
    #displays wumpus image
    wumpus = ct.CTkImage(light_image=Image.open("wumpus.png"), size=(245, 215))
    image_label = ct.CTkLabel(end_frame, image=wumpus, text="")
    image_label.place(relx=0.38, rely=0.2)
    
    #Function for if user selects the play again button
    def play_again():
        end_window.destroy()
        middle_screen()
    
    #user gets the offer to play again or to exit
    play_again_button = ct.CTkButton(end_frame, text="Play",  fg_color=('#ff4400'), font=('', 18),command=play_again)
    play_again_button.place(x=300, y=500)
    exit_button = ct.CTkButton(end_frame, text="Exit", font=('', 18), fg_color=('#ff4400'), command=app.quit)
    exit_button.place(x=540, y=500)
    
    #end screen message, depending on how the user either won or lost
    message_text = ""
    if win == 1:        
        message_text = "Unlucky! You got killed by the Wumpus!"
    elif win == 2:
        message_text = "Oh no! You ran out of arrows, YOU LOSE!"
    elif win == 3:
        message_text = "Unlucky! Your arrow rebounded killing you!"
    elif win == 4:
        message_text = "Oh no! You shot yourself through a loop!"
    elif win == 5:
        message_text = f"Congratulations! You shot the Wumpus in {elapsed_time} seconds" #if the user won, their time of completion is displayed to them
        
    #end message is displayed on the gui
    end_message = ct.CTkLabel(end_frame, text=message_text, font=('', 22))
    end_message.place(relx=0.5, rely=0.1, anchor="center")

#Main playing function/subroutine
def play_screen():
    instructions_window.withdraw() #closes previous instruction window
    global current_cave, arrows, moves, start_time, play_window, win, situational_message, enemy_message
    start_time = time.time() #time starts once user enters the play window

    # Creates play window
    play_window = ct.CTkToplevel(app)
    play_window.title("Play Screen")
    play_window.geometry("1200x800+420+120")
    play_window.resizable(False, False)
    
    play_frame = ct.CTkFrame(play_window, width=960, height=640)
    play_frame.place(relx=0.1, rely=0.1)
    play_frame.pack_propagate(False)
    
    # Display current status of the users current cave, number of arrows, and amount of moves made
    current_cave_display = ct.CTkLabel(play_frame, text=f"Cave: {current_cave}", font=("", 20))
    current_cave_display.place(x=50, y=20)
    arrow_num = ct.CTkLabel(play_frame, text=f"Arrows left: {arrows}", font=("", 20))
    arrow_num.place(x=200, y=20)
    move_num = ct.CTkLabel(play_frame, text=f"Moves made: {moves}", font=("", 20))
    move_num.place(x=400, y=20)
    
    #Any situational cave messages are displayed to the user 
    situational_message = ct.CTkLabel(play_frame, text="", font=('', 18))
    situational_message.place(x=50, y=60)
    enemy_message = ct.CTkLabel(play_frame, text="", font=('', 18))
    enemy_message.place(x=50, y=100)
    
    #Checks if the user is next to the wumpus or bats, if they are the sitautional message is updated to reflect it
    if wumpus_location in cave_system[current_cave]: #checks to see if the wumpus is in an adjacent cave
        enemy_message.configure(text="A Wumpus is nearby!")
    if bats_location in cave_system[current_cave]: #checks to see if bats are in an adjacent cave
        situational_message.configure(text="Watch out! There are bats nearby!")
    
    # Movement function
    def move_player(next_cave):
        global current_cave, moves, wumpus_location, arrows, win

        situational_message.configure(text="")
        enemy_message.configure(text="")

        
        if next_cave == 99:     #99 is the code number for a dead end in the array
            situational_message.configure(text="Whoops, You ran into a dead end!")
        elif next_cave == 98:   #98 is the code number for a dead end in the array
            situational_message.configure(text="Oh no, You walked in a loop!")
        elif next_cave == wumpus_location: #player walks into the wumpus cave
            win = 1
            end_screen() #player loses and is sent to the end screen
        elif next_cave == bats_location: #player moves to the bats cave
            situational_message.configure(text="BATS! You have been teleported to a new cave!")
            current_cave = random.randint(0, 10) #their location is updated to a random cave
            while current_cave == wumpus_location or current_cave == bats_location: #makes sure the user cant be teleported to the wumpus's cave or the bats cave again
                current_cave = random.randint(0, 10)
            current_cave_display.configure(text=f"Cave: {current_cave}") #new cave is displayed
        else:
            if wumpus_location in cave_system[next_cave]:      #checks to see if the wumpus is next to the users new cave
                enemy_message.configure(text="A Wumpus is nearby!")
            current_cave = next_cave #sets the cave they just moved into, as their current cave
            current_cave_display.configure(text=f"Cave: {current_cave}") #updates the current cave display
            
            #if users new cave is next to the bats cave it is displayed to them
            if bats_location in cave_system[next_cave]: 
                situational_message.configure(text="Watch out! There are bats nearby!")
                current_cave = next_cave
                current_cave_display.configure(text=f"Cave: {current_cave}")
                
            
        #move count is updated
        moves += 1
        move_num.configure(text=f"Moves made: {moves}")
    
    # Movement functions which are connected to the buttons
    def north_selection():
        move_player(cave_system[current_cave][0]) #north is the first element in the array

    def east_selection():
        move_player(cave_system[current_cave][1]) #east is the second element in the array

    def south_selection():
        move_player(cave_system[current_cave][2]) #south is the third element in the array

    def west_selection():
        move_player(cave_system[current_cave][3]) #west is the fourth element in the array
    
    
    def shoot_action(shoot_cave):
        global current_cave, moves, wumpus_location, arrows, elapsed_time, win

        situational_message.configure(text="")
        enemy_message.configure(text="")

        if shoot_cave == 99:
            win = 3
            end_screen()
        elif shoot_cave == 98:
            win = 4
            end_screen()
        elif shoot_cave == wumpus_location:
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2) #Calculates the elapsed time, and rounds it to two decimal places
            win = 5
            end_screen()
        else:
            situational_message.configure(text="Whoops, your shot missed!")
            arrows = arrows - 1
            if arrows < 1:
                win = 2
                end_screen()
            else:
                pass

        moves = moves + 1
        arrow_num.configure(text=f"Arrows left: {arrows}")
        
    
    # Movement buttons
    def north_shot():
        shoot_action(cave_system[current_cave][0])

    def east_shot():
        shoot_action(cave_system[current_cave][1])

    def south_shot():
        shoot_action(cave_system[current_cave][2])

    def west_shot():
        shoot_action(cave_system[current_cave][3])

    # Cave images
    cave_image = ct.CTkImage(light_image=Image.open("cave.png"), size=(200, 200)) 
    cave_image_label = ct.CTkLabel(play_frame, image=cave_image, text="")
    cave_image_label.place(x=380, y=130)

    cave_image_label2 = ct.CTkLabel(play_frame, image=cave_image, text="")
    cave_image_label2.place(x=170, y=280)

    cave_image_label3 = ct.CTkLabel(play_frame, image=cave_image, text="")
    cave_image_label3.place(x=580, y=280)

    cave_image_label4 = ct.CTkLabel(play_frame, image=cave_image, text="")
    cave_image_label4.place(x=380, y=430)
    
    move_label = ct.CTkLabel(play_frame, text="Move", font=('', 18))
    move_label.place(x=98, y=480)
    
    shoot_label = ct.CTkLabel(play_frame, text="Shoot", font=('', 18))
    shoot_label.place(x=805, y=480)
      
    
    north_button = ct.CTkButton(play_frame, text="N", font=('', 16), fg_color=('#ff4400'), command=north_selection, width=40, height=40)
    north_button.place(x=100, y=525)

    east_button = ct.CTkButton(play_frame, text="E", font=('', 16), fg_color=('#ff4400'), command=east_selection, width=40, height=40)
    east_button.place(x=170, y=555)

    south_button = ct.CTkButton(play_frame, text="S", font=('', 16), fg_color=('#ff4400'), command=south_selection, width=40, height=40)
    south_button.place(x=100, y=585)

    west_button = ct.CTkButton(play_frame, text="W", font=('', 16), fg_color=('#ff4400'), command=west_selection, width=40, height=40)
    west_button.place(x=30, y=555)
    
    north_shoot_button = ct.CTkButton(play_frame, text="N", font=('', 16), fg_color=('#ff4400'), command=north_shot, width=40, height=40)
    north_shoot_button.place(x=810, y=525)

    east_shoot_button = ct.CTkButton(play_frame, text="E", font=('', 16), fg_color=('#ff4400'), command=east_shot, width=40, height=40)
    east_shoot_button.place(x=880, y=555)

    south_shoot_button = ct.CTkButton(play_frame, text="S", font=('', 16), fg_color=('#ff4400'), command=south_shot, width=40, height=40)
    south_shoot_button.place(x=810, y=585)

    west_shoot_button = ct.CTkButton(play_frame, text="W", font=('', 16), fg_color=('#ff4400'), command=west_shot, width=40, height=40)
    west_shoot_button.place(x=740, y=555)

def middle_screen():
    app.withdraw()
    global instructions_window, current_cave, wumpus_location, bats_location, arrows, moves
    moves = 0
    arrows = 5
    wumpus_location = random.randint(0,10)
    current_cave = random.randint(0,10)
    bats_location = random.randint(0,10)
    while bats_location == wumpus_location:
        bats_location = random.randint(0,10)
    
    while current_cave == wumpus_location or current_cave == bats_location:
        current_cave = random.randint(0, 10)
        

    instructions_window = ct.CTkToplevel(app)
    instructions_window.title("Instructions")
    instructions_window.geometry("1200x800+420+120")
    instructions_window.resizable(False, False)
    
    instructions_frame = ct.CTkFrame(instructions_window, width=960, height=640)
    instructions_frame.place(relx=0.1, rely=0.1)
    instructions_frame.pack_propagate(False)
   
    username_prompt = ct.CTkLabel(instructions_frame, text="Please enter your username (Max 7 Char) and press enter:", font=("", 16))
    username_prompt.place(x=50, y=50)  
    
    error_label = ct.CTkLabel(instructions_frame, text="", font=("", 16))
    error_label.place(x=50, y=150)
    
    usernames = df['Name'].to_list()
    
    def enter():
        global username
        username = username_entry.get()
        if username.strip():  # Check if username is not blank or only whitespace
            if len(username) <= 7:  # Check if the username is 7 characters or less
                usernames.append(username)
                error_label.configure(text="")  # Clear any previous error message
                play_button.place(x=400, y=600)
            else:
                error_label.configure(text="Username must be 7 characters or less.")
        else:
            error_label.configure(text="Username cannot be blank.")
                    
    def instructions_display():
        global instructions_text
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
        global leaderboard_label, leaderboard_label2
        df_score_sorted = df.sort_values(by='Score', ascending=True).head(10)
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
        
        
    def leaderboard_close():
        leaderboard_label.destroy()
        leaderboard_label2.destroy()
        
    def instructions_close():
        instructions_text.destroy()
        
    
    
    
    username_entry = ct.CTkEntry(instructions_frame, placeholder_text="Username")
    username_entry.place(x=50, y=100)

    enter_button = ct.CTkButton(instructions_frame, text="Enter", font=('', 14), fg_color=('#ff4400'), command=enter)
    enter_button.place(x=250, y=100)
    
        
    instructions_prompt = ct.CTkLabel(instructions_frame, text="Do you want to read the instructions?", font=("", 16))
    instructions_prompt.place(x=50, y=200)  
    
    instructions_yes = ct.CTkButton(instructions_frame, text="Open", font=('', 14), fg_color=('#ff4400'), command=instructions_display)
    instructions_yes.place(x=50, y=250)

    instructions_no = ct.CTkButton(instructions_frame, text="Close", font=('', 14), fg_color=('#ff4400'), command = instructions_close)
    instructions_no.place(x=250, y=250)
    
    leaderboard_prompt = ct.CTkLabel(instructions_frame, text="Do you want to view the leaderboards?", font=("", 16))
    leaderboard_prompt.place(x=520, y=50)

    leaderboard_yes = ct.CTkButton(instructions_frame, text="Open", font=('', 14), fg_color=('#ff4400'), command=leaderboard_display)
    leaderboard_yes.place(x=520, y=100)

    leaderboard_no = ct.CTkButton(instructions_frame, text="Close", font=('', 14), fg_color=('#ff4400'), command = leaderboard_close)
    leaderboard_no.place(x=720, y=100)
    
    play_button = ct.CTkButton(instructions_frame, text="Play", font=('', 14), fg_color=('#ff4400'), command=play_screen)
    

# Main app frame
app_frame = ct.CTkFrame(app, width=960, height=640)
app_frame.place(relx=0.1, rely=0.1)
app_frame.pack_propagate(False)

cavebackground = ct.CTkImage(dark_image=Image.open("background.png"), size=(960, 640))
backgroundimage_label = ct.CTkLabel(app_frame, image=cavebackground, text="")
backgroundimage_label.place(relx=0, rely=0, relwidth=1, relheight=1)


welcome_message = ct.CTkLabel(app_frame, text="Welcome to Hunt the Wumpus", font=("", 30),bg_color="transparent")

welcome_message.pack(padx=10, pady=20)  

play_message = ct.CTkLabel(app_frame, text="Would you like to play?", font=("", 20),)
play_message.pack(padx=10, pady=0)  

wumpus = Image.open("wumpus.png").convert("RGBA")
wumpus = ct.CTkImage(light_image=Image.open("wumpus.png"), size=(245, 215),)
image_label = ct.CTkLabel(app_frame, image=wumpus, text="", bg_color="transparent")
image_label.place(relx=0.38, rely=0.2)



play_button = ct.CTkButton(app_frame, text="Play", font=('', 18), fg_color=('#ff4400'), command=middle_screen,)
play_button.place(x=300, y=500)

exit_button = ct.CTkButton(app_frame, text="Exit", font=('', 18), fg_color=('#ff4400'), command=app.quit,)
exit_button.place(x=540, y=500)

app.mainloop()
