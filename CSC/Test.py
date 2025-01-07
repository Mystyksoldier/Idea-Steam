import psycopg2
import requests

# Configuraties
STEAM_API_KEY = "709D0CFD11FD9A8BC5734194DB742A03"  # Vul je Steam API-sleutel in
STEAM_USERNAME = input("Geef uw gebruikersnaam: ")  # Vul de gebruikersnaam in
POSTGRESQL_CONFIG = {
    'host': '20.16.230.195',
    'port': 5432,
    'database': 'SteamBox',
    'user': 'postgres',
    'password': 'IDEA'
}

def get_steam_id(api_key, username):
    """
    Haalt de Steam ID op met behulp van een gebruikersnaam via de Steam API.
    """
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {
        'key': api_key,
        'vanityurl': username
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Steam API-response: {data}")  # Debug-output
        if data['response']['success'] == 1:
            return data['response']['steamid']
        else:
            raise Exception(f"Geen match voor gebruikersnaam '{username}'. Foutbericht van API: {data['response']['message']}")
    else:
        raise Exception(f"Steam API fout: {response.status_code}, {response.text}")


def fetch_steam_data(user_id, api_key):
    """
    Haalt gebruikersgegevens op via de Steam API.
    """
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': api_key,
        'steamid': user_id,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Steam API fout: {response.status_code}, {response.text}")

def upload_to_postgresql(data, db_config):
    """
    Uploadt data naar een PostgreSQL-database.
    """
    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Controleer of de tabel bestaat, zo niet, maak deze aan
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS steam_games (
                game_id BIGINT PRIMARY KEY,
                name TEXT,
                playtime_forever INTEGER
            )
        ''')

        # Voeg gegevens toe aan de database
        for game in data['response'].get('games', []):
            cursor.execute('''
                INSERT INTO steam_games (game_id, name, playtime_forever)
                VALUES (%s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE
                SET name = EXCLUDED.name, playtime_forever = EXCLUDED.playtime_forever
            ''', (game['appid'], game.get('name', 'Onbekend'), game['playtime_forever']))

        # Bevestig de wijzigingen
        conn.commit()
        print("Gegevens succesvol geüpload naar de database.")

    except Exception as e:
        print(f"Fout bij uploaden: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    try:
        print(f"Steam ID ophalen voor gebruiker: {STEAM_USERNAME}")
        steam_id = get_steam_id(STEAM_API_KEY, STEAM_USERNAME)
        print(f"De Steam ID van {STEAM_USERNAME} is: {steam_id}")

        print("Steam gegevens ophalen...")
        steam_data = fetch_steam_data(steam_id, STEAM_API_KEY)

        print("Data uploaden naar PostgreSQL...")
        upload_to_postgresql(steam_data, POSTGRESQL_CONFIG)

    except Exception as e:
        print(f"Fout opgetreden: {e}")
