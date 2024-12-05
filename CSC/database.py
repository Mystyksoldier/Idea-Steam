import requests
import psycopg2
from datetime import datetime

# Steam API details
steam_api_key = 'YOUR_API_KEY'
steam_id = 'STEAM_ID'  # Vervang met de Steam ID van de gebruiker.

# PostgreSQL connection details
pg_host = "localhost"
pg_database = "your_database"
pg_user = "your_user"
pg_password = "your_password"

# Functie om gegevens van Steam API op te halen
def fetch_steam_data(api_key, steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    response.raise_for_status()  # Geeft een fout als de aanvraag mislukt.
    data = response.json()
    player = data['response']['players'][0]  # Haal de eerste speler op.
    return {
        "steam_id": player["steamid"],
        "player_name": player["personaname"],
        "profile_url": player["profileurl"],
        "avatar": player["avatar"]
    }

# Functie om gegevens in PostgreSQL op te slaan
def save_to_postgresql(data):
    try:
        # Maak verbinding met PostgreSQL
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_database,
            user=pg_user,
            password=pg_password
        )
        cursor = conn.cursor()
        
        # Voer een INSERT of UPDATE uit
        cursor.execute("""
            INSERT INTO SteamPlayerData (steam_id, player_name, profile_url, avatar, last_updated)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (steam_id) DO UPDATE
            SET player_name = EXCLUDED.player_name,
                profile_url = EXCLUDED.profile_url,
                avatar = EXCLUDED.avatar,
                last_updated = EXCLUDED.last_updated;
        """, (data["steam_id"], data["player_name"], data["profile_url"], data["avatar"], datetime.now()))

        # Commit de transactie
        conn.commit()
        print(f"Gegevens opgeslagen voor speler: {data['player_name']}")
    except Exception as e:
        print(f"Fout bij het opslaan in PostgreSQL: {e}")
    finally:
        # Sluit de verbinding
        cursor.close()
        conn.close()

# Haal gegevens op en sla ze op
player_data = fetch_steam_data(steam_api_key, steam_id)
save_to_postgresql(player_data)