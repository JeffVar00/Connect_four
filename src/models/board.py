class GameBoard:
    def __init__(self):
        self.board = np.zeros((6, 7))  # A 6x7 matrix to represent the board
    

    def make_move(self, column, player):
        # Adds a piece to the lowest empty position in the selected column
        if self.board[0][column] != 0:
            # column is full, invalid move
            return False
        else:
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = player
                    return True
    
    def undo_move(self, column):
        for row in range(6):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break
    
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