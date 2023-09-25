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

        # Create a frame to center the grid
        frame = tk.Frame(self.master)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Fixed button width and uniform padding
        button_width = 8
        button_padding_x = 5
        button_padding_y = 5

        self.canvas = tk.Canvas(frame, width=400, height=350)
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
                
            # Create a button for each column with fixed width and padding
            column_button = tk.Button(frame, text=f"{col+1}", width=button_width, command=lambda col=col: self.make_move(col))
            column_button.grid(row=6, column=col, padx=button_padding_x, pady=button_padding_y)

        # Create the option menu below the buttons
        option_menu = OptionMenu(frame, StringVar(self.master, "Minimax"), *["Minimax", "AlphaBeta"], command=self.choose_search_algorithm)
        option_menu.grid(row=7, column=0, columnspan=7, pady=button_padding_y)

        # Create a text field called depth to write the depht of the search and validate its always a number and default value 4
        depth = StringVar(self.master, "4")
        depth.trace("w", lambda name, index, mode, depth=depth: self.validate_depth(depth))
        depth_entry = tk.Entry(frame, textvariable=depth, width=button_width)
        depth_entry.grid(row=8, column=0, columnspan=7, pady=button_padding_y)


    def validate_depth(self, depth):
        if not depth.get().isdigit():
            depth.set("0")

    def make_move(self, col):
        # update depth in game from the depth entry field
        self.game.depth = int(self.master.children['!frame'].children['!entry'].get())

        if self.game.player_move(col):

            board = self.game.board

            for row in range(6):
                for col in range(7):
                    if board[row][col] == 1:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        # Make circles slightly smaller
                        radius = 15
                        self.canvas.create_oval(x_center - radius, y_center - radius, x_center + radius, y_center + radius, fill="moccasin", outline="black")
                    elif board[row][col] == 2:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        # Make circles slightly smaller
                        radius = 15
                        self.canvas.create_oval(x_center - radius, y_center - radius, x_center + radius, y_center + radius, fill="lightblue", outline="black")


            if self.game.check_winner():
                messagebox.showinfo("Congratulations!", "Player " + str(self.game.turn) + " won!")

                # reset the canvas and the board
                self.canvas.delete("all")
                self.create_grid()
                self.game.reset()

    def create_option_menu(self):
        pass

    def choose_search_algorithm(self, algorithm):
        self.game.search_algorithm = algorithm