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
app.configure(fg_color="#2a475e")

# Navbar at the top
navbar = ctk.CTkFrame(app, width=900, height=60, fg_color="#1b2838")
navbar.place(x=0, y=0)

navbar_title = ctk.CTkLabel(navbar, text="IDEA STEAM", font=("Minecraftia", 24), text_color="#c7d5e0")
navbar_title.place(x=20, y=15)

user_label = ctk.CTkLabel(navbar, text=username, font=("Minecraftia", 16), width=120, height=30, fg_color="#c7d5e0", text_color="black")
user_label.place(x=730, y=15)

exit_button = ctk.CTkButton(navbar, text="Exit", width=40, height=30, fg_color="red", text_color="#c7d5e0", corner_radius=10, command=exit)
exit_button.place(x=860, y=15)

# Friends Online Section
friends_frame = ctk.CTkFrame(app, width=300, height=500, fg_color="#1b2838")
friends_frame.place(x=20, y=100)

friends_label = ctk.CTkLabel(friends_frame, text="Friends online:", font=("Minecraftia", 16), text_color="#c7d5e0")
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
        fg_color="#c7d5e0",
        text_color="black",
        hover_color="#DDD",
    )

    friend_button.pack(pady=5, padx=5, anchor="center")

# Common font settings
font_style = ("Minecraftia", 16)
title_font_style = ("Minecraftia", 18)
corner_radius = 15

# Container Frame for all Sections
sections_container = ctk.CTkFrame(app, width=900, height=500, fg_color="transparent", corner_radius=corner_radius) 
sections_container.place(x=300, y=100)

# Size for all blocks
block_width = 250
block_height = 200
SPACING = 10

# Most Played Section
most_played_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="#c7d5e0", corner_radius=corner_radius)
most_played_frame.place(x=0, y=0)

most_played_label = ctk.CTkLabel(most_played_frame, text="Most Played Games:", font=title_font_style, text_color="black", bg_color="#c7d5e0")
most_played_label.place(relx=0.5, y=15, anchor="n")  # Better spacing from the top

top_games = top3games()

# Display the top 3 games
for idx, game in enumerate(top_games):
    label = ctk.CTkLabel(most_played_frame, text=game, font=font_style, text_color="black", bg_color="#c7d5e0")
    label.place(x=10, y=50 + (idx * 30))

# Graph Section
recently_played_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="#c7d5e0", corner_radius=corner_radius)
recently_played_frame.place(x=block_width + SPACING, y=0)

recently_played_label = ctk.CTkLabel(recently_played_frame, text="Price vs Playtime", font=title_font_style, text_color="black", bg_color="#c7d5e0")
recently_played_label.place(relx=0.5, y=10, anchor="n")

# Button to open the graph
graph_button = ctk.CTkButton(recently_played_frame, text="Show Graph", command=open_graph_window)
graph_button.place(relx=0.5, rely=0.6, anchor="center")

# Steambox Section
steambox_frame = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="#c7d5e0", corner_radius=corner_radius)
steambox_frame.place(x=0, y=block_height + SPACING)

steambox_label = ctk.CTkLabel(steambox_frame, text="Steam Box:", font=title_font_style, text_color="black", bg_color="#c7d5e0")
steambox_label.place(relx=0.5, y=10, anchor="n")

steambox_onButton = ctk.CTkButton(steambox_frame, text="ON", width=100, height=50, fg_color="green", text_color="black", corner_radius=32, command=lambda: picoOnOrOff("on"))
steambox_onButton.place(relx=0.28, rely=0.5, anchor="center")

steambox_offButton = ctk.CTkButton(steambox_frame, text="OFF", width=100, height=50, fg_color="red", text_color="black", corner_radius=32, command=lambda: picoOnOrOff("off"))
steambox_offButton.place(relx=0.72, rely=0.5, anchor="center")

# Statistics Section 
statistics_section2 = ctk.CTkFrame(sections_container, width=block_width, height=block_height, fg_color="#c7d5e0", corner_radius=corner_radius)
statistics_section2.place(x=block_width + SPACING, y=block_height + SPACING)

# Calculate statistics
mean, median = calculate_statistics()

# Format the output to display as text
statistics_text = f"Mean = {mean}\nMedian = {median}"

# Label for "Game Hours Statistics"
title_label = ctk.CTkLabel(statistics_section2, text="Game Hours Statistics:", font=title_font_style, text_color="#333333", bg_color="#c7d5e0")
title_label.place(relx=0.5, rely=0.2, anchor="center")

# Label to display the statistics output
statistics_label = ctk.CTkLabel(statistics_section2, text=statistics_text, font=font_style, text_color="#333333", bg_color="#c7d5e0", corner_radius=corner_radius, padx=20, pady=10)
statistics_label.place(relx=0.5, rely=0.6, anchor="center")


# Start the Tkinter event loop
app.mainloop()
