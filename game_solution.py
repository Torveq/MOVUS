from tkinter import *
from PIL import Image, ImageTk
import os
import time
import random
import math
import json
import tkinter.font
#from tkinter import ttk
'''Add shapes using actual shape functions circles for pfps in leaderboard for example and use text for death message or smth'''
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets\Icon.ico")
        #self.root.resizable(True,True) doesnt work as intended, trying to upscale the entire thing to provide fullscreen option
        self.root.bind("<Button-1>", self.debugging) # for debugging purposes
        self.root.wm_attributes('-transparentcolor', '#ab23ff')
        self.state_file = "game_state.json"
        self.GameFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=16) # additional options weight, underline, overstrike, slant, etc
        self.InputFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=67) 
        
        # Preloads all frames of animation (NPCWR is an abbreviation for NPC Walk Right BR is bite right AR is attack right etc..)
        self.run_right = self.load_frames("Assets\PlayerRunRight")
        self.run_left = self.load_frames("Assets\PlayerRunLeft")
        self.attack_right = self.load_frames("Assets\RightAttack")
        self.attack_left = self.load_frames("Assets\LeftAttack")
        self.run_attack_right = self.load_frames("Assets\RightRunAttack")
        self.run_attack_left = self.load_frames("Assets\LeftRunAttack")
        self.dead_right = self.load_frames("Assets\PlayerDeadRight")
        self.dead_left = self.load_frames("Assets\PlayerDeadLeft")
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

    def debugging(self, event):
        # As the name suggests
        print(f"Clicked at ({event.x}, {event.y})")

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
        self.clear_frame()
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
        self.play_button = Button(self.start_frame, image=self.button_img, command=self.username_entry, bd=0, highlightthickness=0, padx=0, pady=0)
        #self.play_button.bind("<Key>", self.game) press any key to play
        self.play_button.place(relx=0.5,rely=0.715, anchor = CENTER)

    def username_entry(self):
        self.play_button.config(command=self.game)
        self.NameImg=ImageTk.PhotoImage(Image.open(r"Assets\NameEntry.png").resize((643,74)))
        label = Label(self.start_frame, image=self.NameImg, bd=0, highlightthickness=0,padx=0, pady=0)
        label.place(x=125, y=290, anchor=NW)
        self.user_input= StringVar()
        self.NameInput = Entry(self.start_frame, textvariable=self.user_input, font=(self.InputFont), justify="center", bd=2, bg="#222a5c", width=8, fg="teal")
        self.NameInput.place(x=180, y=100)
        self.NameInput.bind("<Return>", self.game)
        self.user_input.trace("w", self.name_limit)

    def name_limit(self, *args):
        # Ensures that entered username doesnt exceed 10 characters and capitalises the username
        self.username = self.user_input.get().upper()
        if len(self.username) > 8:
            self.user_input.set(self.username[:8])
            self.username = self.username[:8]

    def game(self, event=None):
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

        # Load pause option and game over menus and necessary button images
        self.OptionsImg = ImageTk.PhotoImage(Image.open("Assets\optionsmenu.png"))
        self.GameOverImg = ImageTk.PhotoImage(Image.open("Assets\GameOverMenu.png"))

        # Load and initialize player sprite and set default jumping image orientation
        self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
        self.Player_Sprite = self.cn.create_image(self.W // 2, int(self.H * 0.82), image = self.PlayerImg, anchor = CENTER)
        self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))

        self.Zombies = []

        # Load and initialize player's health bar and score, last time he was hit/direction is set to default 0 to avoid errors on first time of running
        self.Score = 0
        self.ScoreTxt = self.cn.create_text(90, 20, text = f"Score: {self.Score}", font=self.GameFont)  #is this enough text for the rubric?
        self.FullHealthBarImg = ImageTk.PhotoImage(Image.open(r"Assets\HealthBar\100.png").resize((250, 14)))
        self.HP = self.cn.create_image(400, self.H*0.03, image = self.FullHealthBarImg, anchor=NW)
        self.health = 10
        self.last_hit_time = 0
        self.dx = 0

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
            self.y_speed = -3
            self.cn.itemconfig(self.Player_Sprite, image = self.JumpImg) 
            self.Jump()
        
        elif event.char == "w":   #unexpected occurs when player holding down attack and then tries to run in either direction
            if self.Jumping or self.Attacking or self.RunAttacking:
                return  # Prevents attacking if the player is jumping or already attacking
            attack_range = 50
            closest_mob = None
            min_distance = float('inf')  # To track only the closest mob to the player
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
                    zx, zy = self.cn.coords(zombie.zombie_sprite)
                    distance = math.sqrt((self.x -zx)**2 + (self.y -zy)**2)
                    if abs(self.x - zx) < attack_range and distance < min_distance:
                        closest_mob = zombie
                        min_distance = distance
                else:
                    continue
            if closest_mob:
                closest_mob.take_damage(1)  
            
            self.animate()
            


    def deaction(self, event):
        # Detects when a key is released and resets to original states
        self.Action = False
        self.Running = False
        self.Attacking = False
        self.RunAttacking = False
        self.reset_sprite()
        pass
    
    def Jump(self):
        if not self.Jumping or self.state != "game":
            return
        self.y_speed += 0.1 #gravity
        self.cn.move(self.Player_Sprite, 0, self.y_speed)
        self.cn.update()
        if self.cn.coords(self.Player_Sprite)[1] >= self.H * 0.82:
            self.Jumping = False
            self.y_speed = 0
            self.reset_sprite()
        else:
            self.root.after(10, self.Jump)


    def animate(self):
        # Animate the player sprite during action
        if self.state=="end":
            if self.frame_index < len(self.running_frames):
                self.cn.itemconfig(self.Player_Sprite, image=self.running_frames[self.frame_index])
                self.frame_index += 1
                self.root.after(400, self.animate)
            else:
                self.cn.itemconfig(self.Player_Sprite, image=self.running_frames[self.frame_index-1])
                return
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

    def update_score(self):
        self.Score += 1
        #self.ScoreTxt.update() why doesn this work
        self.cn.itemconfig(self.ScoreTxt, text=f"Score: {self.Score}") #self.ScoreTxt.config doesnt work cause its on a canvas and not a standard widget

    def reset_sprite(self):
        # Resets the player sprite to the idle position
        self.cn.itemconfig(self.Player_Sprite, image=self.PlayerImg)

    def save_state(self):
        self.state = "paused"
        for zombie in self.Zombies:
                if not zombie.alive:
                    self.Zombies.remove(zombie)
                    self.cn.delete(zombie.zombie_sprite)  # Removes dead zombies from the list first
        self.game_data = {
            "player": {
                "position": self.cn.coords(self.Player_Sprite),
                "health": self.health, #placeholder for actual health logic
                "score": self.Score
            },
            "zombies": [
                {
                    "position": self.cn.coords(zombie.zombie_sprite),
                    "health": zombie.health,
                    "alive": zombie.alive,
                    "state": zombie.state
                }
                for zombie in self.Zombies
            ],
            "game_state": self.state
        }

        with open(self.state_file, "w") as file:
            json.dump(self.game_data, file)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as file:
                game_data = json.load(file)

            player_data = game_data["player"]
            self.cn.coords(self.Player_Sprite, *player_data["position"])

            for zombie in self.Zombies: 
                self.cn.delete(zombie.zombie_sprite)
            self.Zombies.clear()

            for zombie_data in game_data["zombies"]:
                try:
                    x, y= zombie_data["position"]
                except:
                    continue
                zombie = NPC(self, self.cn, *zombie_data["position"], self.state,
                    self.npcwl, self.npcwr, self.npcrl, self.npcrr,
                    self.npcal, self.npcar, self.npcbl, self.npcbr,
                    self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
                zombie.health = zombie_data["health"]
                zombie.alive = zombie_data["alive"]
                zombie.changestate(zombie_data["state"])
                self.Zombies.append(zombie)

    

    def pause(self):
        # Pauses the game and displays an option menu
        if self.state == "game":
            self.save_state()
            self.state = "paused"
            self.cn.unbind("<KeyPress>")
            self.cn.unbind("<KeyRelease>") #need to fix this as still detected when paused
            #[key for key in ["d", "a", "w"] if self.bg1_canvas.unbind(f"<KeyRelease-{key}>", self.deaction)]
            self.Pause_button.destroy()
            self.OptionsButton = Button(image = self.OptionsImg, borderwidth=0, highlightthickness=0, background="#ab23ff")
            self.OptionsButton.bind("<Button-1>", self.Optionclicked)
            self.OptionsMenu = self.cn.create_window(self.W // 2, int(self.H * 0.5), window = self.OptionsButton, anchor = CENTER)   

            # Pausing mob related stuff
            for zombie in self.Zombies:
                zombie.pauseani()
            self.root.after_cancel(self.spawn_timer)
            self.root.after_cancel(self.mobact_timer)         

    def resume(self):
        # Resume game
        if self.state == "paused":
            self.load_state()
            self.state = "game"
            self.cn.delete(self.OptionsMenu)
            self.cn.focus_set()
            self.cn.bind("<KeyPress>", self.action)
            [key for key in ["d", "a", "w"] if self.cn.bind(f"<KeyRelease-{key}>", self.deaction)]
            # Recreate the pause button
            self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
            self.cn.create_window(20, 20, window=self.Pause_button)
            if self.Jumping:   # to account for pausing mid air
                self.Jump()
            
            # Resuming mob related stuff
            for zombie in self.Zombies:
                zombie.resumeani()
            self.spawn_mobs()
            self.action_mobs()

    def Optionclicked(self, event):
        # Determines what button on the options menu has been pressed
        x, y = event.x, event.y
        if self.state == "paused":
            # X button dimensions x1=405 y1=56 x2=425 y2=77 then for resume, restart, stats, settings, and quit
            dimen = [[174,3,192,22],[14, 39, 178, 71],[16, 85, 178, 116], [17, 130, 178, 162], [15, 175, 178, 206], [17, 221, 177, 250]]
            for d in dimen:
                if (x>d[0] and x<d[2]) and (y>d[1] and y<d[3]):
                    b = dimen.index(d)
                    if b==0:
                        self.resume()
                    elif b==1:
                        self.resume()
                    elif b==2:
                        self.clear_frame()
                        self.game()
                        return
                    elif b==3:
                        pass
                    elif b==4:
                        pass
                    else:
                        self.start_menu()
        elif self.state == "end":
            # dimensions go for quit, leaderboard, and restart buttons respectively
            dimen = [[37,89,73,127],[96,88,133,125],[156,88,194,125]]
            for d in dimen:
                if (x>d[0] and x<d[2]) and (y>d[1] and y<d[3]):
                    b = dimen.index(d)
                    if b==0:
                        self.start_menu()
                    elif b==1:
                        pass  # placeholder for leaderboard function
                    else:
                        self.clear_frame()
                        self.game()

    def game_over(self):
        # Ends the game sets all zombies to idle position and stops them and plays death animation of player and loads game over screen
        self.dmsgs = [f"{self.username} was eviscerated.", f"{self.username} was brutally dissected.", f"{self.username} had both kidneys stolen.", f"{self.username}'s body was donated to science.", f"{self.username} received a forced amputation.", f"{self.username} was voluntold to donate blood.", f"{self.username} had an unsuccessful lobotomy."]
        for zombie in self.Zombies:
            zombie.changestate("idle")
        self.running_frames = self.dead_right if self.dx>0 else self.dead_left
        self.state="end"
        self.root.after_cancel(self.spawn_timer)
        self.root.after_cancel(self.mobact_timer)
        self.animate() 
        self.Pause_button.destroy()
        self.deathmsg = self.cn.create_text(self.W//2, 230, text = self.dmsgs[random.randint(0, len(self.dmsgs)-1)], font=self.GameFont, anchor=CENTER, fill="#E11919", tags="death_msg")
        #self.transp_bg = self.cn.create_rectangle(0, 270, self.W, 200, fill="#000000", outline="", alpha=0.5) #need to update python from 3.10 to update tkinter
        for i in range(3):
            self.cn.create_rectangle(0, 260, self.W, 200, fill="#000000", outline="", stipple="gray50", tags="bg")  # Stipple pattern for transparency effect of text bg
        self.cn.tag_raise("death_msg", "bg") # to display text on top of transparent bg
        self.OverButton = Button(image = self.GameOverImg, borderwidth=0, highlightthickness=0, background="#ab23ff")
        self.OverButton.bind("<Button-1>", self.Optionclicked)
        self.GameOverMenu = self.cn.create_window(self.W // 2, int(self.H * 0.3), window = self.OverButton, anchor = CENTER)

        

    def spawn_mobs(self):
        # Spawn in zombies at random intervals and positions along the surface
        x = random.choice([random.randint(0,int(0.25*float(self.W))),random.randint(int(0.75*float(self.W)),self.W)])  # gives random coordinate from either first quarter or fourth quarter of the map, may have to adjust for allowing only integers using randint if cannot move sprites to float/decimal pixels
        y = int(self.H * 0.82)
        zombie = NPC(self, self.cn, x, y, self.state, self.npcwl, self.npcwr, self.npcrl, self.npcrr, self.npcal, self.npcar, self.npcbl, self.npcbr, self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
        self.Zombies.append(zombie)
        zombie.animate()

        spawn_interval = 10000
        # Schedules next spawning mob based on milliseconds in the spawn_interval variable
        self.spawn_timer=self.root.after(spawn_interval, self.spawn_mobs)

    def take_damage(self):
        ctime = time.time()
        if ctime - self.last_hit_time >= 2:  # 2 second cooldown for damaging the player
            self.health -= 10
            if self.health < 0 and self.state!="end":
                self.health=0
                self.game_over()
                return
            else:
                self.newhealthimg = ImageTk.PhotoImage(Image.open(f"Assets\HealthBar\{self.health}.png").resize((250, 14)))  # if i dont attribute it to the class tkinter thing will do smth called garbage collecting idk why ask
                self.cn.itemconfig(self.HP, image = self.newhealthimg)
                self.last_hit_time = ctime

    def action_mobs(self):
        # Updates the mobs to move towards the player and if in range inflict damage
        x = self.cn.coords(self.Player_Sprite)[0]
        for zombie in self.Zombies:
            if zombie.alive:
                zombie.moveto(x)
                if zombie.collisions(x) and self.state!="end":
                    self.take_damage()
                elif self.state=="end":
                    zombie.changestate("idle")
                    return
                else:
                    zombie.changestate("walking_right" if zombie.dx > 0 else "walking_left")
        # Continuosly move towards the player and attack
        self.mobact_timer=self.root.after(50, self.action_mobs)

    def mob_collisions(self, dx):
        # Adds collision checks between player and NPCs so that player can not run through them but can jump over them
        px, py = self.cn.coords(self.Player_Sprite)
        next_px = px + dx

        for zombie in self.Zombies:
            if not zombie.alive:
                continue
            zx, zy = self.cn.coords(zombie.zombie_sprite)
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
    def __init__(self, app, cn, x, y, PlayerState, NPCWL, NPCWR, NPCRL, NPCRR, NPCAL, NPCAR, NPCBL, NPCBR, NPC1deadR, NPC1deadL, NPC2deadR, NPC2deadL): #placeholder defaults to prevent errors for now for when mob 2 is to be added to the game
        
        self.app =app
        self.cn = cn
        self.Pstate = PlayerState
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
        self.Animating = True
        self.state = "idle"
        self.changestate("walking_right")
        self.frames = self.walk_right
        self.frame_index = 0
        self.IdleZ1 = ImageTk.PhotoImage(Image.open(r"Assets\NPC\Mob1Idle.png"))
        self.zombie_sprite = self.cn.create_image(x, y, image=self.IdleZ1, anchor = CENTER)
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
            elif new_state == "idle":
                self.frames = None  # might raise errors 
            elif new_state == "dead":
                if self.dx > 0:
                    self.frames = self.dead1_right
                else:   #doesnt really show animation if moving towards player from east to west 
                    self.frames = self.dead1_left
            self.frame_index = 0 
        
    def animate(self):
        # Ques appropriate animation for the NPC
        if self.frames is None:
            self.cn.itemconfig(self.zombie_sprite, image=self.IdleZ1)
            return
        if not self.Animating:
            return
        if not self.alive:    # Deletes dead zombie after death animation ends
            if self.frame_index == len(self.frames) - 1:   
                self.cn.delete(self.zombie_sprite)
                return
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.cn.itemconfig(self.zombie_sprite, image=self.frames[self.frame_index])
        self.mobanimate = self.cn.after(150, self.animate)

    def pauseani(self):
        self.cn.after_cancel(self.mobanimate)
        self.Animating = False

    def resumeani(self):
        self.Animating = True
        self.animate()
            
    def moveto(self, playerx):
        # Moves NPC towards players current coordinates if not already attacking
        if self.state.startswith("attacking"):
            return
        x = self.cn.coords(self.zombie_sprite)[0]
        self.dx = playerx - x
        if abs(self.dx) > 10: # Minimum distance from player to change direction to avoid endless switching if player close
            direction = "walking_right" if self.dx > 0 else "walking_left"  #only accounts for walking atm
            self.changestate(direction)
            step = min(self.mob_speed, self.dx) if self.dx>0 else max(-self.mob_speed, self.dx)
            self.cn.move(self.zombie_sprite, step, 0)

    def collisions(self, playerx, attack_range = 30):
        # Checks if mob is close enough to inflict damage unto the player
        x = self.cn.coords(self.zombie_sprite)[0]
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
            self.app.update_score()
            self.changestate("dead")
            

        

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
