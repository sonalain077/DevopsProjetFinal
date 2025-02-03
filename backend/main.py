from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import pandas as pd
from database import get_db_connection

app = FastAPI()

# 🌍 Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 CSV File Path
CSV_FILE_PATH = "nbaplayersdraft.csv"

# 📊 Import CSV to Database (Only if empty)
def import_csv_to_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the table is already populated
    cursor.execute("SELECT COUNT(*) FROM players;")
    count = cursor.fetchone()[0]

    if count == 0:  # Only insert if empty
        df = pd.read_csv(CSV_FILE_PATH)

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO players (
                    year, rank, overall_pick, team, player, college, years_active, games, minutes_played,
                    points_per_game, average_total_rebounds, average_assists
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row["year"], row["rank"], row["overall_pick"], row["team"], row["player"], row["college"],
                row["years_active"], row["games"], row["minutes_played"],
                row["points_per_game"], row["average_total_rebounds"], row["average_assists"]
            ))

        conn.commit()
        print("📊 Données importées avec succès depuis le fichier CSV !")
    
    cursor.close()
    conn.close()

# Run only if it's the first time
import_csv_to_db()

# 🏀 API to get player stats
@app.get("/players/{name}")
def get_player(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM players WHERE LOWER(player) LIKE LOWER(%s)", (f"%{name}%",))
    player = cursor.fetchone()
    conn.close()
    
    if player:
        return {
            "id": player[0],
            "name": player[5] if player[5] else "Inconnu",
            "team": player[4] if player[4] else "Inconnu",
            "points_per_game": float(player[13]) if player[13] is not None else 0.0,  # Avoid `null`
            "assists_per_game": float(player[15]) if player[15] is not None else 0.0,
            "rebounds_per_game": float(player[14]) if player[14] is not None else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="Player not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

