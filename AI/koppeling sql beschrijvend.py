import psycopg2

# Configuraties voor PostgreSQL
POSTGRESQL_CONFIG = {
    'host': '20.16.230.195',
    'port': 5432,
    'database': 'SteamBox',
    'user': 'postgres',
    'password': 'IDEA'
}

def fetch_playtime_data(db_config):
    """
    Haalt de speeltijden van spellen op uit de PostgreSQL-database.
    """
    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Haal speeltijdgegevens op
        cursor.execute("SELECT playtime_forever FROM steam_games")
        rows = cursor.fetchall()

        # Converteer rijen naar een lijst met integers
        playtimes = [row[0] for row in rows if row[0] is not None]

        return playtimes

    except Exception as e:
        print(f"Fout bij het ophalen van gegevens: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

def calculate_statistics(playtimes):
    """
    Bereken het gemiddelde en de mediaan van een lijst met speeltijden zonder externe bibliotheken.
    """
    if not playtimes:
        print("Geen gegevens beschikbaar om statistieken te berekenen.")
        return None, None

    # Bereken gemiddelde
    mean_playtime = sum(playtimes) / len(playtimes)

    # Bereken mediaan
    sorted_playtimes = sorted(playtimes)
    n = len(sorted_playtimes)
    if n % 2 == 0:
        median_playtime = (sorted_playtimes[n // 2 - 1] + sorted_playtimes[n // 2]) / 2
    else:
        median_playtime = sorted_playtimes[n // 2]

    return mean_playtime, median_playtime

if __name__ == "__main__":
    try:
        print("Speeltijdgegevens ophalen...")
        playtime_data = fetch_playtime_data(POSTGRESQL_CONFIG)

        if playtime_data:
            print("Statistieken berekenen...")
            mean, median = calculate_statistics(playtime_data)

            print(f"Gemiddelde speeltijd: {mean:.2f} minuten")
            print(f"Mediaan speeltijd: {median:.2f} minuten")
        else:
            print("Geen speeltijdgegevens beschikbaar om te verwerken.")

    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
