from tkinter import *
from PIL import Image, ImageTk
import os
import time
import random
#from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets\Icon.ico")
        #self.root.resizable(True,True) doesnt work as intended, trying to upscale the entire thing to provide fullscreen option

        # Preloads all frames of animation (NPCWR is an abbreviation for NPC Walk Right BR is bite right AR is attack right etc..)
        self.run_right = self.load_frames("Assets\PlayerRunRight")
        self.run_left = self.load_frames("Assets\PlayerRunLeft")
        self.attack_right = self.load_frames("Assets\RightAttack")
        self.attack_left = self.load_frames("Assets\LeftAttack")
        self.run_attack_right = self.load_frames("Assets\RightRunAttack")
        self.run_attack_left = self.load_frames("Assets\LeftRunAttack")
        self.npcwr = self.load_frames(r"Assets\NPC\Mob1WalkRight")
        self.npcwl = self.load_frames(r"Assets\NPC\Mob1WalkLeft")
        self.npcrr = self.load_frames(r"Assets\NPC\Mob2RunRight")
        self.npcrl = self.load_frames(r"Assets\NPC\Mob2RunLeft")
        self.npcar = self.load_frames(r"Assets\NPC\Mob1AttackRight")
        self.npcal = self.load_frames(r"Assets\NPC\Mob1AttackLeft")
        self.npcbr = self.load_frames(r"Assets\NPC\Mob2BiteRight")
        self.npcbl = self.load_frames(r"Assets\NPC\Mob2BiteLeft")
        self.npc1deadr = self.load_frames(r"Assets\NPC\Mob1DeadRight")
        self.npc1deadl = self.load_frames(r"Assets\NPC\Mob1DeadLeft")
        self.npc2deadr = self.load_frames(r"Assets\NPC\Mob2DeadRight")
        self.npc2deadl = self.load_frames(r"Assets\NPC\Mob2DeadLeft")

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
        self.cn = Canvas(self.game_frame, width=self.W, height=self.H)
        self.cn.pack()
        self.cn.create_image(0,0,image=self.gamebg_1, anchor = NW)

        # Load and initialize player sprite and set default jumping image orientation
        self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
        self.Player_Sprite = self.cn.create_image(self.W // 2, int(self.H * 0.82), image = self.PlayerImg, anchor = CENTER)
        self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))

        self.Zombies = []

        # Load and initialize player's health bar 
        self.FullHealthBarImg = ImageTk.PhotoImage(Image.open(r"Assets\HealthBar\100.png").resize((250, 14)))
        self.HP = self.cn.create_image(400, self.H*0.03, image = self.FullHealthBarImg, anchor=NW)

        # Detect keys pressed and released for appropriate action
        self.Action = False
        self.Running = False
        self.Jumping = False
        self.Attacking = False
        self.RunAttacking = False
        
        self.cn.focus_set()
        self.cn.bind("<KeyPress>", self.action)
        [key for key in ["d", "a", "w"] if self.cn.bind(f"<KeyRelease-{key}>", self.deaction)]
        #self.cn.bind("<ButtonRelease-1>", self.deaction) later for when i implement attacking via left mouse button 

        # Start spawning mobs and queuing their animations
        self.spawn_mobs()
        self.action_mobs()

        # Adding a Pause button
        self.PauseImg = ImageTk.PhotoImage(Image.open("Assets\Pause_Button.png").convert("RGBA").resize((25,25)))
        self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0, padx=0, pady=0)
        self.cn.create_window(20,20, window = self.Pause_button)

    def action(self, event):
        # Detect what key is pressed and do relevant action
        if self.state!="game":
            return
        self.x, self.y = self.cn.coords(self.Player_Sprite)

        if event.char == "d" and self.x < self.W - 20:
            if not self.mob_collisions(dx=10):
                self.running_frames = self.run_right
                self.dx = 10
                self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
                self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))
                if not self.Running:
                    self.Running = True
                    self.Action = True
                    self.animate()

        elif event.char == "a" and self.x > 20:
            if not self.mob_collisions(dx=-10):
                self.running_frames = self.run_left
                self.dx = -10
                self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleL.png"))
                self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpLeft.png").resize((80,80)))
                if not self.Running:
                    self.Running = True
                    self.Action = True
                    self.animate()

        elif (event.keysym == "space" and not self.Jumping) and (self.x <= (self.W - 10) and self.x >= 20): #right boundary shorter than left due to extra leading transparent pixels when sprite facing east
            self.Jumping = True
            y_speed = -3
            grav = 0.1
            self.cn.itemconfig(self.Player_Sprite, image = self.JumpImg) 
            while y_speed < 0 or self.cn.coords(self.Player_Sprite)[1] < self.H * 0.82:
                self.cn.move(self.Player_Sprite, 0, y_speed)
                self.cn.update()
                y_speed += grav
                time.sleep(0.01)
                # Breaks loop if game is paused
                if self.state == "paused":
                    return
            self.Jumping = False
            self.reset_sprite()
        
        elif event.char == "w":
            if self.Jumping or self.Attacking or self.RunAttacking:
                return  # Prevents attacking if the player is jumping or already attacking
            attack_range = 50
            if self.Running and not self.RunAttacking:
                self.RunAttacking = True
                self.Action = True
                self.running_frames = self.run_attack_right if self.dx>0 else self.run_attack_left
            elif not self.Attacking:
                self.Attacking = True
                self.Action = True
                self.running_frames = self.attack_right if self.dx>0 else self.attack_left
            for zombie in self.Zombies:
                if zombie.alive:
                    zx, zy = self.cn.coords(zombie.zombieframe)
                    if abs(self.x - zx) < attack_range:
                        zombie.take_damage(1)
                else:
                    continue
            
            self.animate()
            


    def deaction(self, event):
        # Detects when a key is released and resets to original states
        self.Action = False
        self.Running = False
        self.Attacking = False
        self.RunAttacking = False
        self.reset_sprite()
        pass
    
    def animate(self):
        # Animate the player sprite during action
        if self.Action == False or self.state != "game":
            return
        
        self.bounds()
        if not self.mob_collisions(self.dx) and not self.Attacking: 
            self.cn.move(self.Player_Sprite, self.dx, 0)
        if self.Jumping:
            self.cn.itemconfig(self.Player_Sprite, image = self.JumpImg)
        else:
            self.framespeed = 100
            self.frame_index = (self.frame_index +1) % len(self.running_frames)
            self.cn.itemconfig(self.Player_Sprite, image = self.running_frames[self.frame_index])
        self.root.after(self.framespeed, self.animate)

    def bounds(self):
        # Checks if Player Sprite is within the border of the screen/the boundary and doesn't allow further movement
        x = self.cn.coords(self.Player_Sprite)[0]
        if x <= 20 and self.dx < 0:
            self.dx = 0
        elif x >= self.W - 20 and self.dx > 0:
            self.dx = 0

    def reset_sprite(self):
        # Resets the player sprite to the idle position
        self.cn.itemconfig(self.Player_Sprite, image=self.PlayerImg)

    def pause(self):
        # Pauses the game and displays an option menu
        if self.state == "game":
            self.state = "paused"
            self.cn.unbind("<KeyPress>")
            self.cn.unbind("<KeyRelease>") #need to fix this as still detected when paused
            #[key for key in ["d", "a"] if self.bg1_canvas.unbind(f"<KeyRelease-{key}>", self.deaction)]

    def spawn_mobs(self):
        # Spawn in zombies at random intervals and positions along the surface
        x = random.choice([random.randint(0,int(0.25*float(self.W))),random.randint(int(0.75*float(self.W)),self.W)])  # gives random coordinate from either first quarter or fourth quarter of the map, may have to adjust for allowing only integers using randint if cannot move sprites to float/decimal pixels
        y = int(self.H * 0.82)
        zombie = NPC(self.cn, x, y, self.npcwl, self.npcwr, self.npcrl, self.npcrr, self.npcal, self.npcar, self.npcbl, self.npcbr, self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
        self.Zombies.append(zombie)
        zombie.animate()

        spawn_interval = 10000
        # Schedules next spawning mob based on milliseconds in the spawn_interval variable
        self.root.after(spawn_interval, self.spawn_mobs)

    def action_mobs(self):
        # Updates the mobs to move towards the player and if in range inflict damage
        x = self.cn.coords(self.Player_Sprite)[0]
        for zombie in self.Zombies:
            if zombie.alive:
                zombie.moveto(x)
                if zombie.collisions(x):
                    # Logic for attack will be put here
                    pass 
                else:
                    zombie.changestate("walking_right" if zombie.dx > 0 else "walking_left")
        # Continuosly move towards the player and attack
        self.root.after(50, self.action_mobs)

    def mob_collisions(self, dx):
        # Adds collision checks between player and NPCs so that player can not run through them but can jump over them
        px, py = self.cn.coords(self.Player_Sprite)
        next_px = px + dx

        for zombie in self.Zombies:
            if not zombie.alive:
                continue
            zx, zy = x = self.cn.coords(zombie.zombieframe)
            if abs(next_px - zx) < 40:
                if abs(py-zy)<20:
                    # Block movement only towards the zombie as to allow player to escape in opposite direction
                    towards_mob = (dx>0 and next_px<zx) or (dx<0 and next_px>zx)
                    if towards_mob:
                        return True
        return False


    def clear_frame(self):
        # Reset and remove all frames and widgets
        for widget in self.root.winfo_children():
            widget.destroy() 
        #self.start_frame.pack_forget() might want to add this back when project gets too big 

class NPC(App):
    def __init__(self, cn, x, y, NPCWL, NPCWR, NPCRL, NPCRR, NPCAL, NPCAR, NPCBL, NPCBR, NPC1deadR, NPC1deadL, NPC2deadR, NPC2deadL):
        self.cn = cn

        # Initialising animation frames for each possible action
        self.walk_left = NPCWL  #Two different zombies one that only walks(slower and attacks) and one that only runs(faster and bites)
        self.walk_right = NPCWR
        self.run_left = NPCRL
        self.run_right = NPCRR
        self.attack_left = NPCAL
        self.attack_right = NPCAR
        self.bite_left = NPCBL
        self.bite_right = NPCBR
        self.dead1_right = NPC1deadR
        self.dead1_left = NPC1deadL
        self.dead2_right = NPC2deadR
        self.dead2_left = NPC2deadL


        # Initial state and animation settings
        self.state = "idle"
        self.changestate("walking_right")
        self.frames = self.walk_right
        self.frame_index = 0
        IdleZ1 = ImageTk.PhotoImage(Image.open(r"Assets\NPC\Mob1Idle.png"))
        self.zombieframe = self.cn.create_image(x, y, image=IdleZ1, anchor = CENTER)
        self.alive = True
        self.mob_speed = 3
        self.health = 2

        self.animate()

    def changestate(self, new_state):
        # Change the state of the NPC
        if new_state != self.state:
            self.state = new_state
            if new_state == "walking_left":
                self.frames = self.walk_left
            elif new_state == "walking_right":
                self.frames = self.walk_right
            elif new_state == "running_left":
                self.frames = self.run_left
            elif new_state == "running_right":
                self.frames = self.run_right
            elif new_state == "attacking_left":
                self.frames = self.attack_left
            elif new_state == "attacking_right":
                self.frames = self.attack_right
            elif new_state == "dead":
                if self.dx > 0:
                    self.frames = self.dead1_right
                else:
                    self.frames = self.dead1_left
            self.frame_index = 0 
        
    def animate(self):
        # Ques appropriate animation for the NPC
        if not self.alive:    # Deletes dead zombie after death animation ends
            if self.frame_index == len(self.frames) - 1:   
                self.cn.delete(self.zombieframe)
                return
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.cn.itemconfig(self.zombieframe, image=self.frames[self.frame_index])
        self.cn.after(150, self.animate)
            
    def moveto(self, playerx):
        # Moves NPC towards players current coordinates if not already attacking
        if self.state.startswith("attacking"):
            return
        x = self.cn.coords(self.zombieframe)[0]
        self.dx = playerx - x
        if abs(self.dx) > 10: # Minimum distance from player to change direction to avoid endless switching if player close
            direction = "walking_right" if self.dx > 0 else "walking_left"  #only accounts for walking atm
            self.changestate(direction)
            step = min(self.mob_speed, self.dx) if self.dx>0 else max(-self.mob_speed, self.dx)
            self.cn.move(self.zombieframe, step, 0)

    def collisions(self, playerx, attack_range = 30):
        # Checks if mob is close enough to inflict damage unto the player
        x = self.cn.coords(self.zombieframe)[0]
        if abs(playerx - x) < attack_range:
            if not self.state.startswith("attacking"):
                self.changestate(f"attacking_{'right' if self.dx>0 else 'left'}")
            return True
        else:
            return False
        
    def take_damage(self, damage):
        # Reduces health of mob and checks if mob is dead or not
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.changestate("dead")
            

        

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
