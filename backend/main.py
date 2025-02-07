from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import threading
from database import get_db_connection, init_db

app = FastAPI()

# Autoriser le CORS pour la communication avec le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À modifier en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin du fichier CSV
CSV_FILE_PATH = "nbaplayersdraft.csv"

def import_csv_to_db():
    """
    Importe les données du CSV dans la base, uniquement si la table est vide.
    """
    conn = get_db_connection()
    if conn is None:
        print("Connexion à la base impossible dans import_csv_to_db")
        return
    cursor = conn.cursor()
    # Vérifier si la table est déjà peuplée
    cursor.execute("SELECT COUNT(*) FROM players;")
    count = cursor.fetchone()[0]
    if count == 0:
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
        print("Importation du CSV réussie !")
    cursor.close()
    conn.close()

@app.get("/players/{name}")
def get_player(name: str):
    """
    Récupère les statistiques d'un joueur via un filtrage par nom.
    """
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
            "points_per_game": float(player[13]) if player[13] is not None else 0.0,
            "assists_per_game": float(player[15]) if player[15] is not None else 0.0,
            "rebounds_per_game": float(player[14]) if player[14] is not None else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="Player not found")

# Lancer l'import du CSV avec un délai (10 secondes)
threading.Timer(10.0, import_csv_to_db).start()

if __name__ == "__main__":
    # Initialiser la base avant de démarrer le serveur
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

