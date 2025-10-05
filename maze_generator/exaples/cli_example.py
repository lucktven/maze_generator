"""
Example of use via command line
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.maze_generator import MazeGenerator


def main():
    if len(sys.argv) == 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    else:
        width = 21
        height = 15

    generator = MazeGenerator(width, height)
    generator.generate()

    print(f"Лабіринт {width}x{height}:")
    print(generator.to_ascii())


if __name__ == "__main__":
    main()