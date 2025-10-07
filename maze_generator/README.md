# Maze Generator

A robust Python library for generating perfect mazes using recursive backtracking algorithm with guaranteed solvability and trap safety.

## Features

- **DFS backtracking algorithm** ensuring single solution path
- **Complete safety validation** - guaranteed path without deadly trap sequences
- **Configurable elements**: Walls, paths, entrance, exit, traps (0-5), and treasures (0-1)
- **Always provides valid path** from entrance to exit that won't kill the player
- **Built-in Tkinter-based visualization** with color coding
- **Customizable maze dimensions** and element distribution

## Installation

### Requirements
- Python 3.8 or higher

### Quick Install
```
git clone https://github.com/lucktven/maze_generator.git
cd maze_generator
```

## Quick Start

### Graphical Interface
```
python main.py
```

### Command Line Usage
```
python cli_example.py [width] [height]
```

### Basic Python Usage
```
from src.maze_generator import MazeGenerator

# Create 21x15 maze
generator = MazeGenerator(21, 15)
generator.generate()

# ASCII representation
print(generator.to_ascii())

# Get statistics
stats = generator.get_stats()
```

## Project Structure

```
maze_generator/
├── src/
│   ├── maze_cell.py        # Cell type definitions and enum
│   ├── maze_generator.py   # Core generation logic with safety checks
│   └── maze_gui.py         # Graphical interface
├── examples/
│   ├── basic_usage.py      # Basic API usage example
│   └── cli_example.py      # Command line interface example
├── tests/
│   └── test_maze_generator.py  # Comprehensive test suite
├── main.py                 # Application entry point
└── README.md
```

## API Reference

### MazeGenerator Class

#### Constructor
```
MazeGenerator(width: int, height: int)
```
Creates a new maze generator instance. Dimensions are automatically adjusted to odd numbers for proper maze generation.

#### Key Methods

- `generate()`: Generates a new maze with random configuration and safety validation
- `to_ascii() -> str`: Returns ASCII representation of the maze
- `get_stats() -> dict`: Returns maze statistics and metadata
- `validate_maze() -> bool`: Validates all maze conditions are met

#### Safety Guarantees

- **Path existence**: Always at least one path from entrance to exit
- **Trap safety**: No path contains 3+ consecutive traps that would kill player
- **Treasure reachability**: If present, treasure is always reachable via safe path
- **Validation**: Automatic regeneration if conditions aren't met

## Interface Notation

### Graphical Interface (GUI)

| Symbol      | Color     | Description                                       |
|-------------|-----------|---------------------------------------------------|
| **E**       | 🟩 Green  | Maze entrance                                     |
| **X**       | 🟥 Red    | Maze exit                                         |
| **T**       | 🟨 Yellow | Trap - passable, but 3 consecutive cells kill player |
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
| Constant   | Value | Description                     | Constraints           |
|------------|-------|---------------------------------|----------------------|
| `WALL`     | 0     | Impermeable barrier             | -                    |
| `ROAD`     | 1     | Passable path                   | -                    |
| `ENTRANCE` | 2     | Maze entry point                | Must be on outer side|
| `EXIT`     | 3     | Maze exit point                 | Must be on outer side|
| `TRAP`     | 4     | Hazardous cell                  | 0-5 per maze, safe path guaranteed |
| `TREASURE` | 5     | Collectible item                | 0-1 per maze, always reachable |

## Algorithm & Complexity

### Core Algorithm
The generator uses a **Depth-First Search with backtracking** approach:

1. **Initialization**: Grid filled with walls
2. **Path carving**: Recursive DFS creating passages while maintaining connectivity
3. **Entrance/exit placement**: Strategic placement on maze borders
4. **Safe trap placement**: Traps placed ensuring no deadly sequences (3+ consecutive)
5. **Treasure placement**: Guaranteed reachability on safe path
6. **Validation**: BFS with trap counting ensures all safety conditions

### Safety Features
- **Trap sequence validation**: Modified BFS tracks consecutive traps
- **Automatic regeneration**: If safety conditions fail, maze regenerates
- **Path verification**: Multiple validation steps ensure compliance

### Complexity Analysis
- **Time Complexity**: O(n²) for maze generation and validation
- **Space Complexity**: O(n²) for maze storage
- **Validation**: O(n²) for BFS safety checks

## Testing

Run the comprehensive test suite:
```
python tests/test_maze_generator.py
```






