import customtkinter as ctk
from functions import *
from tkinter import messagebox
import sys
import os

# Sample user data for login validation
USER_DATA = {
    "admin": "123",  # username: password
    "user1": "mypassword",
    "user2": "pass2023"
}

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USER_DATA and USER_DATA[username] == password:
        sys.exit(1)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Initialize the main window
app = ctk.CTk()
app.geometry("450x300")
app.title("IDEA STEAM")
app.configure(bg="#472D5B", fg_color="#5b2d54")

# Title Label
title_label = ctk.CTkLabel(app, text="Login", font=("Minecraftia", 24), text_color="white")
title_label.pack(pady=20)

# Username Label and Entry
username_label = ctk.CTkLabel(app, text="Username:", font=("Minecraftia", 16), text_color="white")
username_label.pack(pady=5)

username_entry = ctk.CTkEntry(app, width=250, height=30)
username_entry.pack(pady=5)

# Password Label and Entry
password_label = ctk.CTkLabel(app, text="Password:", font=("Minecraftia", 16), text_color="white")
password_label.pack(pady=5)

password_entry = ctk.CTkEntry(app, show="*", width=250, height=30)
password_entry.pack(pady=5)

# Login Button
login_button = ctk.CTkButton(app, text="Login", width=100, height=40, corner_radius=10, command=validate_login)
login_button.pack(pady=20)

app.mainloop()
