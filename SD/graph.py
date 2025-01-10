import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from decimal import Decimal
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Toplevel

def create_plot():
    # Database connection
    conn = psycopg2.connect(
        host='20.16.230.195',
        port='5432',
        dbname='SteamBox',
        user='postgres',
        password='IDEA'
    )
    cur = conn.cursor()
    cur.execute("SELECT game_id, name, playtime_hours, genres, price FROM steam_games")
    rows = cur.fetchall()
    conn.close()

    # Creating DataFrame from rows fetched from database
    df = pd.DataFrame(rows, columns=['game_id', 'name', 'playtime_hours', 'genres', 'price'])

    # Data cleaning: convert decimal to float
    df['price'] = df['price'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['playtime_hours'] = df['playtime_hours'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

    # Filter data (remove zero values)
    df = df[(df['price'] > 0) & (df['playtime_hours'] > 0)]

    # Prepare data for linear regression
    X = df[['playtime_hours']]  # Independent variable: playtime
    y = df['price']  # Dependent variable: price

    # Create a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the prices using the model
    y_pred = model.predict(X)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase size for better visibility

    # Scatter plot for actual data points
    ax.scatter(df['playtime_hours'], df['price'], color='blue', alpha=0.5)

    # Plot the regression line
    ax.plot(df['playtime_hours'], y_pred, color='red', linewidth=2, label='Prediction Line')

    # Set title and labels
    ax.set_title('Price vs Playtime with Prediction Line')
    ax.set_xlabel('Playtime (hours)')
    ax.set_ylabel('Price (€)')
    ax.grid(True)

    # Set Y-axis limits to ignore outlier values
    ax.set_ylim(0, 120)
    ax.set_yticks(np.arange(0, 121, 5))

    # Display the legend
    ax.legend()

    # Return the figure object
    return fig

# Function to open the graph in a separate window when a button is clicked
def open_graph_window():
    # Create a new Toplevel window
    graph_window = Toplevel()
    graph_window.title("Price vs Playtime Graph")
    graph_window.geometry("800x600")

    # Create the plot
    fig = create_plot()

    # Embed the plot in the new window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a button to close the window
    close_button = tk.Button(graph_window, text="Close", command=graph_window.destroy)
    close_button.pack(pady=10)

