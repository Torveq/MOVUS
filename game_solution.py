from tkinter import *
from PIL import Image, ImageTk
import os
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets\Icon.ico")

        # Preloads all frames of animation
        self.run_right = self.load_frames("Assets\PlayerRunRight")
        self.run_left = self.load_frames("Assets\PlayerRunLeft")

        self.start_menu()

    def load_frames(self, folder):
        # Loads all frames for any one sprite animation
        self.frame_index = 0
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                image = Image.open(os.path.join(folder, filename)).resize((80,80))
                frames.append(ImageTk.PhotoImage(image))
        return frames  #could use .self instead but to be more modular ig

    def start_menu(self):
        # Reset screen
        #self.clear_frame()
        # Create a frame for the start menu with dimesniosn equal to that of the image
        self.start_img = Image.open("Assets/MainMenue.png")
        self.W, self.H = self.start_img.size
        self.start_frame = Frame(self.root, width=self.W, height=self.H)
        self.start_frame.pack(fill="both", expand=True)

        # Load and display the start image
        self.start_img = ImageTk.PhotoImage(self.start_img)
        label = Label(self.start_frame, image=self.start_img)
        label.pack()

        # Button to start the game
        self.button_img = ImageTk.PhotoImage(Image.open("Assets\PlayButton.png"))
        self.play_button = Button(self.start_frame, image=self.button_img, command=self.game, bd=0, highlightthickness=0, padx=0, pady=0)
        #self.play_button.bind("<Key>", self.game) press any key to play
        self.play_button.place(relx=0.5,rely=0.715, anchor = CENTER)

    def game(self):
        # Reset Screen
        self.clear_frame()
        self.state = "game"

        # Create game frame
        self.gamebg_1 = Image.open("Assets\Gamebg_1.png")
        self.W, self.H = self.gamebg_1.size
        self.game_frame = Frame(self.root, width=self.W, height=self.H)
        self.game_frame.pack(fill="both", expand=True)

        # Load and initialise first game scene
        self.gamebg_1 = ImageTk.PhotoImage(self.gamebg_1)
        self.bg1_canvas = Canvas(self.game_frame, width=self.W, height=self.H)
        self.bg1_canvas.pack()
        self.bg1_canvas.create_image(0,0,image=self.gamebg_1, anchor = NW)

        # Load and initialize player sprite and set default jumping image orientation
        self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
        self.Player_Sprite = self.bg1_canvas.create_image(self.W // 2, int(self.H * 0.82), image = self.PlayerImg, anchor = CENTER)
        self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))

        # Detect keys pressed and released for appropriate action
        self.Running = False
        self.Jumping = False
        self.bg1_canvas.focus_set()
        self.bg1_canvas.bind("<KeyPress>", self.action)
        [key for key in ["d", "a"] if self.bg1_canvas.bind(f"<KeyRelease-{key}>", self.deaction)]

        # Adding a Pause button
        self.PauseImg = ImageTk.PhotoImage(Image.open("Assets\Pause_Button.png").convert("RGBA").resize((25,25)))
        self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0, padx=0, pady=0)
        self.bg1_canvas.create_window(20,20, window = self.Pause_button)

    def action(self, event):
        # Detect what key is pressed and do relevant action
        if self.state!="game":
            return
        self.x, self.y = self.bg1_canvas.coords(self.Player_Sprite)
        if event.char == "d" and self.x < self.W - 20:
            self.running_frames = self.run_right
            self.dx = 10
            self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
            self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))
            if not self.Running:
                self.Running = True
                self.animate()
        elif event.char == "a" and self.x > 20:
            self.running_frames = self.run_left
            self.dx = -10
            self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleL.png"))
            self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpLeft.png").resize((80,80)))
            if not self.Running:
                self.Running = True
                self.animate()
        elif (event.keysym == "space" and not self.Jumping) and (self.x <= (self.W - 10) and self.x >= 20): #right boundary shorter than left due to extra leading transparent pixels when sprite facing east
            self.Jumping = True
            y_speed = -3
            grav = 0.1
            self.bg1_canvas.itemconfig(self.Player_Sprite, image = self.JumpImg) 
            while y_speed < 0 or self.bg1_canvas.coords(self.Player_Sprite)[1] < self.H * 0.82:
                self.bg1_canvas.move(self.Player_Sprite, 0, y_speed)
                self.bg1_canvas.update()
                y_speed += grav
                time.sleep(0.01)
                # Breaks loop if game is paused
                if self.state == "paused":
                    return
            self.Jumping = False
            self.reset_sprite()


    def deaction(self, event):
        # Detects when a key is released and resets to original states
        self.Running = False
        self.reset_sprite()
        pass
    
    def animate(self):
        # Animate the player sprite during action
        if self.Running == False or self.state != "game":
            return
        self.bounds()
        self.bg1_canvas.move(self.Player_Sprite, self.dx, 0)
        if self.Jumping:
            self.bg1_canvas.itemconfig(self.Player_Sprite, image = self.JumpImg)
        else:
            self.framespeed = 100
            self.frame_index = (self.frame_index +1) % len(self.running_frames)
            self.bg1_canvas.itemconfig(self.Player_Sprite, image = self.running_frames[self.frame_index])
        self.root.after(self.framespeed, self.animate)

    def bounds(self):
        # Checks if Player Sprite is within the border of the screen/the boundary and doesn't allow further movement
        x = self.bg1_canvas.coords(self.Player_Sprite)[0]
        if x <= 20 and self.dx < 0:
            self.dx = 0
        elif x >= self.W - 20 and self.dx > 0:
            self.dx = 0

    def reset_sprite(self):
        # Resets the player sprite to the idle position
        self.bg1_canvas.itemconfig(self.Player_Sprite, image=self.PlayerImg)

    def pause(self):
        # Pauses the game and displays an option menu
        if self.state == "game":
            self.state = "paused"
            self.bg1_canvas.unbind("<KeyPress>")
            self.bg1_canvas.unbind("<KeyRelease>") #need to fix this as still detected when paused
            #[key for key in ["d", "a"] if self.bg1_canvas.unbind(f"<KeyRelease-{key}>", self.deaction)]

        pass

    def clear_frame(self):
        # Reset and remove all frames and widgets
        for widget in self.root.winfo_children():
            widget.destroy() 
        #self.start_frame.pack_forget() might want to add this back when project gets too big 

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
