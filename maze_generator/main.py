"""
Main file for launching the graphical interface
"""

import tkinter as tk
from src.maze_gui import MazeApp

def main():
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()