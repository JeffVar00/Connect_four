from tkinter import *
from tkinter import messagebox

class Gui:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.buttons = []
        self.create_grid()
        self.create_option_menu()

    def create_grid(self):
        for row in range(6):
            row_buttons = []
            for col in range(7):
                b = Button(self.master, text=" ", width=2, command=lambda col=col: self.make_move(col))
                b.grid(row=row, column=col)
                row_buttons.append(b)
            self.buttons.append(row_buttons)

    def make_move(self, col):
        if self.game.player_move(col):
            
            # get the board and update all the buttons
            board = self.game.board
            for i in range(6):
                for j in range(7):
                    if board[i][j] != 0:
                        self.buttons[i][j].config(text=str(board[i][j])[:1])

            if self.game.check_winner():
                messagebox.showinfo("Felicidades!", "El Jugador " + str(self.game.turn) + " ganó! ")
                self.master.quit()

    def create_option_menu(self):
        option_menu = OptionMenu(self.master, StringVar(self.master, "1"), *["Minimax", "AlphaBeta"], command=self.choose_search_algorithm)
        option_menu.grid(row=6, column=3)

    def choose_search_algorithm(self, algorithm):
        self.game.search_algorithm = algorithm