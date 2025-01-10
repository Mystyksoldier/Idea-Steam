import customtkinter as ctk
from functions import *
from database import *
from graph import *
import json

session = Session()

username = load_session_data()

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

user_label = ctk.CTkLabel(navbar, text=username, font=("Minecraftia", 16), width=120, height=30, fg_color="white", text_color="black")
user_label.place(x=730, y=15)

exit_button = ctk.CTkButton(navbar, text="Exit", width=40, height=30, fg_color="red", text_color="white", corner_radius=10, command=exit)
exit_button.place(x=860, y=15)

# Friends Online Section
friends_frame = ctk.CTkFrame(app, width=300, height=500, fg_color="#3A2352")
friends_frame.place(x=20, y=100)

friends_label = ctk.CTkLabel(friends_frame, text="Friends online:", font=("Minecraftia", 16), text_color="white")
friends_label.pack(pady=10)

for friend in onlineFriends()[:5]:  # Only show the first 5 friends
    friend_id = friend[0]  # First element: friend_id
    friend_name = friend[1]  # Second element: friend_name
    friend_status = friend[2]  # Third element: friend_status
    current_game = friend[3]  # Fourth element: current_game
    
    # You can now use these values, for example, to create buttons:
    friend_button = ctk.CTkButton(
        friends_frame,
        text=f"{friend_name}\n{friend_status}",
        width=200,
        height=50,
        corner_radius=32,
        fg_color="white",
        text_color="black",
        hover_color="#DDD",
    )

    friend_button.pack(pady=5, padx=5, anchor="center")

# Container Frame for Other Sections
sections_container = ctk.CTkFrame(app, width=900, height=500, fg_color="transparent") 
sections_container.place(x=300, y=100)

# Size for all blocks
block_width = 250
block_height = 200
SPACING = 10

# Most Played Section
most_played_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="white")
most_played_frame.place(x=0, y=0)

most_played_label = ctk.CTkLabel(most_played_frame, text="Most Played Games:", font=("Minecraftia", 18), text_color="black")
most_played_label.place(relx=0.5, y=15, anchor="n")  # Better spacing from the top

top_games = top3games()

# Display the top 3 games
for idx, game in enumerate(top_games):
    label = ctk.CTkLabel(most_played_frame, text=game, font=("Minecraftia", 14), text_color="black")
    label.place(x=10, y=50 + (idx * 30))

# Recently Played Section
recently_played_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="white")
recently_played_frame.place(x=block_width + SPACING, y=0)

recently_played_label = ctk.CTkLabel(recently_played_frame, text="Price vs Playtime", font=("Minecraftia", 16), text_color="black")
recently_played_label.place(relx=0.5, y=10, anchor="n")

# Button to open the graph
graph_button = ctk.CTkButton(recently_played_frame, text="Show Graph", command=open_graph_window)
graph_button.place(relx=0.5, rely=0.6, anchor="center")

# Steambox Section
steambox_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="white")
steambox_frame.place(x=0, y=block_height + SPACING)

steambox_label = ctk.CTkLabel(steambox_frame, text="Steam Box:", font=("Minecraftia", 16), text_color="black")
steambox_label.place(relx=0.5, y=10, anchor="n")

steambox_onButton = ctk.CTkButton(steambox_frame, text="ON", width=100, height=50, fg_color="green", text_color="black", corner_radius=32, command=lambda: picoOnOrOff("on"))
steambox_onButton.place(relx=0.28, rely=0.5, anchor="center")

steambox_offButton = ctk.CTkButton(steambox_frame, text="OFF", width=100, height=50, fg_color="red", text_color="black", corner_radius=32, command=lambda: picoOnOrOff("off"))
steambox_offButton.place(relx=0.72, rely=0.5, anchor="center")

# Empty Section 2
empty_section2 = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="white")
empty_section2.place(x=block_width + SPACING, y=block_height + SPACING)

# Label to display calculate_statistics() output
statistics_label = ctk.CTkLabel(empty_section2, text=calculate_statistics(), font=("Minecraftia", 14), text_color="black")
statistics_label.place(relx=0.5, rely=0.5, anchor="center")

# Start the Tkinter event loop
app.mainloop()
