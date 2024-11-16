from tkinter import *
from PIL import Image, ImageTk

class GifPlayer:
    def __init__(self, root, gif_path):
        self.root = root
        self.gif_path = gif_path
        self.frames = []  # Store all GIF frames
        self.current_frame = 0  # Track the current frame index
        self.load_gif()

        # Label to display the GIF
        self.label = Label(root)
        self.label.pack()

        # Start the GIF animation
        
        self.play_gif()

    def load_gif(self):
        """Load all frames of the GIF into memory."""
        gif = Image.open(self.gif_path)
        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy())
                self.frames.append(frame)
                gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass  # End of GIF frames

    def play_gif(self):
        """Play the GIF by displaying each frame sequentially."""
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])  # Update the label with the current frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Move to the next frame
            #self.delay = 100 if self.current_frame%2==0 else 5000
            self.delay = 50
            self.root.after(self.delay, self.play_gif)  # Adjust delay (ms) as needed for animation speed

# Main setup
if __name__ == "__main__":
    root = Tk()
    root.title("GIF Player")
    gif_player = GifPlayer(root, "Assets\LeaderboardBG.gif")  # Assets\main_bg.gif
    root.mainloop()
