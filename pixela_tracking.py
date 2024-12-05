import os
import tkinter as tk
from tkinter import messagebox, ttk

import requests as req
from cairosvg import svg2png
from dotenv import load_dotenv

load_dotenv()


BACKGROUND_COLOR = "#D5E8D4"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"

USERNAME = os.getenv("USERNAME")
# print(USERNAME)
TOKEN = os.getenv("TOKEN")
# print(TOKEN)


class Tracking:
    def __init__(
        self, dates: list, all_surah: dict, current_surah, current_verse
    ) -> None:
        self.before = ""

        self.all_surah = all_surah
        self.surahs_list = [key for key in self.all_surah]
        self.current_surah = current_surah
        self.current_verse = current_verse

        global history_img
        self.date_list = dates

        self.main_win = tk.Tk()
        self.main_win.title("The Quran Tracker")
        self.main_win.config(padx=20, pady=20, background=BACKGROUND_COLOR)

        # self.canvas = tk.Canvas(width=300, height=300)
        # self.canvas.grid(column=0, row=0)

        self.title = tk.Label(text="The Quran Tracker", background=BACKGROUND_COLOR)
        self.title.grid(
            column=1,
            row=0,
        )

        self.sign_out = tk.Button(
            text="Sign Out",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
        )
        self.sign_out.grid(column=2, row=0, padx=30, sticky="e")

        history_img = tk.PhotoImage(file="history.png")
        # self.canvas.create_image(20,20, image=history_img)
        self.img = tk.Label(image=history_img, background=BACKGROUND_COLOR)
        self.img.grid(column=0, row=1, padx=20, pady=20, columnspan=5)

        self.page_text = tk.Label(text="Page:", background=BACKGROUND_COLOR)
        self.page_text.grid(column=0, row=2)
        self.page_spinbox = tk.Spinbox(from_=1, to=100, width=3)
        self.page_spinbox.grid(column=1, row=2)

        self.to_date = tk.Label(text="Update Date:", background=BACKGROUND_COLOR)
        self.to_date.grid(column=0, row=3)
        self.date = ttk.Combobox(values=self.date_list, width=9)
        self.date.grid(column=1, row=3)

        self.submit_btn = tk.Button(
            text="Submit",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.submit_pressed,
        )
        self.submit_btn.grid(column=0, row=4, columnspan=2)

        self.today_read = tk.Label(text=f"Today, 1 Page", background=BACKGROUND_COLOR)
        self.total_read = tk.Label(text="Total: 9 Page", background=BACKGROUND_COLOR)
        self.max_read = tk.Label(text="Max: 4 Page", background=BACKGROUND_COLOR)
        self.min_read = tk.Label(text="Min: 1 Page", background=BACKGROUND_COLOR)
        self.avg_read = tk.Label(text="Avg: 3 Page", background=BACKGROUND_COLOR)
        self.total_days = tk.Label(text="Total Days: 3", background=BACKGROUND_COLOR)

        self.today_read.grid(column=2, row=2)
        self.total_read.grid(column=2, row=3)
        self.max_read.grid(column=2, row=4)
        self.min_read.grid(column=2, row=5)
        self.avg_read.grid(column=2, row=6)
        self.total_days.grid(column=2, row=7)

        self.currently_on_surah_text = tk.Label(
            text="Currently On Surah:", background=BACKGROUND_COLOR
        )
        self.currently_on_surah_cb = ttk.Combobox(values=self.surahs_list, width=12)
        self.currently_on_surah_cb.set(current_surah)
        self.currently_on_surah_cb.bind("<<ComboboxSelected>>", self.refresh_verse)
        self.currently_on_surah_text.grid(column=3, row=2)
        self.currently_on_surah_cb.grid(column=4, row=2)


        self.var = tk.StringVar()
        self.currently_on_verse_text = tk.Label(
            text="On Verse:", background=BACKGROUND_COLOR
        )
        self.currently_on_verse_spinbox = tk.Spinbox( textvariable=self.var,
            from_=1, to=self.all_surah[self.currently_on_surah_cb.get()], width=3
        )
        self.var.set(current_verse)
        self.currently_on_verse_text.grid(column=3, row=3)
        self.currently_on_verse_spinbox.grid(column=4, row=3)
        # self.refresh_verse()
        self.submit_btn = tk.Button(
            text="Update",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.update_pressed,
        )
        self.submit_btn.grid(column=3, row=4, columnspan=2)

        self.main_win.mainloop()

    def refresh_verse(self, event):
        print(f"inside refresh verse:{self.before},{self.currently_on_surah_cb.get()}")
        if self.before != self.currently_on_surah_cb.get():
            print(
                f"inside refresh verse ififif:{self.before},{self.currently_on_surah_cb.get()}"
            )
            self.before = self.currently_on_surah_cb.get()
            self.currently_on_verse_spinbox.config(
                to=self.all_surah[self.currently_on_surah_cb.get()]
            )

    def update_pressed(self):
        surah = self.currently_on_surah_cb.get()
        verse = self.currently_on_verse_spinbox.get()
        print(f"surah:{surah}  verse:{verse}")

        with open("data/current.csv", mode="w") as file:
            file.write(f"{surah},{verse}")

    def submit_pressed(self):
        page = self.page_spinbox.get()
        date = self.date.get().replace("-", "")

        header = {"X-USER-TOKEN": TOKEN}

        body = {"quantity": page}
        print(body)

        # print(f"{date}")

        update_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/graph1/{date}"

        update_res = req.put(url=update_endpoint, headers=header, json=body)
        try:
            update_res.raise_for_status()  # TODO Handle 503 Server Error
        except req.exceptions.HTTPError:
            pass

        # print(update_res.json()["isSuccess"])
        # print(str(update_res.json()["isSuccess"]) == "False")

        while str(update_res.json()["isSuccess"]) == "False":
            update_res = req.put(url=update_endpoint, headers=header, json=body)
            print(f"I am here{update_res.json()['isSuccess']}")

        print(f"I am here{update_res.json()}")

        update_history()
        self.refresh_img()

    def refresh_img(self):
        global history_img
        history_img = tk.PhotoImage(file="history.png")
        self.img.config(image=history_img, background=BACKGROUND_COLOR)


def update_history():
    # print("HERE!")
    svg_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/graph1"  # TODO This needs changing before finishing up.

    parameters = {"mode": "short"}

    res = req.get(url=svg_endpoint)
    # print(res.url)
    svg_code = res.text
    svg2png(bytestring=svg_code, write_to="history.png")
