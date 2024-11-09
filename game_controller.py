import requests
import numpy as np
from PushBattle import Game, PLAYER1, PLAYER2

PLAYER1_URL = "http://localhost:5008"
PLAYER2_URL = "http://localhost:5009"

def start_game():
    """Send a start game request to each player."""
    game = Game()
    
    # Convert board to list if it's an ndarray or any other numpy type
    board = game.board.tolist() if isinstance(game.board, np.ndarray) else game.board

    data = {
        "game": game.to_dict(),
        "board": board,
        "first_turn": True,  # Assuming Player 1 starts
        "max_latency": 5  # Example latency in seconds
    }

    # Notify both players that the game is starting
    requests.post(f"{PLAYER1_URL}/start", json=data)
    data["first_turn"] = False
    requests.post(f"{PLAYER2_URL}/start", json=data)

    return game

def play_game(game):
    """Plays the game by alternating between player moves until it ends."""
    turn = PLAYER1
    turn_count = 1

    while not game.is_game_over():
        # Decide which player URL to use
        player_url = PLAYER1_URL if turn == PLAYER1 else PLAYER2_URL

        # Prepare data for the move request
        data = {
            "game": game.to_dict(),
            "board": game.board,
            "turn_count": turn_count,
            "attempt_number": 1
        }

        # Get move from the agent
        response = requests.post(f"{player_url}/move", json=data)
        move = response.json().get("move")

        if not move:
            print(f"Player {turn} did not return a valid move. Ending game.")
            break

        # Apply move in the game instance
        try:
            game.apply_move(move)
            print(f"Player {turn} made move: {move}")
        except Exception as e:
            print(f"Invalid move by Player {turn}: {move} - {e}")
            break

        # Switch turns
        turn = PLAYER1 if turn == PLAYER2 else PLAYER2
        turn_count += 1

    # Notify both players that the game has ended
    end_data = {
        "game_result": game.get_result(),  # Result of the game
    }
    requests.post(f"{PLAYER1_URL}/end", json=end_data)
    requests.post(f"{PLAYER2_URL}/end", json=end_data)

    print("Game over!")
    print("Result:", game.get_result())

# Run the game
if __name__ == "__main__":
    game = start_game()
    play_game(game)
