from tkinter import *
from PIL import Image, ImageTk
from Leaderboard import *
from idlelib.tooltip import Hovertip
import os
import time
import random
import math
import json
import tkinter.font
import webbrowser

class App:
    """
    Main application class for the MOVUS game, handling game initialization, 
    menu management, game mechanics, and user interactions.
    
    Manages game states, sprite animations, player controls, 
    and overall game flow across different screens and modes.
    """

    def __init__(self, root):
        """
        Initialize the game application with root window, 
        load assets, and set up initial game state.

        Args:
            root(tk.Tk): The main tkinter window for the application/game
        """
        self.root = root
        self.root.title("MOVUS")
        self.root.iconbitmap("Assets\Icon.ico")
        self.state = "initialising"
        self.prev_state = None
        self.BossKeyTransparent = 0
        self.saves_folder = "PlayerSaves"
        self.root.wm_attributes('-transparentcolor', '#ab23ff')
        self.GameFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=16) # additional options weight, underline, overstrike, slant, etc
        self.InputFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=67) # add other font incase character not accounted for in custom is used
        self.LBFont = tkinter.font.Font(family="CyberpunkCraftpixPixel", size=10)

        self.key_binds = {
            "attack": "w",
            "right": "d",
            "left": "a",
            "jump": "space",
            "bosskey": "b",
            "bosstype": 0
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


    def load_frames(self, folder):
        """
        Load and resize animation frames from a specified folder.
        
        Args:
            folder (str): Path to the folder containing sprite animation frames
        
        Returns:
            list: List of PhotoImage objects representing animation frames
        """
        self.frame_index = 0
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                image = Image.open(os.path.join(folder, filename)).resize((80,80))
                frames.append(ImageTk.PhotoImage(image))
            elif filename.endswith(".jpg"):
                image = Image.open(os.path.join(folder, filename))
                frames.append(ImageTk.PhotoImage(image))
        return frames  #could use .self instead but to be more modular

    def start_menu(self):
        """
        Create and display the game's start menu screen.
        Sets up buttons for play, leaderboard, settings, and social links.
        """
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
        self.play_button.bind("<Return>", lambda event: self.play_button.invoke())  # Bind Enter key to play button
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

        # Small "How to Play" button
        self.htp_b_img = ImageTk.PhotoImage(Image.open("Assets\HowToPlayButton.jpg"))
        self.htp_b = Button(self.start_frame, image=self.htp_b_img, command=self.tipscreen, bd=0, highlightthickness=0, padx=0, pady=0)
        Hovertip(self.htp_b, "How to play", hover_delay=1000)
        self.htp_b.place(x=49, y=594, anchor=SW)

        # Socials button
        url = "https://www.instagram.com/torsoq/profilecard/?igsh=NW9oY3Bjbm4xdW4="
        self.soc_b_img = ImageTk.PhotoImage(Image.open("Assets\SocialsButton.png"))
        self.soc_b = Button(self.start_frame, image=self.soc_b_img, command=lambda: webbrowser.open(url), bd=0, highlightthickness=0, padx=0, pady=0)
        Hovertip(self.soc_b, "Open socials webpage on default browser", hover_delay=1000)
        self.soc_b.place(x=840, y=590, anchor=SW)

    def username_entry(self):
        """
        Provide an interface for the player to enter their username.
        Restricts username length and format.
        """
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
        """
        Limit and format the entered username.
        Ensures username is capitalized and no longer than 8 characters.
        """
        self.username = self.user_input.get().upper()
        if len(self.username) > 8:
            self.user_input.set(self.username[:8])
            self.username = self.username[:8]
        elif len(self.username) == 0:
            self.username = "GUEST"

    def settings(self):
        """
        Open the game settings menu, allowing key binding remapping 
        and boss key type selection.
        """
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
        # Overlay other buttons with transparent rectangle to prevent pressing them once pressed
        self.block_b = Canvas(self.start_frame, width=900, height=60, bg="#ab23ff", bd=0, highlightthickness=0)
        self.block_b.place(x=0, y=540, anchor=NW)
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
        self.clicked =StringVar()
        self.clicked.set(options[0 if self.BossKeyTransparent==0 else 1])
        dropdown = OptionMenu(self.settings_frame, self.clicked, *options)
        dropdown.config(font=self.GameFont, bg="#222a5c", fg="white", activeforeground="black", bd=0, border=0, highlightthickness=2, highlightbackground="black",indicatoron=0)
        dropdown.place(x=28, y= 348, anchor=NW)
        dropdown['menu'].config(font=("CyberpunkCraftpixPixel", 10), bg="#222a5c", fg="white", activeforeground="black", bd=0, border=0, activeborder=0)
        self.clicked.trace_add("write", self.UpdateBossKey)

    def UpdateBossKey(self, *args):
        """
        Update boss key settings based on user selection.
        """
        if self.clicked.get()=="Boss-Key2:":
            self.BossKeyTransparent = 1
            self.save_settings()
        else:
            self.BossKeyTransparent = 0
            self.save_settings()

    def Remap(self, action):
        """
        Initiate key remapping for a specific game action.
        
        Args:
            action (str): The game action to remap (e.g., 'attack', 'jump')
        """
        button = self.key_buttons[action]
        button.focus_set()
        button.bind("<KeyPress>", lambda event: self.capture_key(event, action, button))

    def capture_key(self, event, action, button):
        """
        Capture and set a new key binding for a specific game action.
        
        Args:
            event: Tkinter key press event
            action (str): The game action being remapped
            button (tk.Button): The button representing the action
        """
        key = event.keysym 
        self.key_binds[action] = key  
        button.config(text=key) 
        self.refresh_warnings()
        self.save_settings() 
        button.unbind("<KeyPress>")  

    def warn_duplicate(self, current_action, key):
        """
        Check if a key binding is already used by another action.
        
        Args:
            current_action (str): The current action being checked
            key (str): The key to check for duplicates
        
        Returns:
            bool: True if key is a duplicate, False otherwise
        """
        for action, bound_key in self.key_binds.items():
            if current_action!=action and key==bound_key: 
                return True
        return False
    
    def refresh_warnings(self):
        """
        Update button colors to indicate duplicate key bindings.
        """
        for action, button in self.key_buttons.items():
            button.config(fg="green")
        for action1, key1 in self.key_binds.items():
            for action2, key2 in self.key_binds.items():
                if action1 != action2 and key1 == key2:
                    self.key_buttons[action1].config(fg="red")
                    self.key_buttons[action2].config(fg="red")

    def save_settings(self):
        """
        Save current key bindings and boss key settings to a JSON file.
        """
        # its own function rather than joined with save_state to make keybinds global to all users and not just one
        with open("settings.json", "w") as file:
            self.key_binds["bosstype"] = self.BossKeyTransparent
            print(self.BossKeyTransparent)
            json.dump(self.key_binds, file)

    def load_settings(self):
        """
        Load previously saved key bindings from a JSON file.
        """
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                self.key_binds = json.load(file)
                self.BossKeyTransparent = self.key_binds.get("bosstype", 0)
                print(self.BossKeyTransparent)
                self.key_binds.pop("bosstype")

    def CloseSettings(self):
        """
        Close the settings menu and restore previous game state.
        """
        self.settings_frame.destroy()
        self.block_b.destroy()
        self.state=self.prev_state
    
    def tipscreen(self):
        """
        Display a temporary tip screen with game instructions/tips.
        """
        self.TipImg = Image.open("Assets\TipScreen.png")
        self.TipImg = ImageTk.PhotoImage(self.TipImg)
        self.tipscreen = Label(self.start_frame, image=self.TipImg)
        self.tipscreen.place(relx=0.5, rely=0.5, anchor=CENTER)  
        self.block_b = Canvas(self.start_frame, width=900, height=60, bg="#ab23ff", bd=0, highlightthickness=0)
        self.block_b.place(x=0, y=540, anchor=NW)
        self.root.after(2500, lambda: (self.tipscreen.destroy(),self.block_b.destroy()))  


    def game(self, event=None):
        """
        Initialize and start the main game, loading necessary assets 
        and setting up game state.
        """
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

        # Load and initialise game scene
        self.gamebg_1 = ImageTk.PhotoImage(self.gamebg_1)
        self.gamebg_2 = ImageTk.PhotoImage(Image.open("Assets\Gamebg_2.png").resize((self.W, self.H)))
        self.gamebg_3 = ImageTk.PhotoImage(Image.open("Assets\Gamebg_3.png").resize((self.W, self.H)))
        self.gamebg_4 = ImageTk.PhotoImage(Image.open("Assets\Gamebg_4.png").resize((self.W, self.H)))  
        self.gamebg = [self.gamebg_1, self.gamebg_2, self.gamebg_3, self.gamebg_4]
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
        self.RelativeScore = 0
        self.scorepwave = 2
        self.spawn_interval = 10000
        self.zombie_num = 0
        self.remaining_time = 0
        self.ScoreTxt = self.cn.create_text(90, 20, text = f"Score: {self.Score}", font=self.GameFont)
        self.FullHealthBarImg = ImageTk.PhotoImage(Image.open(r"Assets\HealthBar\100.png").resize((250, 14)))
        self.HP = self.cn.create_image(400, self.H*0.03, image = self.FullHealthBarImg, anchor=NW)
        self.health = 100
        self.last_hit_time = 0
        self.dx = 0
        self.grav=0.1

        # Detect keys pressed and released for appropriate action
        self.Action = False
        self.Running = False
        self.Jumping = False 
        self.Attacking = False
        self.RunAttacking = False
        self.BossKActive = False
        self.Transparent = False
        self.cheaton = False
        self.mob_cap = False
        
        self.cn.focus_set()
        self.cn.bind("<KeyPress>", self.action)
        [key for key in [self.key_binds["attack"],self.key_binds["right"],self.key_binds["left"]] if self.cn.bind(f"<KeyRelease-{key}>", self.deaction)]
        
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
        """
        Handle player input during gameplay, managing movement, 
        jumping, attacking, and special keys.
        
        Args:
            event: Tkinter key press event
        """
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
        
        elif event.keysym == self.key_binds["attack"]:   
            if self.Jumping or self.Attacking or self.RunAttacking:
                return  # Prevents attacking if the player is jumping or already attacking
            self.Attack()

        elif event.keysym == self.key_binds["bosskey"]:
            self.BossKey()

    def deaction(self, event):
        """
        Reset player action states when keys are released.
        
        Args:
            event: Tkinter key release event
        """
        self.Action = False
        self.Running = False
        self.Attacking = False
        self.RunAttacking = False
        self.reset_sprite()
        pass
    
    def Attack(self):
        """
        Manage player attack mechanics, including attack animations 
        and damage calculation for nearby enemies.
        """
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

    def Jump(self):
        """
        Implement player jumping mechanics with gravity and 
        landing detection.
        """
        if self.state=="loaded":  # to account for the case where a save is loaded where the player is mid air
            self.Jumping=True
            self.state="game"
        if not self.Jumping or self.state != "game":
            return
        self.y_speed += self.grav
        self.cn.move(self.Player_Sprite, 0, self.y_speed)
        self.cn.update()
        if self.cn.coords(self.Player_Sprite)[1] >= self.H * 0.82:
            self.Jumping = False
            self.y_speed = 0
            self.reset_sprite()
        else:
            self.root.after(10, self.Jump)

    def BossKey(self):
        """
        Toggle boss key functionality, providing different 
        screen overlay options when activated.
        """
        if self.BossKActive:
            if self.Transparent==False:
                self.TranspWin.destroy()
            else:
                self.cn.delete(self.TransRec)
                root.overrideredirect(False) # rebirth menu title bar and basically the border
                self.Transparent=False
            self.BossKActive = False
            return
        elif self.BossKeyTransparent:
            self.Transparent=True
            self.TransRec=self.cn.create_rectangle(0, 0, self.W+5, self.H+5, fill="#ab23ff", outline="#ab23ff")
            root.overrideredirect(True)  # remove menu title bar and basically the border
        else:
            self.TranspWin = Toplevel()
            self.TranspWin.attributes("-fullscreen", True)
            self.BossKImg = ImageTk.PhotoImage(Image.open("Assets\BossKeyImg.png").resize((self.TranspWin.winfo_screenwidth(), self.TranspWin.winfo_screenheight())))
            self.BossKLabel = Label(self.TranspWin, image=self.BossKImg)
            self.BossKLabel.pack(fill=BOTH, expand=True)

        self.BossKActive = True

    def animate(self):
        """
        Manage sprite animation frames for player movements 
        and actions across different game states.
        """
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
        """
        Prevent player sprite from moving beyond screen boundaries.
        """
        x = self.cn.coords(self.Player_Sprite)[0]
        if x <= 20 and self.dx < 0:
            self.dx = 0
        elif x >= self.W - 20 and self.dx > 0:
            self.dx = 0

    def check_cheat_code(self, key):
        """
        Check for entered cheat code sequence.
        
        Args:
            key (str): Most recently pressed key
        """
        self.key_sequence.append(key)
        if self.key_sequence[-len(self.konami_sequence):] == self.konami_sequence:
            self.cheat_code()
            self.key_sequence.clear() # or we can do self.key_sequence = [] to clear the list
        elif len(self.key_sequence) > len(self.konami_sequence):
            self.key_sequence.pop(0)

    def cheat_code(self):
        """
        Apply cheat code effects, such as health restoration 
        and gravity modification.
        """
        self.cheaton = True  # a vriable that i may use in the future to imoplement some more complex cheat code functionalities
        if self.grav >=0.05:
            self.grav -= 0.03
        elif self.grav >=0.03:
            self.grav -= 0.01
        if self.health + 30 < 100 and self.health < 100:
            self.health += 30
        elif self.health < 100:
            self.health += 100 - self.health
            self.newhealthimg = ImageTk.PhotoImage(Image.open(f"Assets\HealthBar\{self.health}.png").resize((250, 14)))
            self.cn.itemconfig(self.HP, image = self.newhealthimg)

    def update_score(self):
        """
        Update game score and manage wave progression.
        """
        self.Score += 1
        self.RelativeScore += 1
        self.cn.itemconfig(self.ScoreTxt, text=f"Score: {self.Score}") #self.ScoreTxt.config doesnt work cause its on a canvas and not a standard widget
        if self.RelativeScore % self.scorepwave == 0 and self.Score != 0:
            print(self.Score, self.scorepwave, self.RelativeScore)
            self.WaveNum += 1
            self.scorepwave +=1 
            self.RelativeScore = 0
            self.root.after_cancel(self.spawn_timer)
            self.root.after_cancel(self.mobact_timer)
            self.Pause_button.destroy()
            self.cn.itemconfig(self.GameBG, image=self.WaveBreakImg)
            self.typewriter()
            self.root.after(self.delta*len(self.WaveMsg), self.start_wave)
            
    def start_wave(self):
        """
        Start a new enemy wave after wave break screen.
        """
        self.cn.delete(self.WaveTxt)
        self.Pause_button = Button(self.game_frame, image=self.PauseImg, command=self.pause, bd=0, highlightthickness=0)
        self.cn.create_window(20, 20, window=self.Pause_button)
        self.cn.itemconfig(self.GameBG, image=self.gamebg[(self.WaveNum%4) - 1])
        self.mob_cap = False
        self.spawn_mobs()
        self.action_mobs()

    def typewriter(self):
        """
        Create a typewriter-like text effect for wave announcement.
        """
        self.WaveMsg = f"Wave {self.WaveNum} is approaching...                                           "
        self.WaveTxt = self.cn.create_text(self.W//2, self.H*0.35, text='', font=self.InputFont, fill="black")
        self.delta = 225
        delay = 0
        for i in range(len(self.WaveMsg)+1):
            s = self.WaveMsg[:i]
            updatedtxt = lambda s=s: self.cn.itemconfig(self.WaveTxt, text=s)
            self.cn.after(delay, updatedtxt)
            delay += self.delta


    def reset_sprite(self):
        """
        Reset player sprite to idle state based on last movement direction.
        """
        self.cn.itemconfig(self.Player_Sprite, image=self.IdleR if self.dx>0 else self.IdleL)

    def save_state(self):
        """
        Saves the current game state to a JSON file.
        
        This method captures the current game state, including:
        - Player information (position, health, score, wave number)
        - Zombie information (position, health, state)
        - Removes dead zombies from the list before saving
        
        The state is saved in a JSON file specific to the current player.
        """
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
                "airspeed": self.y_speed if self.Jumping else 0,
                "wave": self.WaveNum,
                "scoreperwave": self.scorepwave,
                "RelativeScore": self.RelativeScore,
                "zombie_num": self.zombie_num,
                "mobcapreached": self.mob_cap
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
        """
        Loads a previously saved game state from a JSON file.
        
        If a saved game state exists for the current player:
        - Restores player position, health, score, and wave number
        - Recreates zombies with their saved positions and states
        
        If no saved state exists:
        - Resets player health to 100
        - Resets score to 0
        - Clears existing zombies
        """
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
            # Load in saved score and wavenumber
            self.Score = player_data["score"]
            self.cn.itemconfig(self.ScoreTxt, text=f"Score: {self.Score}")
            self.WaveNum = player_data["wave"]
            # To account for a save where player is in mid air 
            if player_data["jumping"]:
                self.state="loaded"
                self.y_speed=player_data["airspeed"]
                self.Jump()
            # Load in saved game background if wave number is not 0
            if self.WaveNum != 0:
                self.cn.itemconfig(self.GameBG, image=self.gamebg[(self.WaveNum%4) - 1])
            self.zombie_num = player_data["zombie_num"]
            self.mob_cap = player_data["mobcapreached"]
            self.scorepwave = player_data["scoreperwave"]
            self.RelativeScore = player_data["RelativeScore"]

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
        """
        Displays the game's leaderboard screen.
        """
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
        """
        Close the leaderboard screen and return to the previous game state.
        """
        self.lb_frame.destroy()
        self.state=self.prev_state

    def pause(self):
        """
        Pause the game and display options menu.

        Stops game mechanics, saves current state, unbinds key events, 
        and prepares the game for player interaction in paused mode.
        """
        if self.state == "game":
            self.save_state()
            
            if not self.state == "boss":
                self.cn.unbind("<KeyPress>")
                self.cn.unbind("<KeyRelease>") 

            self.state = "paused"
            self.Pause_button.destroy()
            self.OptionsButton = Button(image = self.OptionsImg, borderwidth=0, highlightthickness=0, background="#ab23ff")
            self.OptionsButton.bind("<Button-1>", self.Optionclicked)
            self.OptionsMenu = self.cn.create_window(self.W // 2, int(self.H * 0.5), window = self.OptionsButton, anchor = CENTER)   
            
            # Pausing mob related stuff calculating remainig time for the next mob spawn
            self.root.after_cancel(self.spawn_timer)
            self.remaining_time = max(0, (self.spawn_interval/1000) - (time.time() - self.elapsed_spawn_time))
            for zombie in self.Zombies:
                zombie.pauseani()
            self.root.after_cancel(self.mobact_timer)         

    def resume(self):
        """
        Resumes the game from a paused state reversing all actions done in the pause method.
        """
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
        """
        Handle user interactions with options menu buttons.

        Processes button clicks in different game states (paused or end), 
        triggering corresponding actions like resuming, restarting, 
        viewing leaderboard, or returning to start menu.

        Args:
            event: Tkinter mouse click event with x and y coordinates
        """
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
        """
        Initiate game over sequence and final screen.

        Performs multiple actions to conclude the game:
        - Saves player's final score to leaderboard
        - Stops zombie movement and animations and set them to idle frames
        - Plays player death animation
        - Displays a randomly selected death message(from terraria)
        - Creates game over menu with restart and quit options
        - Cancels active game timers
        """
        save_score(self.username, self.Score) # for leaderboard
        self.dmsgs = [f"{self.username} was eviscerated.", f"{self.username} was brutally dissected.", f"{self.username} had both kidneys stolen.", f"{self.username}'s body was donated to science.", f"{self.username} received a forced amputation.", f"{self.username} was voluntold to donate blood.", f"{self.username} suffered from a tragic lobotomy.", f"{self.username}'s body was donated to science."]
        for zombie in self.Zombies:
            zombie.changestate("idle")
        self.running_frames = self.dead_right if self.dx>0 else self.dead_left
        self.state="end"
        self.root.after_cancel(self.spawn_timer)
        self.root.after_cancel(self.mobact_timer)
        self.animate() 
        self.Pause_button.destroy()
        self.deathmsg = self.cn.create_text(self.W//2, 230, text = self.dmsgs[random.randint(0, len(self.dmsgs)-1)], font=self.GameFont, anchor=CENTER, fill="#E11919", tags="death_msg")
        
        for i in range(3):
            self.cn.create_rectangle(0, 260, self.W, 200, fill="#000000", outline="", stipple="gray50", tags="bg")  # Stipple pattern for transparency effect of text bg
        self.cn.tag_raise("death_msg", "bg") # to display text on top of transparent bg
        self.OverButton = Button(image = self.GameOverImg, borderwidth=0, highlightthickness=0, background="#ab23ff")
        self.OverButton.bind("<Button-1>", self.Optionclicked)
        self.GameOverMenu = self.cn.create_window(self.W // 2, int(self.H * 0.3), window = self.OverButton, anchor = CENTER)

        

    def spawn_mobs(self):
        """
        Spawn zombies at random intervals and positions.

        Controls zombie spawning based on current wave, zombie cap, 
        and predefined spawn intervals. Adjusts zombie difficulty 
        and game progression.
        """
        if self.mob_cap:
            self.mob_cap = False
            return
        print(self.zombie_num, self.scorepwave, self.mob_cap, 1)
        self.mob_cap = False
        self.elapsed_spawn_time = time.time()
        x = random.choice([random.randint(0,int(0.25*float(self.W))),random.randint(int(0.75*float(self.W)),self.W)])  # gives random coordinate from either first quarter or fourth quarter of the map, may have to adjust for allowing only integers using randint if cannot move sprites to float/decimal pixels
        y = int(self.H * 0.82)
        zombie = NPC(self, self.cn, x, y, self.state, self.Score, self.WaveNum, self.npcwl, self.npcwr, self.npcrl, self.npcrr, self.npcal, self.npcar, self.npcbl, self.npcbr, self.npc1deadr, self.npc1deadl, self.npc2deadr, self.npc2deadl)
        self.Zombies.append(zombie)
        zombie.animate()
        zombie.NextWave()   # modifies the zombie based on the wave number

        self.zombie_num +=1

        # Schedules next spawning mob based on milliseconds in the spawn_interval variable
        self.spawn_timer=self.root.after(self.spawn_interval, self.spawn_mobs)

        if self.zombie_num >= self.scorepwave:
            self.mob_cap = True
            self.zombie_num = 0
            self.root.after_cancel(self.spawn_timer)
            print(self.zombie_num, self.scorepwave, self.mob_cap, 2)
            return


    def take_damage(self):
        """
        Handle player damage mechanics.

        Reduces player health, updates health bar, displays hurt 
        sprite, and triggers game over when health reaches zero. 
        Implements a cooldown between damage events.
        """
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
                self.newhealthimg = ImageTk.PhotoImage(Image.open(f"Assets\HealthBar\{self.health}.png").resize((250, 14)))  # if i dont attribute it to the class tkinter will be garbage collecting
                self.cn.itemconfig(self.HP, image = self.newhealthimg)
                self.last_hit_time = ctime

    def action_mobs(self):
        """
        Manage zombie behavior and movement during gameplay; attack player if in range.

        Continuously updates zombie positions, checks for player 
        collisions, and controls zombie movement and attack states.
        """
        x,y = self.cn.coords(self.Player_Sprite)
        for zombie in self.Zombies:
            if zombie.alive:
                zombie.moveto(x)
                if zombie.collisions(x,y) and self.state!="end":
                    self.take_damage()
                elif self.state=="end":
                    zombie.changestate("idle")
                    return
                else:
                    zombie.changestate("walking_right" if zombie.dx > 0 else "walking_left")
        # Continuosly move towards the player and attack
        self.mobact_timer=self.root.after(50, self.action_mobs)

    def mob_collisions(self, dx):
        """
        Detect and prevent player movement through zombie, providing collision feedback.

        Args:
            dx (float): Horizontal player movement distance

        Returns:
            bool: True if movement is blocked, False if movement is allowed
        """
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
        """
        Remove all widgets from the game window.

        Destroys all child widgets, effectively resetting the 
        game screen for new game initialization or state changes.
        """
        for widget in self.root.winfo_children():
            widget.destroy() 

class NPC(App):
    """
    Initialize a zombie (NPC) with game-specific attributes.

    Sets up zombie's initial state, animations, movement capabilities, 
    and links to the main game application.
    """

    def __init__(self, app, cn, x, y, PlayerState, PlayerScore, WaveNumb, NPCWL, NPCWR, NPCRL, NPCRR, NPCAL, NPCAR, NPCBL, NPCBR, NPC1deadR, NPC1deadL, NPC2deadR, NPC2deadL): #placeholder defaults to prevent errors for now for when mob 2 is to be added to the game
        """
        Initialize a zombie (NPC) with game-specific attributes.

        Sets up zombie's initial state, animations, movement capabilities, 
        and links to the main game application.
        """
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
        """
        Change the zombie's current state and animation frames based on game context.
        """
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
                self.frames = None  
            elif new_state == "dead":
                if self.dx > 0:
                    self.frames = self.dead1_right
                else:   
                    self.frames = self.dead1_left
            self.frame_index = 0 
    
    def NextWave(self):
        """
        Increase zombie difficulty as game progresses.

        Incrementally enhances zombie attributes like health, 
        speed, and spawn mechanics to maintain game challenge.
        """
        if self.Wave != 0:
            if self.Wave == 1:
                self.health = 2
            if self.Wave%3==0:
                self.health += 1
        
        # every round changes
        self.mob_speed += 1
        self.app.spawn_interval -= 500 if self.app.spawn_interval>2000 else 0

    def animate(self):
        """
        Manage zombie sprite animation frames.

        Cycles through animation frames, updates sprite image, and 
        handles special cases like death animation and sprite deletion.
        """
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
        """
        Pause zombie animation during game pause.
        """
        self.cn.after_cancel(self.mobanimate)
        self.Animating = False

    def resumeani(self):
        """
        Resume zombie animation after game is unpaused.
        """
        self.Animating = True
        self.animate()
            
    def moveto(self, playerx):
        """
        Move zombie towards player's position.

        Controls zombie movement direction and speed, updating 
        state and position relative to player's location.
        """
        if self.state.startswith("attacking"):
            return
        x = self.cn.coords(self.zombie_sprite)[0]
        self.dx = playerx - x
        if abs(self.dx) > 10: # Minimum distance from player to change direction to avoid endless switching if player close
            direction = "walking_right" if self.dx > 0 else "walking_left"  
            self.changestate(direction)
            step = min(self.mob_speed, self.dx) if self.dx>0 else max(-self.mob_speed, self.dx)
            self.cn.move(self.zombie_sprite, step, 0)

    def collisions(self, playerx, playery, attack_range = 30):
        """
        Determine if zombie is in range to attack player and attack if within the range.

        Args:
            playerx (int): Player's x-coordinate
            playery (int): Player's y-coordinate
            attack_range (int, optional): Maximum distance for attack. Defaults to 30.

        Returns:
            bool: True if zombie can attack, False otherwise
        """
        x, y = self.cn.coords(self.zombie_sprite)
        if abs(playerx - x) < attack_range and abs(playery - y) < attack_range - 10:
            if not self.state.startswith("attacking"):
                self.changestate(f"attacking_{'right' if self.dx>0 else 'left'}")
            return True
        else:
            return False
        
    def take_damage(self, damage):
        """
        Process damage inflicted on the zombie.

        Reduces zombie health, triggers death sequence and animation if no HP left, and updates game score accordingly.
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.app.update_score()
            self.changestate("dead")
            


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
