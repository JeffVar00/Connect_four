import numpy as np

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((6, 7))  # Matriz 6x7 para representar el tablero
        self.turn = 1  # Jugador 1 comienza primero
        self.search_algorithm = "Minimax"  # Algoritmo de búsqueda predeterminado
        self.depth = 4  # Profundidad predeterminada para minimax y poda alfa-beta


    def reset(self):
        """
        Reinicia el juego, estableciendo el tablero en blanco y el turno en el jugador 1.
        """
        self.board = np.zeros((6, 7))
        self.turn = 1

    def player_move(self, column):
        
        """
        Maneja los movimientos del jugador y actualiza la interfaz gráfica.
        """

        if self.turn != 1:
            self.switch_turn()
        
        if self.make_move(column):
            
            if self.check_winner():
                return True

            self.switch_turn()
            self.computer_move()
            return True
        else:
            return False
        
    def is_valid_move(self, column):
        """
        Verifica si un movimiento es válido.
        """
        return self.board[0][column] == 0

    def make_move(self, column):
        """
        Agrega una pieza a la posición más baja vacía en la columna seleccionada
        """
        
        if self.board[0][column] != 0:
            # Movimiento inválido
            return False
        else:
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = self.turn
                    return True
                
    def undo_move(self, column):
        
        """
        Deshace el último movimiento del jugador de la computadora.
        """

        for row in range(6):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break

    def computer_move(self):
        if self.search_algorithm == "Minimax":
            _, chosen_column = self.minimax(self.depth, True)
        elif self.search_algorithm == "AlphaBeta":
            _, chosen_column = self.alpha_beta(self.depth, -np.inf, np.inf, True)
        self.make_move(chosen_column)

    def minimax(self, depth, is_maximizing):
        if self.is_board_full() or self.check_winner() or depth == 0:
            return self.evaluate_the_board(), None
            
        if is_maximizing:
            value = -np.inf
            column = np.random.choice([c for c in range(7) if self.is_valid_move(c)])
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    new_score, _ = self.minimax(depth-1, False)
                    if new_score > value:
                        value = new_score
                        column = col
                    self.undo_move(col)
            return value, column

        else: # Minimizing player
            value = np.inf
            column = np.random.choice([c for c in range(7) if self.is_valid_move(c)])
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    new_score, _ = self.minimax(depth-1, True)
                    if new_score < value:
                        value = new_score
                        column = col
                    self.undo_move(col)
            return value, column
        
    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        if self.is_board_full() or self.check_winner() or depth == 0:
            return self.evaluate_the_board(), None

        if is_maximizing:
            value = -np.inf
            column = np.random.choice([c for c in range(7) if self.is_valid_move(c)])
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    new_score, _ = self.alpha_beta(depth-1, alpha, beta, False)
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    self.undo_move(col)
                    if alpha >= beta:
                        break
            return value, column
            
        else: # Minimizing player
            value = np.inf
            column = np.random.choice([c for c in range(7) if self.is_valid_move(c)])
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    new_score, _ = self.alpha_beta(depth-1, alpha, beta, True)
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    self.undo_move(col)
                    if beta <= alpha:
                        break
            return value, column
        
    def evaluate_the_board(self):
        # Matriz de puntuaciones para los posibles escenarios
        scores = [[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]]

        score = 0

        # Evaluar el tablero para el jugador 1 (oponente)
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row, col] == 1:
                    score -= scores[row][col]

        # Evaluar el tablero para el jugador 2 (IA)
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row, col] == 2:
                    score += scores[row][col]

        return score

    def check_winner(self):
        """
        Verifica si un jugador ha ganado.
        """
        for i in range(6):
            for j in range(7):
                # Verifica horizontalmente
                if j < 4 and self.board[i][j] == self.turn and self.board[i][j+1] == self.turn and self.board[i][j+2] == self.turn and self.board[i][j+3] == self.turn:
                    return True
                # Verifica verticalmente
                if i < 3 and self.board[i][j] == self.turn and self.board[i+1][j] == self.turn and self.board[i+2][j] == self.turn and self.board[i+3][j] == self.turn:
                    return True
                # Verifica diagonal a la derecha
                if i < 3 and j < 4 and self.board[i][j] == self.turn and self.board[i+1][j+1] == self.turn and self.board[i+2][j+2] == self.turn and self.board[i+3][j+3] == self.turn:
                    return True
                # Verifica diagonal a la izquierda
                if i < 3 and j > 2 and self.board[i][j] == self.turn and self.board[i+1][j-1] == self.turn and self.board[i+2][j-2] == self.turn and self.board[i+3][j-3] == self.turn:
                    return True
        return False
    
    def switch_turn(self):
        self.turn = 3 - self.turn  # Alternar entre el jugador 1 (1) y el jugador 2 (2)

    def is_board_full(self):
        return all(self.board[0][col] != 0 for col in range(7))
