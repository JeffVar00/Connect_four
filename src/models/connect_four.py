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

        best_move = -1
        best_value = float('-inf')

        if self.search_algorithm == "Minimax":

            print("Minimax")
            
            for col in range(7):
                if self.board[0][col] == 0:
                    self.make_move(col)
                    self.switch_turn()
                    move_value = self.minimax(
                        self.depth - 1, False)
                    self.undo_move(col)
                    self.switch_turn()
                    if move_value > best_value:
                        best_move = col
                        best_value = move_value
        
        elif self.search_algorithm == "AlphaBeta":

            print("Alpha Beta")

            for col in range(7):
                if self.board[0][col] == 0:
                    self.make_move(col)
                    self.switch_turn()
                    move_value = self.alpha_beta(
                        self.depth - 1, -np.inf, np.inf, False)
                    self.undo_move(col)
                    self.switch_turn()
                    if move_value > best_value:
                        best_move = col
                        best_value = move_value

        self.make_move(best_move)

    def minimax(self, depth, is_maximizing):
        if self.is_board_full() or self.check_winner() or depth == 0:
            return self.evaluate_the_board()
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    self.switch_turn()
                    eval = self.minimax(depth - 1, False)
                    self.undo_move(col)
                    self.switch_turn()
                    max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col)
                    self.switch_turn()
                    eval = self.minimax(depth - 1, True)
                    self.undo_move(col)
                    self.switch_turn()
                    min_eval = min(min_eval, eval)
            return min_eval
            
        
    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        if self.is_board_full() or self.check_winner() or depth == 0:
            return self.evaluate_the_board()

        if is_maximizing:
            max_result = float('-inf')
            for col in range(7):
                if self.board[0][col] == 0:
                    self.make_move(col)
                    self.switch_turn()
                    evaluation = self.alpha_beta(depth - 1, alpha, beta, False)
                    self.undo_move(col)
                    self.switch_turn()
                    max_result = max(max_result, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break

            return max_result
        
        min_result = float('inf')
        for col in range(7):
            if self.board[0][col] == 0:
                self.make_move(col)
                self.switch_turn()
                evaluation = self.alpha_beta(depth - 1, alpha, beta, True)
                self.undo_move(col)
                self.switch_turn()
                min_result = min(min_result, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

        return min_result
        
    def evaluate_the_board(self):
        """
        Evalua el tablero, aqui suponemos que 2 es la IA y 1 el jugador
        """
        if self.turn == 2:
            return 1
        if self.turn == 1:
            return -1
        return 0

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
