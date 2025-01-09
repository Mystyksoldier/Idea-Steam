import psycopg2

# Verbind met de PostgreSQL database
try:
    conn = psycopg2.connect(
        host="20.16.230.195",  # Je hebt het IP-adres van de host hier ingevuld
        port=5432,  # Standaard PostgreSQL-poort
        database="SteamBox",  # De naam van je database
        user="postgres",  # Je PostgreSQL-gebruikersnaam
        password="IDEA"  # Je wachtwoord
    )

    print("Verbonden met de database")

    # Maak een cursor object
    cursor = conn.cursor()

    # Voer een query uit (dit is een voorbeeld, vervang het met jouw query)
    cursor.execute("SELECT * FROM steam_games")  # Vervang 'jouw_tabel' met de juiste tabelnaam

    # Haal de gegevens op
    rows = cursor.fetchall()
    print("Gegevens opgehaald:", rows)

except Exception as e:
    print("Fout bij het ophalen van gegevens:", e)

finally:
    # Sluit de cursor en de verbinding
    if conn is not None:
        conn.close()
        print("Verbinding gesloten")
