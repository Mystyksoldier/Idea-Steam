import psycopg2
import requests

# Configuraties
STEAM_API_KEY = "709D0CFD11FD9A8BC5734194DB742A03"
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
        if data['response']['success'] == 1:
            return data['response']['steamid']
        else:
            raise Exception(
                f"Geen match voor gebruikersnaam '{username}'. Foutbericht van API: {data['response']['message']}")
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
        'include_appinfo': True,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Steam API fout: {response.status_code}, {response.text}")


def fetch_game_details(app_id):
    """
    Haalt extra details op voor een game zoals genres en prijs.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]['success']:
            game_data = data[str(app_id)]['data']
            genres = ', '.join([genre['description'] for genre in game_data.get('genres', [])])
            price = game_data.get('price_overview', {}).get('final', 0) / 100  # Prijs in euro's
            return genres, price
        else:
            return None, None
    else:
        raise Exception(f"Steam Store API fout: {response.status_code}, {response.text}")


def table_exists(cursor, table_name):
    """
    Controleert of een tabel bestaat in de database.
    """
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]


def upload_to_postgresql(steam_data, friends_data, db_config):
    """
    Uploadt gegevens naar een PostgreSQL-database.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Leeg de tabellen alleen als ze bestaan
        if table_exists(cursor, 'steam_games'):
            cursor.execute('DELETE FROM steam_games')

        if table_exists(cursor, 'steam_friends'):
            cursor.execute('DELETE FROM steam_friends')

        # Maak de tabel voor games zonder de played_since kolom
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS steam_games (
                game_id BIGINT PRIMARY KEY,
                name TEXT,
                playtime_hours NUMERIC,
                genres TEXT,
                price NUMERIC
            )
        ''')

        # Voeg games toe aan de database zonder played_since
        for game in steam_data['response'].get('games', []):
            app_id = game['appid']
            playtime_hours = round(game['playtime_forever'] / 60, 2) if game['playtime_forever'] else 0
            genres, price = fetch_game_details(app_id)

            cursor.execute('''
                INSERT INTO steam_games (game_id, name, playtime_hours, genres, price)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE
                SET 
                    name = EXCLUDED.name,
                    playtime_hours = EXCLUDED.playtime_hours,
                    genres = EXCLUDED.genres,
                    price = EXCLUDED.price
            ''', (app_id, game.get('name', 'Onbekend'), playtime_hours, genres, price))

        # Maak de tabel voor vrienden
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS steam_friends (
                friend_id BIGINT PRIMARY KEY,
                friend_name TEXT,
                friend_status TEXT,
                current_game TEXT
            )
        ''')

        # Voeg vrienden toe aan de database
        for friend in friends_data:
            friend_id = friend['steamid']
            friend_name = friend.get('personaname', 'Onbekend')
            friend_status = {0: 'Offline', 1: 'Online', 2: 'Busy', 3: 'Away', 4: 'Snooze', 5: 'Looking to Trade',
                            6: 'Looking to Play'}.get(friend.get('personastate', 0), 'Onbekend')
            current_game = friend.get('gameextrainfo', None)

            cursor.execute('''
                INSERT INTO steam_friends (friend_id, friend_name, friend_status, current_game)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (friend_id) DO UPDATE
                SET 
                    friend_name = EXCLUDED.friend_name,
                    friend_status = EXCLUDED.friend_status,
                    current_game = EXCLUDED.current_game
            ''', (friend_id, friend_name, friend_status, current_game))

        conn.commit()
        print("Gegevens succesvol geüpload naar de database.")

    except Exception as e:
        print(f"Fout bij uploaden: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def fetch_friends_data(api_key, steam_id):
    """
    Haalt gegevens op over vrienden van een gebruiker via de Steam API.
    """
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {
        'key': api_key,
        'steamid': steam_id,
        'relationship': 'friend'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Steam API fout: {response.status_code}, {response.text}")


def fetch_player_summaries(api_key, steam_ids):
    """
    Haalt uitgebreide spelersgegevens op voor een lijst van Steam IDs via de Steam API.
    """
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': api_key,
        'steamids': ','.join(steam_ids)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Steam API fout: {response.status_code}, {response.text}")


def get_steam_data_for_user(username):
    """
    Haalt alle benodigde gegevens voor de opgegeven gebruiker en uploadt naar de database.
    """
    try:
        print(f"Steam ID ophalen voor gebruiker: {username}")
        steam_id = get_steam_id(STEAM_API_KEY, username)
        print(f"De Steam ID van {username} is: {steam_id}")

        print("Steam gegevens ophalen...")
        steam_data = fetch_steam_data(steam_id, STEAM_API_KEY)

        print("Vriendenlijst ophalen...")
        friends_data_raw = fetch_friends_data(STEAM_API_KEY, steam_id)
        friend_ids = [friend['steamid'] for friend in friends_data_raw['friendslist']['friends']]

        print("Gedetailleerde vriendengegevens ophalen...")
        friends_data = fetch_player_summaries(STEAM_API_KEY, friend_ids)['response']['players']

        print("Gegevens uploaden naar PostgreSQL...")
        upload_to_postgresql(steam_data, friends_data, POSTGRESQL_CONFIG)

    except Exception as e:
        print(f"Fout opgetreden: {e}")


def load_friends():
    """
    Laad vrienden van de database.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**POSTGRESQL_CONFIG)
        cursor = conn.cursor()

        # Execute a query to fetch all friends from the 'steam_friends' table
        cursor.execute('SELECT friend_id, friend_name, friend_status, current_game FROM steam_friends')
        friends = cursor.fetchall()  # Fetch all results as a list of tuples

        return friends  # Return the list of tuples

    except Exception as e:
        print(f"Fout bij laden vrienden: {e}")
        return []  # Return an empty list if an error occurs
    finally:
        if conn:
            cursor.close()  # Close the cursor
            conn.close()  # Close the connection

def onlineFriends():
    """
    Laad alleen online vrienden van de database en vul aan met offline vrienden als er minder dan 5 online zijn.
    """
    friends = load_friends()
    online_friends = [friend for friend in friends if friend[2] == 'Online']
    
    if len(online_friends) < 5:
        offline_friends = [friend for friend in friends if friend[2] == 'Offline']
        remaining_count = 5 - len(online_friends)
        online_friends.extend(offline_friends[:remaining_count])

    return online_friends


def load_game_data():
    """
    Laad de gamegegevens van de database.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**POSTGRESQL_CONFIG)
        cursor = conn.cursor()

        # Execute a query to fetch all games from the 'steam_games' table
        cursor.execute('SELECT game_id, name, playtime_hours, genres FROM steam_games')
        games = cursor.fetchall()  # Fetch all results as a list of tuples

        return games  # Return the list of tuples

    except Exception as e:
        print(f"Fout bij laden games: {e}")
        return []  # Return an empty list if an error occurs
    finally:
        if conn:
            cursor.close()  # Close the cursor
            conn.close()  # Close the connection
