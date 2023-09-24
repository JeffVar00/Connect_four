class ComputerPlayer(Player):
    def __init__(self, player_number, search_algorithm="Minimax", depth=4):
        super().__init__(player_number)
        self.search_algorithm = search_algorithm
        self.depth = depth

    
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

    def minimax(self, depth, maximizing_player):
        # Base case - evaluation at leaf nodes
        if depth == 0 or self.check_winner():
            return self.evaluate_board()
        
        # Recursive case - maximizer's turn
        if maximizing_player:
            max_eval = float('-inf')
            for col in range(7):
                if self.make_move(col):
                    eval = self.minimax(depth-1, False)
                    self.undo_move(col)
                    max_eval = max(max_eval, eval)
            return max_eval
        # Recursive case - minimizer's turn
        else:
            min_eval = float('inf')
            for col in range(7):
                if self.make_move(col):
                    eval = self.minimax(depth-1, True)
                    self.undo_move(col)
                    min_eval = min(min_eval, eval)          
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
    