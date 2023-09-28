import tkinter as tk
from tkinter import OptionMenu, StringVar, messagebox

class Gui:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.canvas = None

        self.master.geometry("600x500")  # Establece el tamaño inicial de la ventana

        # Crea un marco para centrar la cuadrícula
        self.frame = tk.Frame(self.master)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_grid(self.frame)
        self.create_options(self.frame)
        self.selected_column_indicator = None

    def create_grid(self, frame):
        """
        Crea la cuadrícula del juego con círculos y botones para las columnas.
        También agrega un campo de entrada para especificar la profundidad de búsqueda.
        """

        # Ancho fijo de botones y relleno uniforme
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
                # Centra los círculos agregando relleno
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                self.canvas.create_oval(x_center - 20, y_center - 20, x_center + 20, y_center + 20, fill="white", outline="black")
                
            # Crea un botón para cada columna con ancho y relleno fijos
            column_button = tk.Button(frame, text=f"{col+1}", width=button_width, command=lambda col=col: self.make_move(col))
            column_button.grid(row=6, column=col, padx=button_padding_x, pady=button_padding_y)

    def create_options(self, frame):
        
        # Ancho fijo de botones y relleno uniforme
        button_width = 8
        button_padding_x = 5
        button_padding_y = 5
        
        # Crea el menú de opciones debajo de los botones
        option_menu = OptionMenu(frame, StringVar(self.master, "Minimax"), *["Minimax", "AlphaBeta"], command=self.choose_search_algorithm)
        option_menu.grid(row=7, column=0, columnspan=7, pady=button_padding_y)

        # Crea un campo de texto llamado "depth" numerico no modificable con opcion para subir o bajar el valor (de dos en dos)
        depth = StringVar(self.master, "6")
        depth.trace("w", lambda depth=depth: self.validate_depth(depth))

        depth_entry = tk.Entry(frame, textvariable=depth, width=button_width, state="readonly")
        depth_entry.grid(row=8, column=1, columnspan=5, pady=button_padding_y)

        decrease_button = tk.Button(frame, text="-", width=button_padding_x, command=lambda: self.change_depth(-2, depth))
        decrease_button.grid(row=8, column=0, columnspan=5, pady=button_padding_y)  # Colocado en la columna 0

        increase_button = tk.Button(frame, text="+", width=button_padding_x, command=lambda: self.change_depth(2, depth))
        increase_button.grid(row=8, column=2, columnspan=5, pady=button_padding_y)  # Colocado en la columna 2

    # Agrega esta función para cambiar la profundidad
    def change_depth(self, increment, depth):
        current_depth = int(depth.get())
        new_depth = current_depth + increment
        if new_depth >= 0:  # Asegúrate de que no sea negativo
            depth.set(new_depth)


    def validate_depth(self, depth):
        """
        Valida que el valor en el campo "depth" sea un número.
        """
        if not depth.get().isdigit():
            depth.set("0")

    def make_move(self, col):
        """
        Maneja los movimientos del jugador y actualiza la interfaz gráfica.
        """
        # Actualiza la profundidad en el juego desde el campo de entrada "depth"
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
                        radio = 15
                        self.canvas.create_oval(x_center - radio, y_center - radio, x_center + radio, y_center + radio, fill="moccasin", outline="black")
                    elif board[row][col] == 2:
                        x1 = col * 50 + 10
                        y1 = row * 50 + 10
                        x2 = x1 + 40
                        y2 = y1 + 40
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        radio = 15
                        self.canvas.create_oval(x_center - radio, y_center - radio, x_center + radio, y_center + radio, fill="lightblue", outline="black")


            if self.game.check_winner():
                messagebox.showinfo("¡Felicidades!", "El jugador " + str(self.game.turn) + " ganó!")

                # Reinicia el lienzo y el tablero excepto la opción
                self.canvas.delete("all")
                self.create_grid(self.frame)
                self.game.reset()


    def choose_search_algorithm(self, algorithm):
        """
        Permite al jugador elegir el algoritmo de búsqueda.
        """
        self.game.search_algorithm = algorithm