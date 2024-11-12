from tkinter import *
from tkinter.font import Font

root = Tk()
root.title("Hello There")
root.geometry("500x500")

GameFont = Font(
    family="CyberpunkCraftpixPixel",  # Corrected font family name
    size=42,
    underline=0,
    overstrike=1
)

mylab = Label(root, text="Is this working?", font=GameFont)
mylab.pack()

#available_fonts = font.families()
#print("Available Fonts:")
#for f in available_fonts:
#    print(f)

root.mainloop()
