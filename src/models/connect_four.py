import numpy as np

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((6, 7))  # A 6x7 matrix to represent the board
        self.turn = 1  # player 1 goes first
        self.search_algorithm = "Minimax"  # default search algorithm
        self.depth = 4 # default depth for minimax and alpha-beta pruning

    def player_move(self, column):
        # Adds a piece to the lowest empty position in the selected column
        if self.make_move(column):
            self.switch_turn()
            self.computer_move(self.depth)
            return True
        else:
            return False

    def make_move(self, column):
        # Adds a piece to the lowest empty position in the selected column
        if self.board[0][column] != 0:
            # column is full, invalid move
            return False
        else:
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = self.turn
                    return True
                
    def undo_move(self, column):
        for row in range(6):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break
                
    def computer_move(self, depth):
        best_score = float('-inf')
        best_col = -1

        for col in range(7):
            if self.make_move(col):
                if self.search_algorithm == "AlphaBeta":
                    score = self.alpha_beta(depth, float('-inf'), float('inf'), False)
                else:
                    score = self.minimax(depth, False)
                self.undo_move(col)

                if score > best_score:
                    best_score = score
                    best_col = col
                    
        if best_col != -1:
            self.make_move(best_col)
            self.switch_turn()
    
    def check_winner(self):
        # Verifies if a player has won
        for i in range(6):
            for j in range(7):
                # check horizontal
                if j < 4 and self.board[i][j] == self.turn and self.board[i][j+1] == self.turn and self.board[i][j+2] == self.turn and self.board[i][j+3] == self.turn:
                    return True
                # check vertical
                if i < 3 and self.board[i][j] == self.turn and self.board[i+1][j] == self.turn and self.board[i+2][j] == self.turn and self.board[i+3][j] == self.turn:
                    return True
                # check diagonal to the right
                if i < 3 and j < 4 and self.board[i][j] == self.turn and self.board[i+1][j+1] == self.turn and self.board[i+2][j+2] == self.turn and self.board[i+3][j+3] == self.turn:
                    return True
                # check diagonal to the left
                if i < 3 and j > 2 and self.board[i][j] == self.turn and self.board[i+1][j-1] == self.turn and self.board[i+2][j-2] == self.turn and self.board[i+3][j-3] == self.turn:
                    return True
        return False
    
    def switch_turn(self):
        self.turn = 3 - self.turn  # Alternar entre el jugador 1 (1) y el jugador 2 (2)

    # Evaluation function for Minimax and Alpha-Beta pruning
    def evaluate_board(self):
        score = 0
        directions = [(0, 1), (0, -1), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == self.turn:
                    # favor moves that block the opponent's potential wins
                    for direction in directions:
                        count = 0
                        for k in range(1, 4):
                            row = i + direction[0] * k
                            col = j + direction[1] * k
                            if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == self.turn:
                                count += 1
                            else:
                                break
                        if count == 3 and 0 <= i + direction[0] * 4 < 6 and 0 <= j + direction[1] * 4 < 7 and self.board[i + direction[0] * 4][j + direction[1] * 4] == 0:
                            score += 1
                elif self.board[i][j] == 3 - self.turn:
                    # favor moves that result in the opponent being unable to block our win
                    for direction in directions:
                        count = 0
                        for k in range(1, 4):
                            row = i + direction[0] * k
                            col = j + direction[1] * k
                            if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == (3 - self.turn):
                                count += 1
                            else:
                                break
                        if count == 3 and 0 <= i + direction[0] * 4 < 6 and 0 <= j + direction[1] * 4 < 7 and self.board[i + direction[0] * 4][j + direction[1] * 4] == 0:
                            score -= 10
        return score

    # Minimax algorithm
    def minimax(self, depth, maximizing_player):
        """
        Returns the optimal evaluation value for the current game state using the minimax algorithm.

        Args:
            depth (int): The current depth of the search tree.
            maximizing_player (bool): True if it's the maximizing player's turn, False otherwise.

        Returns:
            float: The optimal evaluation value for the current game state.
        """
        # Base case - evaluation at leaf nodes
        if depth == 0:
            return self.evaluate_board()

        # Recursive case - maximizer's turn
        if maximizing_player:
            max_eval = float('-inf')
            for col in (col for col in range(7) if self.make_move(col)):
                eval = self.minimax(depth-1, False)
                self.undo_move(col)
                max_eval = max(max_eval, eval)
                if max_eval == 1:  # Early exit if winning move found
                    break
            return max_eval
        # Recursive case - minimizer's turn
        else:
            min_eval = float('inf')
            for col in (col for col in range(7) if self.make_move(col)):
                eval = self.minimax(depth-1, True)
                self.undo_move(col)
                min_eval = min(min_eval, eval)
                if min_eval == -1:  # Early exit if losing move found
                    break
            return min_eval
    
    # Alpha-beta pruning
    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        # Base case - evaluation at leaf nodes
        if depth == 0 or self.check_winner():
            return self.evaluate_board()
        
        if maximizing_player:
            max_eval = float('-inf')
            for col in range(7):
                if self.make_move(col):
                    eval = self.alpha_beta(depth-1, alpha, beta, False)
                    self.undo_move(col)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(7):
                if self.make_move(col):
                    eval = self.alpha_beta(depth-1, alpha, beta, True)
                    self.undo_move(col)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval