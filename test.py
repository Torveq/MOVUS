from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("MOVUS") 

#Everything to do with the starting frame as soon as you run the app
def StartMenu():
    StartFrame.pack(fill="both", expand = True)
    SImg = Label(StartFrame, image = StartImg)
    SImg.pack()
    ButtonImg=ImageTk.PhotoImage(Image.open("Assets\Playbutton.png"))
    StartButton = Button(StartFrame, image=ButtonImg, command=Game)
    StartButton.pack()

#Everything to do with the game itself after user hits play button
def Game():
    pass

#Making Starting Frame
StartImg = Image.open("Assets\MainMenue.png")
Width, Height = StartImg.size
StartImg = ImageTk.PhotoImage(StartImg)
StartFrame = LabelFrame(root, bd=0, width=Width, height=Height)


root.mainloop()
if __name__ == "__main_":
    root = Tk()
    root.title("MOVUS")

    StartMenu()


    root.mainloop()