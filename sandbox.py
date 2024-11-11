from tkinter import *
from PIL import Image, ImageTk
import os
import time
import random
import math
import json

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets/Icon.ico")
        self.root.bind("<Button-1>", self.debugging)  # for debugging purposes
        self.root.wm_attributes('-transparentcolor', '#ab23ff')
        self.state_file = "game_state.json"
        
        # Preloads all frames of animation
        self.run_right = self.load_frames("Assets/PlayerRunRight")
        self.run_left = self.load_frames("Assets/PlayerRunLeft")
        # Add other frames for animations similarly

        # Start game setup
        self.start_menu()

    def debugging(self, event):
        print(f"Clicked at ({event.x}, {event.y})")

    def load_frames(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                image = Image.open(os.path.join(folder, filename)).resize((80,80))
                frames.append(ImageTk.PhotoImage(image))
        return frames

    def start_menu(self):
        self.clear_frame()
        self.start_img = Image.open("Assets/MainMenue.png")
        self.W, self.H = self.start_img.size
        self.start_frame = Frame(self.root, width=self.W, height=self.H)
        self.start_frame.pack(fill="both", expand=True)
        self.start_img = ImageTk.PhotoImage(self.start_img)
        label = Label(self.start_frame, image=self.start_img)
        label.pack()

        self.button_img = ImageTk.PhotoImage(Image.open("Assets/PlayButton.png"))
        self.play_button = Button(self.start_frame, image=self.button_img, command=self.game, bd=0, highlightthickness=0)
        self.play_button.place(relx=0.5, rely=0.715, anchor=CENTER)

    def game(self):
        self.clear_frame()
        self.state = "game"

        # Create game frame
        self.gamebg_1 = Image.open("Assets/Gamebg_1.png")
        self.W, self.H = self.gamebg_1.size
        self.game_frame = Frame(self.root, width=self.W, height=self.H)
        self.game_frame.pack(fill="both", expand=True)

        self.gamebg_1 = ImageTk.PhotoImage(self.gamebg_1)
        self.cn = Canvas(self.game_frame, width=self.W, height=self.H)
        self.cn.pack()
        self.cn.create_image(0, 0, image=self.gamebg_1, anchor=NW)

        # Load pause option menu and pause button
        self.OptionsImg = ImageTk.PhotoImage(Image.open("Assets/optionsmenu.png"))
        self.PauseImg = ImageTk.PhotoImage(Image.open("Assets/Pause_Button.png").resize((25,25)))
        self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
        self.cn.create_window(20, 20, window=self.Pause_button)

        # Initialize game state variables
        self.Action = False
        self.Running = False
        self.paused = False

        # Detect keys pressed and released
        self.cn.focus_set()
        self.cn.bind("<KeyPress>", self.action)
        self.cn.bind("<KeyRelease>", self.deaction)

    def pause(self):
        if self.state == "game":
            self.paused = True
            self.state = "paused"
            self.cn.unbind("<KeyPress>")
            self.cn.unbind("<KeyRelease>")
            self.Pause_button.destroy()

            # Show pause menu
            self.OptionsButton = Button(
                image=self.OptionsImg, borderwidth=0, highlightthickness=0, background="#ab23ff")
            self.OptionsButton.bind("<Button-1>", self.option_clicked)
            self.OptionsMenu = self.cn.create_window(self.W // 2, int(self.H * 0.5), window=self.OptionsButton, anchor=CENTER)

    def resume(self):
        if self.state == "paused":
            self.paused = False
            self.state = "game"
            self.cn.delete(self.OptionsMenu)
            self.cn.focus_set()
            self.cn.bind("<KeyPress>", self.action)
            self.cn.bind("<KeyRelease>", self.deaction)

            # Recreate the pause button
            self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
            self.cn.create_window(20, 20, window=self.Pause_button)

    def option_clicked(self, event):
        # Check if resume button is clicked
        x, y = event.x, event.y
        # Assuming you have coordinates for buttons in options menu
        if x > 174 and x < 192 and y > 3 and y < 22:  # Resume button coordinates
            self.resume()
        # Add checks for other buttons

    def action(self, event):
        if self.state != "game":
            return
        # Implement movement or actions here

    def deaction(self, event):
        if self.state != "game":
            return
        # Reset movement

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Set up the Tkinter window
root = Tk()
app = App(root)
root.mainloop()
