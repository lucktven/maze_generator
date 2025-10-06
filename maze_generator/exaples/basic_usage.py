"""
Example of basic use of the maze generator
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.maze_generator import MazeGenerator


def main():
    # Creating and generating a maze
    generator = MazeGenerator(21, 15)
    generator.generate()

    # ASCII output
    print("ASCII representation of a maze:")
    print(generator.to_ascii())

    # Statistic
    stats = generator.get_stats()
    print("\nMaze statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()