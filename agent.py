from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES

class Agent:
    def __init__(self, player=PLAYER1, depth=2):
        self.player = player
        self.depth = depth

    def evaluate_board(self, board):
        """Evaluate the board state."""
        score = 0
        for row in board:
            for cell in row:
                if cell == PLAYER1:
                    score += 10
                elif cell == PLAYER2:
                    score -= 10
        return score

    def minimax(self, state, depth, alpha, beta, is_maximizing_player):
        if depth == 0 or self.is_terminal_state(state):
            return self.evaluate_board(state.board)

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(state, self.player):
                new_state = self.apply_move(state, move, self.player)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(state, PLAYER2):
                new_state = self.apply_move(state, move, PLAYER2)
                eval = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, game):
        best_score = float('-inf')
        best_move = None
        for move in self.get_possible_moves(game, self.player):
            new_state = self.apply_move(game, move, self.player)
            score = self.minimax(new_state, self.depth - 1, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move

        # Fallback to a random valid move if no best move is found (to avoid forfeiting)
        if best_move is None:
            best_move = self.get_random_move(game)

        return best_move

    def get_possible_moves(self, game, player):
        """Get all possible moves for a player based on game state."""
        moves = []
        if (game.p1_pieces if player == PLAYER1 else game.p2_pieces) < NUM_PIECES:
            # Placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # Movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves

    def apply_move(self, game, move, player):
        """Apply a move to the game state to generate a new state."""
        new_game = game.copy()  # Assuming game state has a copy method
        if len(move) == 2:  # Placement move
            r, c = move
            new_game.board[r][c] = player
            if player == PLAYER1:
                new_game.p1_pieces += 1
            else:
                new_game.p2_pieces += 1
        elif len(move) == 4:  # Movement move
            r0, c0, r1, c1 = move
            new_game.board[r0][c0] = EMPTY
            new_game.board[r1][c1] = player
        return new_game

    def is_terminal_state(self, state):
        """Check if the game is in a terminal state (e.g., win condition or max pieces placed)."""
        # Placeholder logic for terminal condition; adapt as needed
        return state.p1_pieces >= NUM_PIECES and state.p2_pieces >= NUM_PIECES

    def get_random_move(self, game):
        """Fallback random move generator."""
        possible_moves = self.get_possible_moves(game, self.player)
        return random.choice(possible_moves) if possible_moves else None
