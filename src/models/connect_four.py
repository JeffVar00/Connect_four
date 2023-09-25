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
            self.computer_move(self.depth)
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
                
    def computer_move(self, depth):
        
        """
        Elige el mejor movimiento para el jugador de la computadora y lo hace.
        """

        best_score = float('-inf')
        best_col = -1

        for col in range(7):
            if self.is_valid_move(col):
                self.make_move(col)
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

    def evaluate_board(self):

        """
        Evalúa el tablero actual y devuelve un puntaje.
        """

        score = 0

        for i in range(6):
            for j in range(7):
                if self.board[i][j] == self.turn:
                    # Movimientos que favorecen al jugador
                    score += self.score_position(i, j)

                elif self.board[i][j] == 3 - self.turn:
                    # Movimientos que bloquean al oponente
                    score -= self.score_position(i, j)

        return score

    def score_position(self, row, col):
        
        """
        Evalúa una posición en el tablero y devuelve un puntaje.
        """

        score = 0

        # Verifica horizontalmente
        if col + 3 < 7:
            window = [self.board[row][col + offset] for offset in range(4)]
            score += self.evaluate_window(window)

        # Verifica verticalmente
        if row + 3 < 6:
            window = [self.board[row + offset][col] for offset in range(4)]
            score += self.evaluate_window(window)

        # Verifica diagonalmente (pendiente positiva)
        if col + 3 < 7 and row + 3 < 6:
            window = [self.board[row + offset][col + offset] for offset in range(4)]
            score += self.evaluate_window(window)

        # Verifica diagonalmente (pendiente negativa)
        if col - 3 >= 0 and row + 3 < 6:
            window = [self.board[row + offset][col - offset] for offset in range(4)]
            score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):

        """
        Evalúa una ventana (ventana de 4 piezas) en el tablero.
        """

        player_pieces = window.count(self.turn)
        opponent_pieces = window.count(3 - self.turn)
        empty_spaces = window.count(0)

        if player_pieces == 4:
            return 1000  # El jugador puede ganar
        elif opponent_pieces == 4:
            return -1000  # El oponente puede ganar
        elif player_pieces == 3 and empty_spaces == 1:
            return 5  # El jugador tiene una fuerte oportunidad de ganar
        elif opponent_pieces == 3 and empty_spaces == 1:
            return -5  # El oponente tiene una fuerte oportunidad de ganar
        elif player_pieces == 2 and empty_spaces == 2:
            return 2  # El jugador tiene un movimiento ventajoso
        elif opponent_pieces == 2 and empty_spaces == 2:
            return -2  # El oponente tiene ventaja
        else:
            return 0  # No hay ventaja

    def is_board_full(self):
        return all(self.board[0][col] != 0 for col in range(7))

    def minimax(self, depth, maximizing_player):

        """
        Implementación del algoritmo Minimax.
        """

        if depth == 0 or self.check_winner() or self.is_board_full():
            return self.evaluate_board()

        best_score = float('-inf') if maximizing_player else float('inf')
        best_col = -1

        for col in range(7):
            if self.is_valid_move(col):
                self.make_move(col)
                score = self.minimax(depth - 1, not maximizing_player)
                self.undo_move(col)

                if maximizing_player:
                    best_score = max(best_score, score)
                    if best_score == 1:  # Se sale antes si se encuentra un movimiento ganador
                        return best_score
                else:
                    best_score = min(best_score, score)
                    if best_score == -1:  # Se sale antes si el movimiento es muy malo
                        return best_score

        return best_score
    
    # Alpha-beta pruning
    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        
        """
        Implementación del algoritmo Alpha-Beta pruning.
        """

        if depth == 0 or self.check_winner() or self.is_board_full():
            return self.evaluate_board()

        best_score = float('-inf') if maximizing_player else float('inf')
        best_col = -1

        for col in range(7):
            if self.is_valid_move(col):
                self.make_move(col)
                score = self.alpha_beta(depth - 1, alpha, beta, not maximizing_player)
                self.undo_move(col)

                if maximizing_player:
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
                else:
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break

        return best_score