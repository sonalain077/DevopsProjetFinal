const API_URL = "http://localhost:8000/players/";

async function searchPlayer() {
    let playerName = document.getElementById("playerName").value;

    if (playerName.trim() === "") {
        alert("Veuillez entrer un nom de joueur !");
        return;
    }

    try {
        let response = await fetch(API_URL + encodeURIComponent(playerName));
        
        console.log("Réponse API:", response);

        if (response.ok) {
            let player = await response.json();
            console.log("Données joueur:", player);

            document.getElementById("playerInfo").innerHTML = `
                <h2>${player.name} (${player.team})</h2>
                <p>Points par match : ${player.points_per_game}</p>
                <p>Rebonds par match : ${player.average_total_rebounds}</p>
                <p>Passes par match : ${player.average_assists}</p>
                <p>Field Goal % : ${player.field_goal_percentage}</p>
                <p>Three Point % : ${player.three_point_percentage}</p>
                <p>Free Throw % : ${player.free_throw_percentage}</p>
                <p>Moyenne minutes jouées : ${player.average_minutes_played}</p>
                <p>Win Shares : ${player.win_shares}</p>
                <p>Win Shares per 48 min : ${player.win_shares_per_48_minutes}</p>
                <p>Box Plus Minus : ${player.box_plus_minus}</p>
                <p>Value Over Replacement : ${player.value_over_replacement}</p>
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
