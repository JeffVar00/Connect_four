import tkinter as tk
from tkinter import OptionMenu, StringVar, messagebox

class Gui:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.canvas = None
        self.create_grid()
        self.create_option_menu()
        self.selected_column_indicator = None

    def create_grid(self):
        self.master.geometry("600x500")  # Set the initial window size
        self.canvas = tk.Canvas(self.master, width=400, height=350)
        self.canvas.grid(row=0, column=0, columnspan=7, rowspan=6)

        for col in range(7):
            for row in range(6):
                x1 = col * 50 + 10
                y1 = row * 50 + 10
                x2 = x1 + 40
                y2 = y1 + 40
                # Center the circles by adding padding
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                self.canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, fill="white", outline="black")

            # Create a button for each column with padding
            column_button = tk.Button(self.master, text="Drop", command=lambda col=col: self.make_move(col))
            column_button.grid(row=6, column=col, padx=10)

        # Create the option menu below the buttons
        option_menu = OptionMenu(self.master, StringVar(self.master, "Minimax"), *["Minimax", "AlphaBeta"], command=self.choose_search_algorithm)
        option_menu.grid(row=7, column=0, columnspan=7)

    def make_move(self, col):
        if self.game.player_move(col):

            board = self.game.board

            # print board
            for row in range(6):
                print(board[row])

            for row in range(6):
                for col in range(7):
                    if board[row][col] == 0:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        # Center the circles when updating
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        self.canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, fill="white", outline="black")
                    elif board[row][col] == 1:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        self.canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, fill="blue", outline="black")
                    elif board[row][col] == 2:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        self.canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, fill="red", outline="black")

            if self.game.check_winner():
                messagebox.showinfo("Congratulations!", "Player " + str(self.game.turn) + " won!")
                self.master.quit()

    def create_option_menu(self):
        pass

    def choose_search_algorithm(self, algorithm):
        self.game.search_algorithm = algorithm