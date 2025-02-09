from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import pandas as pd
import threading
from database import get_db_connection, init_db

app = FastAPI()

# Autorisation CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, restreindre les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE_PATH = "nbaplayersdraft.csv"

def import_csv_to_db():
    conn = get_db_connection()
    if conn is None:
        print("Erreur de connexion à la base de données")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players;")
    count = cursor.fetchone()[0]
    if count == 0:
        df = pd.read_csv(CSV_FILE_PATH)
        for _, row in df.iterrows():
            # Calculer points_per_game à partir de "points" et "games"
            try:
                games = float(row["games"])
                points = float(row["points"])
                pg = points / games if games > 0 else 0.0
            except Exception as e:
                pg = 0.0
            cursor.execute("""
                INSERT INTO players (
                    year, rank, overall_pick, team, player, college, years_active, games, minutes_played,
                    field_goal_percentage, three_point_percentage, free_throw_percentage,
                    average_minutes_played, points_per_game, average_total_rebounds, average_assists,
                    win_shares, win_shares_per_48_minutes, box_plus_minus, value_over_replacement
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row["year"], row["rank"], row["overall_pick"], row["team"], row["player"], row["college"],
                row["years_active"], row["games"], row["minutes_played"],
                row["field_goal_percentage"], row["3_point_percentage"], row["free_throw_percentage"],
                row["average_minutes_played"], pg, row["average_total_rebounds"], row["average_assists"],
                row["win_shares"], row["win_shares_per_48_minutes"], row["box_plus_minus"], row["value_over_replacement"]
            ))
        conn.commit()
        print("Importation du CSV réussie")
    cursor.close()
    conn.close()

# Lancer l'import avec un délai pour laisser le temps à la BDD d'être prête
threading.Timer(10.0, import_csv_to_db).start()

@app.get("/players/{name}")
def get_player(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM players WHERE LOWER(player) LIKE LOWER(%s)", (f"%{name}%",))
    player = cursor.fetchone()
    conn.close()
    
    if player:
        # La structure de la ligne (SELECT *):
        # 0: id,
        # 1: year, 2: rank, 3: overall_pick, 4: team, 5: player, 6: college, 7: years_active,
        # 8: games, 9: minutes_played,
        # 10: field_goal_percentage, 11: three_point_percentage, 12: free_throw_percentage,
        # 13: average_minutes_played, 14: points_per_game, 15: average_total_rebounds,
        # 16: average_assists, 17: win_shares, 18: win_shares_per_48_minutes,
        # 19: box_plus_minus, 20: value_over_replacement
        return {
            "id": player[0],
            "name": player[5] if player[5] else "Inconnu",
            "team": player[4] if player[4] else "Inconnu",
            "field_goal_percentage": float(player[10]) if player[10] is not None else 0.0,
            "three_point_percentage": float(player[11]) if player[11] is not None else 0.0,
            "free_throw_percentage": float(player[12]) if player[12] is not None else 0.0,
            "average_minutes_played": float(player[13]) if player[13] is not None else 0.0,
            "points_per_game": float(player[14]) if player[14] is not None else 0.0,
            "average_total_rebounds": float(player[15]) if player[15] is not None else 0.0,
            "average_assists": float(player[16]) if player[16] is not None else 0.0,
            "win_shares": float(player[17]) if player[17] is not None else 0.0,
            "win_shares_per_48_minutes": float(player[18]) if player[18] is not None else 0.0,
            "box_plus_minus": float(player[19]) if player[19] is not None else 0.0,
            "value_over_replacement": float(player[20]) if player[20] is not None else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="Player not found")

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

