# # import webbrowser

# # webbrowser.open("https://pixe.la/@raf")

# # from selenium import webdriver
# # browser = webdriver.Firefox()
# # browser.get("https://pixe.la/@raf")

# import os
# import tkinter as tk
# from tkinter import messagebox
# from cairosvg import svg2png
# import requests as req
# from dotenv import load_dotenv

# load_dotenv()

# BACKGROUND_COLOR = "#D5E8D4"
# PIXELA_ENDPOINT = "https://pixe.la/v1/users"

# USERNAME = os.getenv("USERNAME")
# print(USERNAME)
# TOKEN = os.getenv("TOKEN")
# print(TOKEN)

# svg_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/graph1"

# parameters = {"mode": "short"}

# res = req.get(url=svg_endpoint)

# print(res.text)
# svg_code = res.text
# # for line in res.iter_lines():
# #     print(line)
# svg2png(bytestring=svg_code, write_to="history.png")

import pandas as pd

all_surahs = (
        pd.read_csv("data/All_Surahs.csv").set_index("Surahs")["Ayahs"]
    )

print(all_surahs)