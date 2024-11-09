from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Initialize global variables
team_name = "EthNayIs"
agent_name = "ChatGPTBot"

# Replace this with your move-making algorithm, such as Minimax, MCTS, etc.
def calculate_best_move(board_state):
    # Placeholder logic for best move; replace with your game strategy
    empty_positions = [(i, j) for i in range(8) for j in range(8) if board_state[i][j] == 0]
    return empty_positions[0] if empty_positions else (0, 0)  # Select first empty position as a default

@app.route("/", methods=["GET"])
def home():
    return jsonify({"Team": team_name, "Agent": agent_name})

@app.route("/start", methods=["POST"])
def start_game():
    data = request.get_json()
    game_id = data.get("game")
    turn = data.get("turn")
    board_state = data.get("board")
    
    print(f"Game {game_id} started. Turn: {turn}. Initial board state received.")
    return jsonify({"status": "Game started", "game_id": game_id})

@app.route("/move", methods=["POST"])
def make_move():
    data = request.get_json()
    board_state = data.get("board")

    # Convert the board state to a numpy array for easier processing
    board = np.array(board_state)
    
    # Calculate the best move based on your strategy
    move_row, move_col = calculate_best_move(board)
    
    print(f"Making move at ({move_row}, {move_col})")
    
    return jsonify({"move_row": move_row, "move_col": move_col})

@app.route("/end", methods=["POST"])
def end_game():
    data = request.get_json()
    game_id = data.get("game")
    turn = data.get("turn")
    board_state = data.get("board")
    
    print(f"Game {game_id} ended. Final turn: {turn}. Final board state received.")
    return jsonify({"status": "Game ended", "game_id": game_id})

@app.route("/test/start", methods=["POST"])
def test_start():
    data = request.get_json()
    return start_game()

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
