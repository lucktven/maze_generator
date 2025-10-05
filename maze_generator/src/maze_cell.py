"""
Identifying the types of cells in the labyrinth
"""

from enum import Enum

class MazeCell(int, Enum):
    """Types of maze cells"""
    WALL = 0
    ROAD = 1
    ENTRANCE = 2
    EXIT = 3
    TRAP = 4
    TREASURE = 5