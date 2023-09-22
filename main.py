from tkinter import *
from src.models.connect_four import ConnectFour
from src.interfaces.main_view import Gui

def main():
    root = Tk()
    game = ConnectFour()
    gui = Gui(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()

