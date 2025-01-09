import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from decimal import Decimal
from sklearn.linear_model import LinearRegression
import numpy as np

# Verbinding maken met de database
conn = psycopg2.connect(
    host='20.16.230.195',
    port='5432',
    dbname='SteamBox',
    user='postgres',
    password='IDEA'
)

# Maak een cursor object
cur = conn.cursor()

# Haal de gegevens op uit de database
cur.execute("SELECT game_id, name, playtime_hours, genres, price FROM steam_games")
rows = cur.fetchall()

# Sluit de verbinding
conn.close()

# Zet de opgehaalde gegevens om in een DataFrame
df = pd.DataFrame(rows, columns=['game_id', 'name', 'playtime_hours', 'genres', 'price'])

# Zet de Decimal-waarden om naar float voor prijs en speeltijd
df['price'] = df['price'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
df['playtime_hours'] = df['playtime_hours'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

# Filter de gegevens om nullen te verwijderen (optioneel)
df = df[(df['price'] > 0) & (df['playtime_hours'] > 0)]

# Maak een lineair regressiemodel
X = df[['playtime_hours']]  # Speeltijd als de onafhankelijke variabele
y = df['price']  # Prijs als de afhankelijke variabele

# Train het model
model = LinearRegression()
model.fit(X, y)

# Voorspel de prijzen
y_pred = model.predict(X)

# Maak een grafiek van de prijs vs speeltijd
plt.figure(figsize=(12, 8))  # Vergroot de grafiek voor beter overzicht
plt.scatter(df['playtime_hours'], df['price'], color='blue', alpha=0.5)  # Scatter plot

# Plot de regressielijn
plt.plot(df['playtime_hours'], y_pred, color='red', linewidth=2, label='Voorspellende lijn')

# Titel en labels
plt.title('Prijs vs Speeltijd van Spellen met Voorspellende Lijn')
plt.xlabel('Speeltijd (uren)')
plt.ylabel('Prijs (€)')
plt.grid(True)

# Verander de limieten van de y-as om de grote waarde van 1600 te negeren
plt.ylim(0, 120)  # Stel de limieten van de y-as in van 0 tot 120

# Verander de stappen van de y-as naar 5
plt.yticks(np.arange(0, 121, 5))  # Stel de ticks in van 0 tot 120 met stappen van 5

# Toon de legende
plt.legend()

# Toon de grafiek
plt.show()
