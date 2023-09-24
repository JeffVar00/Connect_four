class Player:
    def __init__(self, player_number):
        self.player_number = player_number

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