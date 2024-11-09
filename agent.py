from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus
import copy

class Agent:
    def __init__(self, player=PLAYER1):
        self.player = player

    def get_possible_moves(self, game):
        """Returns a list of all possible moves in the current state."""
        moves = []
        current_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces

        if current_pieces < NUM_PIECES:
            # Generate placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # Generate movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves

    def get_best_move(self, game):
        """Returns the best move based on a refined evaluation strategy."""
        possible_moves = self.get_possible_moves(game)

        # If no moves are possible, return None
        if not possible_moves:
            return None

        best_move = None
        best_score = float('-inf')

        # Evaluate each possible move
        for move in possible_moves:
            # Create a deep copy of the game state to evaluate this move
            new_game_state = self.create_game_copy(game)
            self.apply_move(new_game_state, move)
            score = self.evaluate_move(new_game_state)

            # Maximize score for the current player
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def create_game_copy(self, game):
        """Creates a deep copy of the game state."""
        new_game = Game()
        new_game.board = copy.deepcopy(game.board)
        new_game.current_player = game.current_player
        new_game.p1_pieces = game.p1_pieces
        new_game.p2_pieces = game.p2_pieces
        return new_game

    def apply_move(self, game, move):
        """Applies a move to a temporary game state."""
        if len(move) == 2:  # Placement move
            r, c = move
            game.board[r][c] = game.current_player
            if game.current_player == PLAYER1:
                game.p1_pieces += 1
            else:
                game.p2_pieces += 1
        elif len(move) == 4:  # Movement move
            r0, c0, r1, c1 = move
            game.board[r0][c0] = EMPTY
            game.board[r1][c1] = game.current_player

    def evaluate_move(self, game):
        """Enhanced evaluation function emphasizing winning moves and blocking opponents."""
        score = 0
        center = BOARD_SIZE // 2

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == PLAYER1:
                    # Center control
                    score += (BOARD_SIZE - abs(r - center) - abs(c - center))

                    # Reward 3-in-a-row opportunities
                    if self.would_win(game, PLAYER1, r, c):
                        score += 1000  # High value for winning moves
                elif game.board[r][c] == PLAYER2:
                    # Deduct points if opponent is in favorable position
                    score -= (BOARD_SIZE - abs(r - center) - abs(c - center))

                    # Prevent opponent's 3-in-a-row
                    if self.would_win(game, PLAYER2, r, c):
                        score -= 1000  # High value to block opponent's win

        return score

    def would_win(self, game, player, row, col):
        """Checks if placing/moving a piece to (row, col) creates a 3-in-a-row."""
        directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for dr, dc in directions:
            count = 0
            for i in range(-2, 3):
                r, c = _torus(row + i * dr, col + i * dc)
                if game.board[r][c] == player:
                    count += 1
                    if count == 3:
                        return True
                else:
                    count = 0
        return False
