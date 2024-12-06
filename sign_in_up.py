import tkinter as tk
import webbrowser
from tkinter import messagebox

import requests as req
from selenium import webdriver

BACKGROUND_COLOR = "#D5E8D4"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"


class SignInUp:
    def __init__(self) -> None:
        self.signed_in = False
        self.sign_win = tk.Tk()
        self.sign_win.title("Sign In/Up")
        self.sign_win.config(padx=20, pady=20, background=BACKGROUND_COLOR)

        self.username = tk.Label(text="Username:", background=BACKGROUND_COLOR)
        self.username_entry = tk.Entry(width=40)
        self.username.grid(column=0, row=0)
        self.username_entry.grid(column=1, row=0, columnspan=3)

        self.password = tk.Label(text="Password/Token:", background=BACKGROUND_COLOR)
        self.password_entry = tk.Entry(width=40)
        self.password.grid(column=0, row=1)
        self.password_entry.grid(column=1, row=1, columnspan=3)

        self.sign_in = tk.Button(
            text="Sign In",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.sign_in_method,
        )
        self.sign_up = tk.Button(
            text="Sign Up",
            background=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.sign_up_method,
        )
        self.sign_in.grid(column=1, row=2, pady=10, columnspan=1, sticky="")
        self.sign_up.grid(column=2, row=2, pady=10, columnspan=1, sticky="")

        self.warning = tk.Label(
            text="Remember or write down your password/token somewhere. There is no way to recover it if forgotten.\n\nWhen signing up for a new account, you are agreeing to the TOS of pixela and that you are not a minor.",
            background=BACKGROUND_COLOR,
            wraplength=460,
        )
        self.warning.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

        self.sign_win.mainloop()

    def sign_in_method(self):
        username = self.username_entry.get()
        # print(username)
        password = self.password_entry.get()
        # print(password)

        if len(username) == 0 or len(password) == 0:
            messagebox.showinfo(
                title="Empty Fields", message="Do not leave any empty fields."
            )
            return

        graph_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs"
        graph_config = {
            "id": "qurantracker",
            "name": "Reading Quran",
            "unit": "Page",
            "type": "int",
            "color": "sora",
        }
        token_header = {"X-USER-TOKEN": password}
        graph_res = req.post(
            url=graph_endpoint, json=graph_config, headers=token_header
        )
        # graph_res.raise_for_status()
        # print(graph_res.json())

        res_message = graph_res.json()["message"]
        # print(res_message)

        # print(res_message == "Success." or res_message == "This graphID already exist.")
        if res_message == "Success." or res_message == "This graphID already exist.":
            # print("inside success")
            with open(".env", mode="w") as env_file:
                env_file.writelines([f"USERNAME={username}", "\n", f"TOKEN={password}"])

            self.sign_win.quit()
            self.sign_win.destroy()
            self.signed_in = True
        else:
            # if res_message == f"User `{username}` does not exist or the token is wrong.":
            # print(f"User `{username}` does not exist or the token is wrong.")
            messagebox.showerror(
                title="Wrong Username or Password.",
                message=f"{res_message} If you have forgotten either of them then consider signing up for a new account with a new username and a new password/token.",
            )
            return

    def sign_up_method(self):
        username = self.username_entry.get()
        # print(username)
        password = self.password_entry.get()
        # print(password)

        if len(username) == 0 or len(password) == 0:
            messagebox.showinfo(
                title="Empty Fields", message="Do not leave any empty fields."
            )
            return
        pass

        user_data = {
            "token": password,
            "username": username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }

        new_user_res = req.post(url=PIXELA_ENDPOINT, json=user_data)
        # print(new_user_res.json())

        res_message = new_user_res.json()["message"]

        if (
            res_message
            == f"Success. Let's visit https://pixe.la/@{username} , it is your profile page!"
        ):
            # print("inside success")

            open_web = messagebox.askyesno(title="Success!", message=res_message)
            if open_web:
                try:
                    webbrowser.open(f"https://pixe.la/@{username}")
                except:
                    browser = webdriver.Firefox()
                    browser.get(f"https://pixe.la/@{username}")

        else:
            messagebox.showerror(title="Error!", message=res_message)
