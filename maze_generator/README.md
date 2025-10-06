
# Maze Generator

A robust Python library for generating perfect mazes using recursive backtracking algorithm with guaranteed solvability and customizable features.

## Features

- DFS backtracking algorithm ensuring single solution path
- Walls, paths, entrance, exit, traps, and treasures
- Always provides a valid path from entrance to exit
- Built-in Tkinter-based visualization
- Customizable maze dimensions and element distribution

## Installation

### Requirements
- Python 3.8 or higher
- Tkinter 

### Quick Install
```
git clone https://github.com/lucktven/maze_generator.git
```

## Quick Start

### Graphical Interface
```
python main.py
```

## Project Structure

```
maze_generator/
├── src/
│   ├── maze_cell.py        # Cell type definitions
│   ├── maze_generator.py   # Core generation logic
│   └── maze_gui.py         # Graphical interface
├── examples/               # Usage examples
├── tests/                  # Test suite
├── main.py                 # Application entry point
└── README.md
```

## API Reference

### MazeGenerator

#### Constructor
```
MazeGenerator(width: int, height: int)
```
Creates a new maze generator instance. Dimensions are automatically adjusted to odd numbers.

#### Methods

- `generate()`: Generates a new maze with random configuration
- `to_ascii() -> str`: Returns ASCII representation of the maze
- `get_stats() -> dict`: Returns maze statistics and metadata


## Interface Object Notation

### Graphical Interface (GUI)

| Symbol      | Color     | Description                                       |
|-------------|-----------|---------------------------------------------------|
| **E**       | 🟩 Green  | Maze entrance                                     |
| **X**       | 🟥 Red    | Maze exit                                         |
| **T**       | 🟨 Yellow | Trap - passable, but 3 such cells kill the player |
| **$**       | 🟦 Blue   | Treasure - collectible item                       |
| **█**       | ⬛ Black   | Wall - impassable barrier                         |
| **[space]** | ⬜ White   | Road - passable path                              |

### Text Output (ASCII)

| Symbol      | Description                 |
|-------------|-----------------------------|
| `█`         | Wall - impassable barrier   |
| ` ` (space) | Road - passable path        |
| `E`         | Maze entrance               |
| `X`         | Maze exit                   |
| `T`         | Trap - hazardous cell       |
| `$`         | Treasure - collectible item |


### MazeCell Enum
| Constant   | Value | Description                     |
|------------|-------|---------------------------------|
| `WALL`     | 0     | Impermeable barrier             |
| `ROAD`     | 1     | Passable path                   |
| `ENTRANCE` | 2     | Maze entry point                |
| `EXIT`     | 3     | Maze exit point                 |
| `TRAP`     | 4     | Hazardous cell (0-5 per maze)   |
| `TREASURE` | 5     | Collectible item (0-1 per maze) |

## Algorithm

The generator uses a **Depth-First Search with backtracking** approach:

1. Grid filled with walls
2. Recursive depth-first traversal creating passages
3. Entrance, exit, traps, and treasures are strategically placed
4. BFS ensures solvability and validates placement constraints

### Complexity
- O(n²) for maze storage



