import customtkinter as ctk
from tkinter import messagebox
from session import Session
from functions import *
import subprocess
import json

session = Session()

def validate_login():
    username = username_entry.get()

    session.login(username)

    with open('session_data.json', 'w') as f:
        json.dump({'username': username}, f)

    getData()

    app.destroy()
    subprocess.run(["python", "SD/Gui.py"])

app = ctk.CTk()
app.geometry("450x300")
app.title("IDEA STEAM")
app.configure(bg="#2a475e", fg_color="#2a475e")

# Title Label
title_label = ctk.CTkLabel(app, text="Login", font=("Minecraftia", 24), text_color="white")
title_label.pack(pady=20)

# Username Label and Entry
username_label = ctk.CTkLabel(app, text="Username:", font=("Minecraftia", 16), text_color="white")
username_label.pack(pady=5)

username_entry = ctk.CTkEntry(app, width=250, height=30)
username_entry.pack(pady=5)

# Login Button
login_button = ctk.CTkButton(app, text="Login", width=100, height=40, corner_radius=10, command=validate_login)
login_button.pack(pady=20)

app.mainloop()
