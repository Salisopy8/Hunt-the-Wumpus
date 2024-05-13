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


def instructions_button():
    app.withdraw()
    instructions_window = ct.CTkToplevel(app)
    instructions_window.title("Instructions")
    instructions_window.geometry("1200x800+420+120")
    instructions_window.resizable(False, False)
    
    instructions_frame = ct.CTkFrame(instructions_window, width=960, height=640)
    instructions_frame.place(relx=0.1, rely=0.1)
    instructions_frame.pack_propagate(False)


    instructions_text = ct.CTkLabel(instructions_frame, width=30, height=69, text="""You are a hunter lost in a complex cave system. There is a Wumpus lurking within the same cave system, waiting for you to walk into his arms. Apart from the Wumpus there are also bats that live in a cave, teleporting you to a random cave if you happen to run into them. 
                                                                    You only have 5 arrows left, and your objective is to locate and shoot the Wumpus with one of your arrows. But beware, if you run out of arrows, YOU LOSE! 
                                                                    You can travel through the caves in the four cardinal directions (N, E, S, W). However, some caves can be tricky, and may loop back to itself, or even lead to dead ends. Shooting an arrow into any of these may result in killing yourself. 
                                                                    BE CAUTIOUS, AND GOOD LUCK!""", font=("", 10))
    instructions_text.place(x=400, y=600)
    
    
    
    """You are a hunter lost in a complex cave system. There is a Wumpus lurking within the same cave system, waiting for you to walk into his arms. 
                                                                                    Apart from the Wumpus there are also bats that live in a cave, teleporting you to a random cave if you happen to run into them. 
                                                                                    You only have 5 arrows left, and your objective is to locate and shoot the Wumpus with one of your arrows. 
                                                                                    But beware, if you run out of arrows, YOU LOSE! 
                                                                                    You can travel through the caves in the four cardinal directions (N, E, S, W). 
                                                                                    However, some caves can be tricky, and may loop back to itself, or even lead to dead ends. 
                                                                                    Shooting an arrow into any of these may result in killing yourself. 
                                                                                    BE CAUTIOUS, AND GOOD LUCK!"""