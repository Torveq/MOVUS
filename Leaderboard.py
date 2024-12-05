from tkinter import *
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
import os
import random

# File to store leaderboard data
LBtxt = "leaderboard.txt"


def save_score(player_name, score):
    """Save a player's score to the leaderboard file."""
    scores = load_scores()
    # Check if the player already exists
    # and return index of player tuple in scores list
    p_exists_i = next(
        (
            i
            for i, player in enumerate(scores)
            if player[0] == player_name
        ),
        None,
    )
    if p_exists_i is not None:
        # update the existing players score only if > than last entry's
        if score > scores[p_exists_i][1]:
            scores[p_exists_i] = (
                player_name,
                score,
                scores[p_exists_i][2],
            )

    else:
        color = f"#{random.randint(0, 255):02x}"
        color += f"{random.randint(0, 255):02x}"
        color += f"{random.randint(0, 255):02x}"
        scores.append((player_name, score, color))

    scores.sort(key=lambda x: x[1], reverse=True)

    with open(LBtxt, "w") as file:
        for name, score, color in scores:
            file.write(f"{name}:{score}:{color}\n")


def load_scores():
    """Load scores from the leaderboard file and 
    return them as a sorted list."""
    LBtxt = "leaderboard.txt"
    if not os.path.exists(LBtxt):
        return []  # Return an empty list if the file doesn't exist

    scores = []
    with open(LBtxt, "r") as file:
        for line in file:
            try:
                name, score, color = line.strip().split(":")
                scores.append((name, int(score), color))
            except ValueError:
                continue  # Skip invalid lines
    return scores


def display_scores(frame, cn, title_font, elements_font):
    """Load scores and return them as a formatted string."""
    scores = load_scores()
    cn.create_text(
        300,
        73,
        text="LEADERBOARD",
        font=title_font,
        anchor=CENTER,
        fill="#69bbb6",
        tags="title",
    )
    cn.create_rectangle(
        210,
        82,
        390,
        84,
        fill="#5eada8",
        outline="#5eada8",
        tags="underline",
    )
    cn.tag_raise("title", "underline")
    for i in range(min(8, len(scores))):
        # Coordinates for the circle
        x1, y1 = 220, 100 + i * 20  # Adjust y-position for each row
        x2, y2 = x1 + 10, y1 + 10  # Circle size
        # Draw the circle
        cn.create_oval(
            x1,
            y1,
            x2,
            y2,
            fill=scores[i][2],
            outline="black",
            tags=f"circle_{i}",
        )

        # Add the rank in one color
        if i + 1 == 1:
            rankcode = "gold"
        elif i + 1 == 2:
            rankcode = "silver"
        elif i + 1 == 3:
            rankcode = "#CE8946"
        else:
            rankcode = "gray"
        cn.create_text(
            x2 + 10,
            y1 + 5,
            text=f"#{i + 1}",
            font=elements_font,
            anchor=W,
            fill=rankcode,
            tags=f"rank_{i}",
        )

        # Add the name in another color
        cn.create_text(
            x2 + 40,
            y1 + 5,
            text=scores[i][0],
            font=elements_font,
            anchor=W,
            fill="teal",
            tags=f"name_{i}",
        )

        # Add the score in a third color
        cn.create_text(
            x2 + 130,
            y1 + 5,
            text=scores[i][1],
            font=elements_font,
            anchor=W,
            fill="#9FAC8A",
            tags=f"score_{i}",
        )


def display_leaderboard(cn):
    """Display leaderboard."""
    LB_IMG = ImageTk.PhotoImage(Image.open("Assets\LBImg.png"))
    LB_IMGs = cn.create_image(
        300, 155, image=LB_IMG, anchor=CENTER, tags="lb_img"
    )
    cn.img_ref = LB_IMG  # to avoid garbage collection
    cn.tag_raise("lb_img")