import os
import tkinter as tk
from tkinter import messagebox

import requests as req
from cairosvg import svg2png
from dotenv import load_dotenv

load_dotenv()


BACKGROUND_COLOR = "#D5E8D4"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"

USERNAME = os.getenv("USERNAME")
print(USERNAME)
TOKEN = os.getenv("TOKEN")
print(TOKEN)


class Tracking:
    def __init__(self) -> None:
        self.main_win = tk.Tk()
        self.main_win.title("The Quran Tracker")
        self.main_win.config(padx=20, pady=20, background=BACKGROUND_COLOR)

        # self.canvas = tk.Canvas(width=300, height=300)
        # self.canvas.grid(column=0, row=0)

        self.title = tk.Label(text="The Quran Tracker", background=BACKGROUND_COLOR)
        self.title.grid(
            column=0,
            row=0,
        )

        self.sign_out = tk.Button(
            text="Sign Out",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
        )
        self.sign_out.grid(column=1, row=0, sticky="")

        history_img = tk.PhotoImage(file="history.png")
        # self.canvas.create_image(20,20, image=history_img)
        self.img = tk.Label(image=history_img, background=BACKGROUND_COLOR)
        self.img.grid(column=0, row=1, padx=20, pady=20, columnspan=2)

        self.main_win.mainloop()


def update_history():
    svg_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/graph1"  # TODO This needs changing before finishing up.

    parameters = {"mode": "short"}

    res = req.get(url=svg_endpoint)
    svg_code = res.text
    svg2png(bytestring=svg_code, write_to="history.png")


update_history()


a = Tracking()
