const API_URL = "http://backend:8000/players/";


async function searchPlayer() {
    let playerName = document.getElementById("playerName").value;

    if (playerName.trim() === "") {
        alert("Veuillez entrer un nom de joueur !");
        return;
    }

    try {
        let response = await fetch(API_URL + encodeURIComponent(playerName));
        
        console.log("Réponse API:", response); // Debugging

        if (response.ok) {
            let player = await response.json();
            console.log("Données joueur:", player);  // Debugging

            document.getElementById("playerInfo").innerHTML = `
                <h2>${player.name} (${player.team})</h2>
                <p>Points par match : ${player.points_per_game}</p>
                <p>Passes décisives : ${player.assists_per_game}</p>
                <p>Rebonds : ${player.rebounds_per_game}</p>
            `;
        } else {
            console.log("Erreur API :", response.statusText);
            document.getElementById("playerInfo").innerHTML = "<p>Joueur introuvable.</p>";
        }
    } catch (error) {
        console.error("Erreur lors de la requête :", error);
        document.getElementById("playerInfo").innerHTML = "<p>Erreur de connexion.</p>";
    }
}
