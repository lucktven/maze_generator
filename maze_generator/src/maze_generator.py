"""
Maze generator using the DFS backtracking algorithm
"""

import random
from collections import deque
from .maze_cell import MazeCell


class MazeGenerator:
    """Class for generating random mazes"""

    def __init__(self, width, height):
        """
        Initialization of the maze generator

        Args:
            width (int)
            height (int)
        """
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = [[MazeCell.WALL for _ in range(self.width)] for _ in range(self.height)]
        self.entrance = None
        self.exit = None

    def generate(self):
        """Generation of a maze with traps and treasures"""
        self._carve_passages(1, 1)

        # Find all available cells on the border
        border_cells = self._find_border_cells()
        if len(border_cells) < 2:
            self._create_border_access()
            border_cells = self._find_border_cells()

        if len(border_cells) >= 2:
            self.entrance, self.exit = random.sample(border_cells, 2)
        else:
            # Backup option
            self.entrance = (1, 0)
            self.exit = (self.height - 2, self.width - 1)

        self.maze[self.entrance[0]][self.entrance[1]] = MazeCell.ENTRANCE
        self.maze[self.exit[0]][self.exit[1]] = MazeCell.EXIT

        solution_path = self._bfs(self.entrance, self.exit)

        # Adding traps
        traps = random.randint(0, 5)
        placed = 0
        while placed < traps:
            r, c = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
            if self.maze[r][c] == MazeCell.ROAD and (r, c) not in solution_path:
                self.maze[r][c] = MazeCell.TRAP
                placed += 1

        # Add treasure
        if random.random() > 0.5 and solution_path and len(solution_path) > 2:
            treasure_cell = random.choice(solution_path[1:-1])
            self.maze[treasure_cell[0]][treasure_cell[1]] = MazeCell.TREASURE

    def _carve_passages(self, cx, cy):
        """DFS backtracking algorithm for path creation"""
        stack = [(cx, cy)]
        self.maze[cx][cy] = MazeCell.ROAD

        while stack:
            cx, cy = stack[-1]
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)
            moved = False

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1:
                    if self.maze[nx][ny] == MazeCell.WALL:
                        self.maze[cx + dx // 2][cy + dy // 2] = MazeCell.ROAD
                        self.maze[nx][ny] = MazeCell.ROAD
                        stack.append((nx, ny))
                        moved = True
                        break

            if not moved:
                stack.pop()

    def _find_border_cells(self):
        """Finds all roads at the edge of the maze"""
        border_cells = []
        for y in range(self.width):
            if self.maze[0][y] == MazeCell.ROAD:
                border_cells.append((0, y))
            if self.maze[self.height - 1][y] == MazeCell.ROAD:
                border_cells.append((self.height - 1, y))
        for x in range(self.height):
            if self.maze[x][0] == MazeCell.ROAD:
                border_cells.append((x, 0))
            if self.maze[x][self.width - 1] == MazeCell.ROAD:
                border_cells.append((x, self.width - 1))
        return border_cells

    def _create_border_access(self):
        """Creates additional passages to the edge of the maze"""
        for y in range(1, self.width - 1, 2):
            if self.maze[1][y] == MazeCell.ROAD:
                self.maze[0][y] = MazeCell.ROAD
            if self.maze[self.height - 2][y] == MazeCell.ROAD:
                self.maze[self.height - 1][y] = MazeCell.ROAD

        for x in range(1, self.height - 1, 2):
            if self.maze[x][1] == MazeCell.ROAD:
                self.maze[x][0] = MazeCell.ROAD
            if self.maze[x][self.width - 2] == MazeCell.ROAD:
                self.maze[x][self.width - 1] = MazeCell.ROAD

    def _bfs(self, start, goal):
        """Finding a path from the entrance to the exit using BFS"""
        queue = deque([start])
        parents = {start: None}
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if self.maze[nx][ny] in [MazeCell.ROAD, MazeCell.EXIT] and (nx, ny) not in parents:
                        parents[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        if goal not in parents:
            return []

        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parents.get(cur)
        return path[::-1]

    def to_ascii(self):
        """Converts a maze into ASCII representation"""
        symbols = {
            MazeCell.WALL: '█',
            MazeCell.ROAD: ' ',
            MazeCell.ENTRANCE: 'E',
            MazeCell.EXIT: 'X',
            MazeCell.TRAP: 'T',
            MazeCell.TREASURE: '$'
        }

        lines = []
        for row in self.maze:
            lines.append(''.join(symbols[cell] for cell in row))
        return '\n'.join(lines)

    def get_stats(self):
        """Returns maze statistics"""
        stats = {
            'width': self.width,
            'height': self.height,
            'entrance': self.entrance,
            'exit': self.exit,
            'total_cells': self.width * self.height,
            'road_cells': sum(row.count(MazeCell.ROAD) for row in self.maze),
            'trap_cells': sum(row.count(MazeCell.TRAP) for row in self.maze),
            'has_treasure': any(MazeCell.TREASURE in row for row in self.maze)
        }
        return stats