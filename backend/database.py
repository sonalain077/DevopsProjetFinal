import psycopg2

DATABASE_URL = "postgresql://user:password@db:5432/basket"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
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
    conn.close()

init_db()
