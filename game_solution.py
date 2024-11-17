from tkinter import *
from PIL import Image, ImageTk
from Leaderboard import *
from idlelib.tooltip import Hovertip
#from tkinter.tix import *
import os
import time
import random
import math
import json
import tkinter.font
#from tkinter import ttk
'''Add shapes using actual shape functions circles for pfps in leaderboard for example and use text for death message or smth
   also try get the cursor to work
   also add next to settings on start menu a how to play based on the craft pix ting just copy+paste'''
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets\Icon.ico")
        #self.root.resizable(True,True) doesnt work as intended, trying to upscale the entire thing to provide fullscreen option
        self.state = "initialising"
        self.prev_state = None
        self.BossKeyTransparent = False
        self.saves_folder = "PlayerSaves"
        self.root.bind("<Button-1>", self.debugging) # for debugging purposes
        self.root.wm_attributes('-transparentcolor', '#ab23ff')
        self.GameFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=16) # additional options weight, underline, overstrike, slant, etc
        self.InputFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=67) # add other font incase character not accounted for in custom is used
        self.LBFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=10)

        self.key_binds = {
            "attack": "w",
            "right": "d",
            "left": "a",
            "jump": "space",
            "bosskey": "b"
        }

        # Preloads all frames of animation (NPCWR is an abbreviation for NPC Walk Right BR is bite right AR is attack right etc..)
        self.leaderboard_bg = self.load_frames("Assets\Leaderboard_BG")
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
            elif filename.endswith(".jpg"):
                image = Image.open(os.path.join(folder, filename))
                frames.append(ImageTk.PhotoImage(image))
        return frames  #could use .self instead but to be more modular ig

    def start_menu(self):
        # Reset screen
        self.clear_frame()
        self.state = "menu"
        # Load previous settings(keybinds) if available
        self.load_settings()
        # Create a frame for the start menu with dimesniosn equal to that of the image
        self.start_img = Image.open("Assets/MainMenue.png")
        self.W, self.H = self.start_img.size
        self.start_frame = Frame(self.root, width=self.W, height=self.H)
        self.start_frame.pack(fill="both", expand=True)

        # Load and display the start image
        self.start_img = ImageTk.PhotoImage(self.start_img)
        label = Label(self.start_frame, image=self.start_img)
        label.pack()

        # Button to start the game and assume default username
        self.username = "GUEST"
        self.button_img = ImageTk.PhotoImage(Image.open("Assets\PlayButton.png"))
        self.play_button = Button(self.start_frame, image=self.button_img, command=self.username_entry, bd=0, highlightthickness=0, padx=0, pady=0)
        #self.play_button.bind("<KeyPress>", self.game) #press any key to play
        self.play_button.place(relx=0.5,rely=0.715, anchor = CENTER)

        # Leaderboard button
        self.lb_button_img = ImageTk.PhotoImage(Image.open("Assets\LB_StartMenu.png"))
        self.lb_button = Button(self.start_frame, image=self.lb_button_img, command=self.leaderboard, bd=0, highlightthickness=0, padx=0, pady=0)
        Hovertip(self.lb_button, "Displays leaderboard", hover_delay=1000) # 1000ms delay before showing tooltip
        self.lb_button.place(x=792, y=546, anchor=NW)

        # Settings button
        self.set_b_img = ImageTk.PhotoImage(Image.open("Assets\Settings_StartMenu.jpg"))
        self.set_b = Button(self.start_frame, image=self.set_b_img, command=self.settings, bd=0, highlightthickness=0, padx=0, pady=0)
        Hovertip(self.set_b, "Opens keybinds remapping", hover_delay=1000)
        self.set_b.place(x=1, y=594, anchor=SW)

    def username_entry(self):
        self.play_button.config(command=self.game)
        self.NameImg=ImageTk.PhotoImage(Image.open(r"Assets\NameEntry.png").resize((643,74)))
        label = Label(self.start_frame, image=self.NameImg, bd=0, highlightthickness=0,padx=0, pady=0)
        label.place(x=125, y=290, anchor=NW)
        self.user_input= StringVar()
        self.NameInput = Entry(self.start_frame, textvariable=self.user_input, font=(self.InputFont), justify="center", bd=2, bg="#222a5c", width=8, fg="teal")
        self.NameInput.place(x=180, y=100)
        self.NameInput.focus_set()
        self.NameInput.bind("<Return>", self.game)
        self.user_input.trace("w", self.name_limit)

    def name_limit(self, *args):
        # Ensures that entered username doesnt exceed 8 characters and capitalises the username
        self.username = self.user_input.get().upper()
        if len(self.username) > 8:
            self.user_input.set(self.username[:8])
            self.username = self.username[:8]
        elif len(self.username) == 0:
            self.username = "GUEST"

    def settings(self):
        self.prev_state = self.state
        self.state="settings"

        # Make settings display menu
        self.settingsImg = Image.open("Assets\SettingsMenu.png")
        sW, sH = self.settingsImg.size
        self.settings_frame = Frame(root, width=sW-3, height=sH-2, bg="black", bd=0)
        self.settings_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.settingsImg = ImageTk.PhotoImage(self.settingsImg)
        label = Label(self.settings_frame, image=self.settingsImg)
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Remapping keybinds
        self.key_buttons = {}
        i = 0
        for action, key in self.key_binds.items():
            KeyB = Button(self.settings_frame, text=key, command=lambda a=action: self.Remap(a), font=(self.GameFont), bd=2, bg="#222a5c", fg="green")
            # we do a=action because of pythons closure behaviour in loops where lambda takes a refrence of any parameter at the end of the loop then runs 
            KeyB.place(x=185, y= 74+i*68)
            KeyB.lift()
            self.key_buttons[action] = KeyB
            i+=1

        # Display duplicate key warnings upon reopening settings
        self.refresh_warnings()

        # X button to leave settings menu
        self.xb_img = ImageTk.PhotoImage(Image.open(r"Assets\x_button.png").resize((31,31)))
        self.x_lb = Button(self.settings_frame, image=self.xb_img, command=self.CloseSettings, bd=0, highlightthickness=0, padx=0, pady=0)
        self.x_lb.place(x=260,y=9, anchor = NW)

        # Dropdown menu to select boss key functionality
        options = ["Boss-Key1:", "Boss-Key2:"]
        clicked =StringVar()
        clicked.set(options[0 if self.BossKeyTransparent==False else 1])
        dropdown = OptionMenu(self.settings_frame, clicked, *options)
        dropdown.config(font=self.GameFont, bg="#222a5c", fg="white", activeforeground="black", bd=0, border=0, highlightthickness=2, highlightbackground="black",indicatoron=0)
        dropdown.place(x=28, y= 348, anchor=NW)
        dropdown['menu'].config(font=("CyberpunkCraftpixPixel", 10), bg="#222a5c", fg="white", activeforeground="black", bd=0, border=0, activeborder=0)
        # Checks which boss key has been selected
        if clicked.get()=="Boss-Key2:":
            self.BossKeyTransparent = True
        else:
            self.BossKeyTransparent = False


    def Remap(self, action):
        button = self.key_buttons[action]
        button.focus_set()
        button.bind("<KeyPress>", lambda event: self.capture_key(event, action, button))

    def capture_key(self, event, action, button):
        key = event.keysym 
        self.key_binds[action] = key  
        button.config(text=key) 
        self.refresh_warnings()
        self.save_settings() 
        button.unbind("<KeyPress>")  

    def warn_duplicate(self, current_action, key):
        for action, bound_key in self.key_binds.items():
            if current_action!=action and key==bound_key: 
                return True
        return False
    
    def refresh_warnings(self):
        for action, button in self.key_buttons.items():
            button.config(fg="green")
        for action1, key1 in self.key_binds.items():
            for action2, key2 in self.key_binds.items():
                if action1 != action2 and key1 == key2:
                    self.key_buttons[action1].config(fg="red")
                    self.key_buttons[action2].config(fg="red")

    def save_settings(self):
        # saves key binds so that they aren't lost when the game is closed, its own function rather than joined with save_state to make keybinds global to all users and not just one
        with open("settings.json", "w") as file:
            json.dump(self.key_binds, file)

    def load_settings(self):
        # loads keybinds from the json file
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                self.key_binds = json.load(file)

    def CloseSettings(self):
        self.settings_frame.destroy()
        self.state=self.prev_state
    

    def game(self, event=None):
        # Check if restarting the game to clear any saved file
        if self.state == "restart":
            filename = f"PlayerSaves\{self.username}_game_state.json"
            if os.path.exists(filename):
                os.remove(filename)

        # Reset Screen
        self.clear_frame()
        self.state = "game"

        # Load and initialise game background assets
        self.WaveBreakImg = ImageTk.PhotoImage(Image.open("Assets\WaveBreak.jpg"))

        # Create an initial game frame
        self.gamebg_1 = Image.open("Assets\Gamebg_1.png")
        self.W, self.H = self.gamebg_1.size
        self.game_frame = Frame(self.root, width=self.W, height=self.H)
        self.game_frame.pack(fill="both", expand=True)

        # Load and initialise first game scene
        self.gamebg_1 = ImageTk.PhotoImage(self.gamebg_1)
        self.cn = Canvas(self.game_frame, width=self.W, height=self.H)
        self.cn.pack()
        self.GameBG = self.cn.create_image(0,0,image=self.gamebg_1, anchor = NW)

        # Load pause option and game over menus and necessary button images
        self.OptionsImg = ImageTk.PhotoImage(Image.open("Assets\optionsmenu.png"))
        self.GameOverImg = ImageTk.PhotoImage(Image.open("Assets\GameOverMenu.png"))

        # Load and initialize player sprite and set default jumping image orientation
        self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
        self.Player_Sprite = self.cn.create_image(self.W // 2, int(self.H * 0.82), image = self.PlayerImg, anchor = CENTER)
        self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))
        self.HurtR = ImageTk.PhotoImage(Image.open("Assets\HurtRight.png").resize((80,80)))
        self.HurtL = ImageTk.PhotoImage(Image.open("Assets\HurtLeft.png").resize((80,80)))
        self.IdleR = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
        self.IdleL = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleL.png"))

        self.Zombies = []
        
        # Load and initialize variables, and last time he was hit/direction is set to default 0 to avoid errors on first time of running
        self.konami_sequence = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "b", "a", "Return"]
        self.key_sequence = []
        self.WaveNum = 0
        self.Score = 0
        self.scorepwave = 5
        self.spawn_interval = 10000
        self.zombie_num = 0
        self.remaining_time = 0
        self.ScoreTxt = self.cn.create_text(90, 20, text = f"Score: {self.Score}", font=self.GameFont)
        self.FullHealthBarImg = ImageTk.PhotoImage(Image.open(r"Assets\HealthBar\100.png").resize((250, 14)))
        self.HP = self.cn.create_image(400, self.H*0.03, image = self.FullHealthBarImg, anchor=NW)
        self.health = 100
        self.last_hit_time = 0
        self.dx = 0

        # Detect keys pressed and released for appropriate action
        self.Action = False
        self.Running = False
        self.Jumping = False  # could be using a dictionary here instead
        self.Attacking = False
        self.RunAttacking = False
        
        self.cn.focus_set()
        self.cn.bind("<KeyPress>", self.action)
        [key for key in [self.key_binds["attack"],self.key_binds["right"],self.key_binds["left"]] if self.cn.bind(f"<KeyRelease-{key}>", self.deaction)]
        #self.cn.bind("<ButtonRelease-1>", self.deaction) later for when i implement attacking via left mouse button 
        
        # Load previous save(if available) of the player with the same username
        self.load_state()
        self.Jump()

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

        self.check_cheat_code(event.keysym)

        if event.keysym == self.key_binds["right"] and self.x < self.W - 20:
            if not self.mob_collisions(dx=10):
                self.running_frames = self.run_right
                self.dx = 10
                self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleR.png"))
                self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpRight.png").resize((80,80)))
                if not self.Running:
                    self.Running = True
                    self.Action = True
                    self.animate()

        elif event.keysym == self.key_binds["left"] and self.x > 20:
            if not self.mob_collisions(dx=-10):
                self.running_frames = self.run_left
                self.dx = -10
                self.PlayerImg = ImageTk.PhotoImage(Image.open("Assets\PlayerIdleL.png"))
                self.JumpImg = ImageTk.PhotoImage(Image.open("Assets\PlayerJump\JumpLeft.png").resize((80,80)))
                if not self.Running:
                    self.Running = True
                    self.Action = True
                    self.animate()

        elif (event.keysym == self.key_binds["jump"] and not self.Jumping) and (self.x <= (self.W - 10) and self.x >= 20): #right boundary shorter than left due to extra leading transparent pixels when sprite facing east
            self.Jumping = True
            self.y_speed = -3
            self.cn.itemconfig(self.Player_Sprite, image = self.JumpImg) 
            self.Jump()
        
        elif event.keysym == self.key_binds["attack"]:   #unexpected occurs when player holding down attack and then tries to run in either direction
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
        if self.state=="loaded":  # to account for the case where a save is loaded where the player is mid air
            self.Jumping=True
            self.state="game"
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
        elif self.state=="lb":
            self.frame_index = (self.frame_index +1) % len(self.running_frames)
            self.lbcn.itemconfig(self.lbbg, image = self.running_frames[self.frame_index])
            self.delay = 4000 if self.frame_index%2==0 else 100
            self.root.after(self.delay, self.animate)

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

    def check_cheat_code(self, key):
        self.key_sequence.append(key)
        if self.key_sequence[-len(self.konami_sequence):] == self.konami_sequence:
            self.cheat_code()
            self.key_sequence.clear() # or we can do self.key_sequence = [] to clear the list
        elif len(self.key_sequence) > len(self.konami_sequence):
            self.key_sequence.pop(0)

    def cheat_code(self):
        print("LETS GO")
        pass

    def update_score(self):
        self.Score += 1
        #self.ScoreTxt.update() why doesn this work
        self.cn.itemconfig(self.ScoreTxt, text=f"Score: {self.Score}") #self.ScoreTxt.config doesnt work cause its on a canvas and not a standard widget
        if self.Score % self.scorepwave == 0 and self.Score != 0:
            self.WaveNum += 1
            self.root.after_cancel(self.spawn_timer)
            self.root.after_cancel(self.mobact_timer)
            self.Pause_button.destroy()
            self.cn.itemconfig(self.GameBG, image=self.WaveBreakImg)
            self.typewriter()
            self.root.after(self.delta*len(self.WaveMsg), self.start_wave)
            
    def start_wave(self):
        self.cn.delete(self.WaveTxt)
        
        self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
        self.cn.create_window(20, 20, window=self.Pause_button)
        self.cn.itemconfig(self.GameBG, image=self.gamebg_1)
        self.spawn_mobs()
        self.action_mobs()

    def typewriter(self):
        self.WaveMsg = f"Wave {self.WaveNum} is approaching...                                                      "
        self.WaveTxt = self.cn.create_text(self.W//2, self.H*0.35, text='', font=self.InputFont, fill="black")
        self.delta = 300
        delay = 0
        for i in range(len(self.WaveMsg)+1):
            s = self.WaveMsg[:i]
            updatedtxt = lambda s=s: self.cn.itemconfig(self.WaveTxt, text=s)
            self.cn.after(delay, updatedtxt)
            delay += self.delta


    def reset_sprite(self):
        # Resets the player sprite to the idle position
        self.cn.itemconfig(self.Player_Sprite, image=self.IdleR if self.dx>0 else self.IdleL)

    def save_state(self):
        self.state = "paused"
        self.state_file = os.path.join(self.saves_folder, f"{self.username}_game_state.json")
        for zombie in self.Zombies:
                if not zombie.alive:
                    self.Zombies.remove(zombie)
                    self.cn.delete(zombie.zombie_sprite)  # Removes dead zombies from the list first
        self.game_data = {
            "player": {
                "name": self.username,
                "position": self.cn.coords(self.Player_Sprite),
                "health": self.health, 
                "score": self.Score,
                "jumping": self.Jumping,
                "airspeed": self.y_speed if self.Jumping else 0
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
        if os.path.exists(f"PlayerSaves\{self.username}_game_state.json"):
            self.state_file = f"PlayerSaves\{self.username}_game_state.json"
            with open(self.state_file, "r") as file:
                game_data = json.load(file)

            player_data = game_data["player"]

            self.cn.coords(self.Player_Sprite, *player_data["position"])
            # Load in saved HP bar
            self.health = player_data["health"]
            self.newhealthimg = ImageTk.PhotoImage(Image.open(f"Assets\HealthBar\{self.health}.png").resize((250, 14)))  
            self.cn.itemconfig(self.HP, image = self.newhealthimg)
            # Load in saved score
            self.Score = player_data["score"]
            self.cn.itemconfig(self.ScoreTxt, text=f"Score: {self.Score}")
            # To account for a save where player is in mid air 
            if player_data["jumping"]:
                self.state="loaded"
                self.y_speed=player_data["airspeed"]
                self.Jump()

            for zombie in self.Zombies: 
                self.cn.delete(zombie.zombie_sprite)
            self.Zombies.clear()

            for zombie_data in game_data["zombies"]:
                try:
                    x, y= zombie_data["position"]
                except:
                    continue
                zombie = NPC(self, self.cn, *zombie_data["position"], self.state, self.Score, self.WaveNum,
                    self.npcwl, self.npcwr, self.npcrl, self.npcrr,
                    self.npcal, self.npcar, self.npcbl, self.npcbr,
                    self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
                zombie.health = zombie_data["health"]
                zombie.alive = zombie_data["alive"]
                zombie.changestate(zombie_data["state"])
                self.Zombies.append(zombie)
        else:
            self.state_file = os.path.join(self.saves_folder, f"{self.username}_game_state.json")
            self.health=100
            self.Score = 0
            self.Zombies.clear()

    def leaderboard(self):
        self.prev_state = self.state
        self.state="lb"
        self.running_frames = self.leaderboard_bg

        # Make leaderboard initial frame background
        self.lb_frame = Frame(root, width=600, height=300, bg="#ab23ff", bd=0)
        self.lb_frame.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        self.lbcn = Canvas(self.lb_frame, width=600, height=300, borderwidth=0, highlightthickness=0)
        self.lbcn.pack()
        self.lbbg=self.lbcn.create_image(0,0,image=self.running_frames[0], anchor = NW)
        # X button to leave leaderboard
        self.xb_img = ImageTk.PhotoImage(Image.open(r"Assets\x_button.png"))
        self.x_lb = Button(self.lb_frame, image=self.xb_img, command=self.CloseLB, bd=0, highlightthickness=0, padx=0, pady=0)
        xv = 536 if self.prev_state=="menu" else 422
        self.x_lb.place(x=xv,y=16, anchor = NW)

        display_leaderboard(self.lbcn)
        display_scores(self.lb_frame, self.lbcn, self.GameFont, self.LBFont)
        self.animate()

    def CloseLB(self):
        self.lb_frame.destroy()
        self.state=self.prev_state

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

            # trying to create another shape for the rubric but not working
            #points = [40, 260, 165, 260, 150, 266, 50, 266]
            #self.polygondesign = self.cn.create_polygon(points, outline = "blue", fill = "orange", width = 2)
            #self.polygondesign.place(x=23, y=258, anchor = "NW")
            
            # Pausing mob related stuff calculating remainig time for the next mob spawn
            self.root.after_cancel(self.spawn_timer)
            self.remaining_time = max(0, (self.spawn_interval/1000) - (time.time() - self.elapsed_spawn_time))
            for zombie in self.Zombies:
                zombie.pauseani()
            self.root.after_cancel(self.mobact_timer)         

    def resume(self):
        # Resume game
        if self.state == "paused":
            self.load_state()
            self.state = "game"
            self.cn.delete(self.OptionsMenu)
            self.cn.focus_set()
            self.cn.bind("<KeyPress>", self.action)
            [key for key in [self.key_binds["attack"],self.key_binds["right"],self.key_binds["left"]] if self.cn.bind(f"<KeyRelease-{key}>", self.deaction)]
            # Recreate the pause button
            self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
            self.cn.create_window(20, 20, window=self.Pause_button)
            if self.Jumping:   # to account for pausing mid air
                self.Jump()
            
            # Resuming mob related stuff
            for zombie in self.Zombies:
                zombie.resumeani()
            print(self.zombie_num, self.scorepwave, "hey")
            if self.zombie_num<self.scorepwave:
                if self.remaining_time > 0:
                    self.spawn_timer = self.root.after(int(self.remaining_time*1000), self.spawn_mobs)
                else:
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
                        self.state="restart"
                        self.clear_frame()
                        self.game()
                        return
                    elif b==3:
                        self.leaderboard()
                    elif b==4:
                        self.settings()
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
                        self.leaderboard()
                    else:
                        self.state="restart"
                        self.clear_frame()
                        self.game()

    def game_over(self):
        # Ends the game sets all zombies to idle position and stops them and plays death animation of player and loads game over screen
        save_score(self.username, self.Score) # for leaderboard
        self.dmsgs = [f"{self.username} was eviscerated.", f"{self.username} was brutally dissected.", f"{self.username} had both kidneys stolen.", f"{self.username}'s body was donated to science.", f"{self.username} received a forced amputation.", f"{self.username} was voluntold to donate blood.", f"{self.username} suffered from a tragic lobotomy."]
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
        # Spawn in zombies at random intervals and positions along the surface unless zombie cap for wave is reached
        
        self.elapsed_spawn_time = time.time()
        x = random.choice([random.randint(0,int(0.25*float(self.W))),random.randint(int(0.75*float(self.W)),self.W)])  # gives random coordinate from either first quarter or fourth quarter of the map, may have to adjust for allowing only integers using randint if cannot move sprites to float/decimal pixels
        y = int(self.H * 0.82)
        zombie = NPC(self, self.cn, x, y, self.state, self.Score, self.WaveNum, self.npcwl, self.npcwr, self.npcrl, self.npcrr, self.npcal, self.npcar, self.npcbl, self.npcbr, self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
        self.Zombies.append(zombie)
        zombie.animate()
        zombie.NextWave()   # does modifications to the zombie based on the wave number

        self.zombie_num +=1

        # Schedules next spawning mob based on milliseconds in the spawn_interval variable
        self.spawn_timer=self.root.after(self.spawn_interval, self.spawn_mobs)

        if self.zombie_num >= self.scorepwave:
            self.zombie_num = 0
            self.root.after_cancel(self.spawn_timer)

    def take_damage(self):
        ctime = time.time()
        if ctime - self.last_hit_time >= 2:  # 2 second cooldown for damaging the player
            self.health -= 10
            self.cn.itemconfig(self.Player_Sprite, image = self.HurtR if self.dx>0 else self.HurtL)
            self.root.after(200, self.reset_sprite)  # adds 200 ms delay before undisplaying the hurt sprite
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
    def __init__(self, app, cn, x, y, PlayerState, PlayerScore, WaveNumb, NPCWL, NPCWR, NPCRL, NPCRR, NPCAL, NPCAR, NPCBL, NPCBR, NPC1deadR, NPC1deadL, NPC2deadR, NPC2deadL): #placeholder defaults to prevent errors for now for when mob 2 is to be added to the game
        
        self.app =app
        self.cn = cn
        self.Pstate = PlayerState
        self.Pscore = PlayerScore
        self.Wave = WaveNumb

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
        self.dx = 0
        self.IdleZ1 = ImageTk.PhotoImage(Image.open(r"Assets\NPC\Mob1Idle.png"))
        self.zombie_sprite = self.cn.create_image(x, y, image=self.IdleZ1, anchor = CENTER)
        self.alive = True
        self.mob_speed = 3
        self.health = 1

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
    
    def NextWave(self):
        # To increase difficulty from wave to wave
        if self.Wave != 0:
            if self.Wave == 1:
                self.health = 2
            if self.Wave%5==0:
                self.app.scorepwave += 5
            if self.Wave%3==0:
                self.health += 1
        
        # every round changes
        self.mob_speed += 1
        self.app.spawn_interval -= 500 if self.app.spawn_interval>2000 else 0

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
