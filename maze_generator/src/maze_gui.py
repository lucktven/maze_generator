"""
Graphical interface for maze generator
"""

import tkinter as tk
from tkinter import ttk
from .maze_generator import MazeGenerator, MazeCell


class MazeApp:

    def __init__(self, root):
        self.root = root
        self.root.title("maze generator")
        self.maze = None

        self.create_widgets()

    def create_widgets(self):
        """Creating interface elements"""
        # Interface
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(control_frame, text="width:").grid(row=0, column=0, padx=5)
        self.width_var = tk.IntVar(value=21)
        self.width_spin = ttk.Spinbox(control_frame, from_=5, to=101, width=5,
                                      textvariable=self.width_var)
        self.width_spin.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="high:").grid(row=0, column=2, padx=5)
        self.height_var = tk.IntVar(value=15)
        self.height_spin = ttk.Spinbox(control_frame, from_=5, to=101, width=5,
                                       textvariable=self.height_var)
        self.height_spin.grid(row=0, column=3, padx=5)

        self.generate_btn = ttk.Button(control_frame, text="Generate",
                                       command=self.generate_maze)
        self.generate_btn.grid(row=0, column=4, padx=10)

        self.canvas = tk.Canvas(self.root, bg="white", width=500, height=400)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        # Statistic
        self.stats_label = ttk.Label(self.root, text="", padding="5")
        self.stats_label.grid(row=2, column=0)

    def generate_maze(self):
        """Generation of a new maze"""
        width = self.width_var.get()
        height = self.height_var.get()

        generator = MazeGenerator(width, height)
        generator.generate()
        self.maze = generator.maze

        self.draw_maze()
        self.show_stats(generator)

    def draw_maze(self):
        """Displaying a maze on canvas"""
        if not self.maze:
            return

        self.canvas.delete("all")

        cell_size = min(500 // len(self.maze[0]), 400 // len(self.maze))

        colors = {
            MazeCell.WALL: "black",
            MazeCell.ROAD: "white",
            MazeCell.ENTRANCE: "green",
            MazeCell.EXIT: "red",
            MazeCell.TRAP: "yellow",
            MazeCell.TREASURE: "blue"
        }

        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=colors[cell],
                                             outline="gray",
                                             width=1)

                if cell == MazeCell.ENTRANCE:
                    self.canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                            text="E", font=("Arial", 10, "bold"))
                elif cell == MazeCell.EXIT:
                    self.canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                            text="X", font=("Arial", 10, "bold"))
                elif cell == MazeCell.TRAP:
                    self.canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                            text="T", font=("Arial", 8, "bold"))
                elif cell == MazeCell.TREASURE:
                    self.canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                            text="$", font=("Arial", 10, "bold"))

    def show_stats(self, generator):
        """Displaying maze statistics"""
        stats = generator.get_stats()
        stats_text = (f"Size: {stats['width']}x{stats['height']} | "
                      f"Entrance: {stats['entrance']} | Exit: {stats['exit']} | "
                      f"Traps: {stats['trap_cells']} | Treasure: {'Так' if stats['has_treasure'] else 'Ні'}")
        self.stats_label.config(text=stats_text)