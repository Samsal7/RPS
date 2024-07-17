async function playGame(userMove) {
  var result = document.getElementById("result");
  var summary = document.getElementById("summary");

  try {
    var response = await fetch("https://rps-1-pq2i.onrender.com/play", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ move: userMove })
    });
    var data = await response.json();

    var gameResult = `<p id="inline"><strong>Computer Move:</strong></p>`;
    gameResult += `<p id="inline"><strong>Your Move:</strong> </p>`;
    gameResult += `<p><img src= "${data.computer_move}.png" style="width: 100px;" >  VS  <img src= "${data.player_move}.png" style="width: 100px;">`;
    gameResult += `<p><strong>Result:</strong> ${data.result}</p><br>`;
    result.innerHTML = gameResult;

    var gameSummary = `<p><strong>Total Wins:</strong> ${data.num_player_wins}</p>`;
    gameSummary += `<p><strong>Total Losses:</strong> ${data.num_comp_wins}</p>`;
    gameSummary += `<p><strong>Total Ties:</strong> ${data.num_ties}</p>`;
    gameSummary += `<button class = "reset" onclick="resetGame()">Reset</button>`;
    summary.innerHTML = gameSummary;

  } catch (err) {
    console.log("err", err);
  }
}

async function resetGame() {
  var summary = document.getElementById("summary");
  var result = document.getElementById("result");

  try {
    var response = await fetch("https://rps-1-pq2i.onrender.com/reset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });
    var data = await response.json();

    var gameSummary = `<p><strong>Total Wins:</strong> ${data.num_player_wins}</p>`;
    gameSummary += `<p><strong>Total Losses:</strong> ${data.num_comp_wins}</p>`;
    gameSummary += `<p><strong>Total Ties:</strong> ${data.num_ties}</p>`;
    gameSummary += `<button class = "reset" onclick="resetGame()">Reset</button>`;
    summary.innerHTML = gameSummary;
    result.innerHTML = "";

  } catch (err) {
    console.log("err", err);
  }
}
