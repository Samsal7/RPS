from flask import Flask, jsonify, request
# from flask_cors import CORS
from sklearn import svm

app = Flask(__name__)
# CORS(app)pip

# Initialize game variables
history = [1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
input_data = [
    [1, 1],
    [1, 2],
    [3, 2],
    [2, 1],
]
output_data = [3, 2, 1, 1]

model = svm.SVC()
model.fit(input_data, output_data)

# Track total wins, losses, and ties
num_player_wins = 0
num_comp_wins = 0
num_ties = 0


@app.route("/play", methods=["POST"])
def play_game():
  global num_player_wins, num_comp_wins, num_ties
  user_move = request.json.get("move")
  if user_move == 1:
    user_move_name = "Rock"
  elif user_move == 2:
    user_move_name = "Paper"
  elif user_move == 3:
    user_move_name = "Scissors"
  else:
    user_move_name = ""
    
  def getPlayer1():
    data_record = [history[-2], history[-1]]
    current = model.predict([data_record])[0]
    if current == 1:
      return 2
    if current == 2:
      return 3
    return 1

  comp_move = getPlayer1()
  if comp_move == 1:
    comp_move_name = "Rock"
  elif comp_move == 2:
    comp_move_name = "Paper"
  elif comp_move == 3:
    comp_move_name = "Scissors"
  else:
    comp_move_name = ""

  result = ""
  if comp_move == user_move:
    result = "It's a tie"
    num_ties += 1
  elif (comp_move == 1
        and user_move == 2) or (comp_move == 2
                                and user_move == 3) or (comp_move == 3
                                                        and user_move == 1):
    result = "You win!!"
    num_player_wins += 1
  else:
    result = "You lose!!"
    num_comp_wins += 1

  history.append(user_move)
  input_data.append([history[-3], history[-2]])
  output_data.append(history[-1])
  model.fit(input_data, output_data)

  return jsonify({
      "player_move": user_move_name,
      "computer_move": comp_move_name,
      "result": result,
      "num_player_wins": num_player_wins,
      "num_comp_wins": num_comp_wins,
      "num_ties": num_ties
  })


@app.route("/reset", methods=["POST"])
def reset_game():
  global num_player_wins, num_comp_wins, num_ties
  num_player_wins = 0
  num_comp_wins = 0
  num_ties = 0

  return jsonify({
      "num_player_wins": num_player_wins,
      "num_comp_wins": num_comp_wins,
      "num_ties": num_ties
  })


app.run(host='0.0.0.0')
