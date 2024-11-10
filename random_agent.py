from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus
import copy
import time

class RandomAgent:
    def __init__(self, player=PLAYER2, max_depth=4, time_limit=2.0):
        self.player = player
        self.first_move = True
        self.max_depth = max_depth
        self.time_limit = time_limit

    def get_possible_moves(self, game):
        moves = []
        center_moves = []
        current_pieces = game.p2_pieces if game.current_player == PLAYER2 else game.p1_pieces
        center = BOARD_SIZE // 2

        if current_pieces < NUM_PIECES:
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        move = (r, c)
                        if abs(r - center) <= 1 and abs(c - center) <= 1:
                            center_moves.append(move)
                        else:
                            moves.append(move)
            return center_moves + moves
        else:
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves

    def get_best_move(self, game):
        if self.first_move:
            self.first_move = False
            # Check if the center is occupied before choosing it
            if game.board[4][4] == EMPTY:
                return (4, 4)
            else:
                # If center is taken, pick another optimal position
                return (4, 3)

        best_move = None
        best_score = float('-inf')
        start_time = time.time()
        depth = 1

        while depth <= self.max_depth and (time.time() - start_time) < self.time_limit:
            current_best_move = None
            current_best_score = float('-inf')

            for move in self.get_possible_moves(game):
                new_game_state = self.create_game_copy(game)
                self.apply_move(new_game_state, move)
                score = self.minimax(new_game_state, depth - 1, False, float('-inf'), float('inf'), start_time)

                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move

            if current_best_score > best_score:
                best_score = current_best_score
                best_move = current_best_move

            depth += 1

        return best_move

    def minimax(self, game, depth, is_maximizing, alpha, beta, start_time):
        if (time.time() - start_time) >= self.time_limit:
            return 0

        winner = game.check_winner()
        if depth == 0 or winner != EMPTY:
            return self.evaluate_move(game)

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves(game):
                new_game_state = self.create_game_copy(game)
                self.apply_move(new_game_state, move)
                eval = self.minimax(new_game_state, depth - 1, False, alpha, beta, start_time)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(game):
                new_game_state = self.create_game_copy(game)
                self.apply_move(new_game_state, move)
                eval = self.minimax(new_game_state, depth - 1, True, alpha, beta, start_time)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def create_game_copy(self, game):
        new_game = Game()
        new_game.board = copy.deepcopy(game.board)
        new_game.current_player = game.current_player
        new_game.p1_pieces = game.p1_pieces
        new_game.p2_pieces = game.p2_pieces
        return new_game

    def apply_move(self, game, move):
        if len(move) == 2:
            r, c = move
            game.board[r][c] = game.current_player
            if game.current_player == PLAYER2:
                game.p2_pieces += 1
            else:
                game.p1_pieces += 1
            game.push_neighbors(r, c)
        elif len(move) == 4:
            r0, c0, r1, c1 = move
            game.board[r0][c0] = EMPTY
            game.board[r1][c1] = game.current_player
            game.push_neighbors(r1, c1)

    def evaluate_move(self, game):
        score = 0
        center = BOARD_SIZE // 2
        weights = [[center - max(abs(r - center), abs(c - center)) for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == PLAYER2:
                    score += weights[r][c] * 3
                    if self.is_multiple_winning_lines(game, PLAYER2, r, c):
                        score += 1500
                    if self.would_win(game, PLAYER2, r, c):
                        score += 1000
                elif game.board[r][c] == PLAYER1:
                    score -= weights[r][c] * 3
                    if self.is_multiple_winning_lines(game, PLAYER1, r, c):
                        score -= 1500
                    if self.would_win(game, PLAYER1, r, c):
                        score -= 1000
        return score

    def is_multiple_winning_lines(self, game, player, row, col):
        winning_lines = 0
        directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for dr, dc in directions:
            count = 0
            for i in range(-2, 3):
                r, c = _torus(row + i * dr, col + i * dc)
                if game.board[r][c] == player:
                    count += 1
                    if count == 3:
                        winning_lines += 1
                        break
                else:
                    count = 0
        return winning_lines >= 2

    def would_win(self, game, player, row, col):
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
