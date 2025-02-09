import psycopg2
import time
import sys

DATABASE_URL = "postgresql://user:password@localhost:5432/basket"

def get_db_connection(retries=5, delay=5):
    """
    Tente de se connecter à la base de données plusieurs fois avant d'abandonner.
    """
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            print("Connexion à la base réussie à la tentative", attempt + 1)
            return conn
        except psycopg2.OperationalError as e:
            print(f"Tentative {attempt + 1} échouée : {e}. Nouvelle tentative dans {delay} secondes...")
            time.sleep(delay)
    print("Impossible de se connecter à la base après plusieurs tentatives.")
    sys.exit(1)

def init_db():
    """
    Initialise la table players dans la base de données si elle n'existe pas.
    """
    conn = get_db_connection()
    if conn is None:
        print("Échec de connexion lors de l'initialisation de la base.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            year INT,
            rank INT,
            overall_pick INT,
            team TEXT,
            player TEXT,
            college TEXT,
            years_active FLOAT,
            games FLOAT,
            minutes_played FLOAT,
            field_goal_percentage FLOAT,
            three_point_percentage FLOAT,
            free_throw_percentage FLOAT,
            average_minutes_played FLOAT,
            points_per_game FLOAT,
            average_total_rebounds FLOAT,
            average_assists FLOAT,
            win_shares FLOAT,
            win_shares_per_48_minutes FLOAT,
            box_plus_minus FLOAT,
            value_over_replacement FLOAT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Base de données initialisée avec succès.")

# Note : Nous n'appelons pas init_db() ici pour éviter que ce code ne s'exécute lors de l'import.
if __name__ == "__main__":
    init_db()
