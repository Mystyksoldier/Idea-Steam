import customtkinter as ctk
from userdata import users

# Initialize the main window
app = ctk.CTk()
app.geometry("900x600")
app.title("IDEA STEAM")
app.configure(bg="#472D5B")
app.configure(fg_color="#5b2d54")

# Navbar at the top
navbar = ctk.CTkFrame(app, width=900, height=60, fg_color="#3A2352")
navbar.place(x=0, y=0)

navbar_title = ctk.CTkLabel(navbar, text="IDEA STEAM", font=("Minecraftia", 24), text_color="white")
navbar_title.place(x=20, y=15)

user_label = ctk.CTkLabel(navbar, text="User36", font=("Minecraftia", 16), width=120, height=30, fg_color="white", text_color="black")
user_label.place(x=730, y=15)

menu_button = ctk.CTkButton(navbar, text="☰", width=40, height=30, fg_color="white", text_color="black", corner_radius=5, hover_color="#ccc")
menu_button.place(x=860, y=15)

# Standard frame dimensions
FRAME_WIDTH = 250
FRAME_HEIGHT = 200

# Friends Online Section
friends_frame = ctk.CTkFrame(app, width=FRAME_WIDTH, height=500, fg_color="#3A2352")
friends_frame.place(x=20, y=80)

friends_label = ctk.CTkLabel(friends_frame, text="Friends online:", font=("Minecraftia", 16), text_color="white")
friends_label.pack(pady=10)

def onlineFriends():
    return [user for user in  users if user["status"] == "online"]

for friend in onlineFriends()[:5]:
    friend_button = ctk.CTkButton(
        friends_frame,
        text=f"{friend['username']}\n{friend['game']}",
        width=200,
        height=50,
        corner_radius=32,
        fg_color="white",
        text_color="black",
        hover_color="#DDD"
    )
    friend_button.pack(pady=5)

# Most Played Section
most_played_frame = ctk.CTkFrame(app, width=FRAME_WIDTH, height=FRAME_HEIGHT, fg_color="white")
most_played_frame.place(x=300, y=80)

most_played_label = ctk.CTkLabel(most_played_frame, text="Most Played:", font=("Minecraftia", 16), text_color="black")
most_played_label.pack(anchor="w", pady=10, padx=10)

most_played_list = ctk.CTkLabel(most_played_frame, text="1. War Thunder\n2. GTA 5\n3. Pokemon", font=("Minecraftia", 14), text_color="black")
most_played_list.pack(anchor="w", padx=10)

# Recently Played Section
recently_played_frame = ctk.CTkFrame(app, width=FRAME_WIDTH, height=FRAME_HEIGHT, fg_color="white")
recently_played_frame.place(x=600, y=80)

recently_played_label = ctk.CTkLabel(recently_played_frame, text="Recently Played:", font=("Minecraftia", 16), text_color="black")
recently_played_label.pack(anchor="w", pady=10, padx=10)

recently_played_list = ctk.CTkLabel(recently_played_frame, text="• Doctor Simulator\n• Market Insights", font=("Minecraftia", 14), text_color="black")
recently_played_list.pack(anchor="w", padx=10)

# Additional Empty Frames
empty_section1 = ctk.CTkFrame(app, width=FRAME_WIDTH, height=FRAME_HEIGHT, fg_color="white")
empty_section1.place(x=300, y=300)

empty_section2 = ctk.CTkFrame(app, width=FRAME_WIDTH, height=FRAME_HEIGHT, fg_color="white")
empty_section2.place(x=600, y=300)

# Run the app
app.mainloop()
