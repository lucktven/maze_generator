"""
Tests for generating mazes
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.maze_generator import MazeGenerator, MazeCell


def test_maze_initialization():
    """Maze initialization test"""
    generator = MazeGenerator(15, 11)
    assert generator.width == 15
    assert generator.height == 11
    assert len(generator.maze) == 11
    assert len(generator.maze[0]) == 15


def test_maze_generation():
    """Maze generation test"""
    generator = MazeGenerator(15, 11)
    generator.generate()

    # Verification that the maze has been generated
    assert generator.entrance is not None
    assert generator.exit is not None

    # Checking that the input and output are in their places
    assert generator.maze[generator.entrance[0]][generator.entrance[1]] == MazeCell.ENTRANCE
    assert generator.maze[generator.exit[0]][generator.exit[1]] == MazeCell.EXIT


def test_ascii_output():
    """ASCII output test"""
    generator = MazeGenerator(5, 5)
    generator.generate()
    ascii_output = generator.to_ascii()
    assert isinstance(ascii_output, str)
    assert len(ascii_output) > 0


if __name__ == "__main__":
    test_maze_initialization()
    test_maze_generation()
    test_ascii_output()
    print("All tests passed successfully!")