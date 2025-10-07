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

        # Find solution path without traps first
        solution_path = self._bfs(self.entrance, self.exit)

        # Adding traps safely
        self._place_traps_safely(solution_path)

        # Add treasure safely
        self._place_treasure_safely(solution_path)

        # Final validation
        if not self.validate_maze():
            # Regenerate if validation fails
            self._regenerate_until_valid()

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

    def _find_safe_path(self, start, goal):
        """BFS with trap safety check - finds path where player won't die from traps"""
        # Queue: (position, consecutive_traps)
        queue = deque([(start, 0)])
        parents = {(start, 0): None}

        while queue:
            (x, y), trap_count = queue.popleft()

            if (x, y) == goal:
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    cell_type = self.maze[nx][ny]
                    new_trap_count = trap_count

                    if cell_type == MazeCell.TRAP:
                        new_trap_count = trap_count + 1
                        if new_trap_count >= 3:
                            continue  # Skip this path - player would die
                    elif cell_type in [MazeCell.ROAD, MazeCell.EXIT, MazeCell.TREASURE]:
                        new_trap_count = 0  # Reset trap counter
                    else:
                        continue  # Skip walls and other invalid cells

                    state = ((nx, ny), new_trap_count)
                    if state not in parents:
                        parents[state] = ((x, y), trap_count)
                        queue.append(state)

        # Reconstruct path
        path = []
        # Find any safe state that reached the goal
        for (pos, traps), parent in parents.items():
            if pos == goal:
                current_state = (pos, traps)
                while current_state is not None:
                    path.append(current_state[0])  # Extract position only
                    current_state = parents.get(current_state)
                return path[::-1]

        return []

    def _place_traps_safely(self, solution_path):
        """Place traps ensuring there's still a safe path"""
        traps = random.randint(0, 5)
        placed = 0
        max_attempts = 50

        road_cells = []
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == MazeCell.ROAD and (i, j) not in solution_path:
                    road_cells.append((i, j))

        random.shuffle(road_cells)

        for cell in road_cells:
            if placed >= traps:
                break

            r, c = cell
            # Temporarily place trap
            original_cell = self.maze[r][c]
            self.maze[r][c] = MazeCell.TRAP

            # Check if safe path still exists
            safe_path = self._find_safe_path(self.entrance, self.exit)
            if safe_path:
                placed += 1
            else:
                # Revert if no safe path
                self.maze[r][c] = original_cell

    def _place_treasure_safely(self, solution_path):
        """Place treasure ensuring it's reachable"""
        if random.random() > 0.5 and solution_path and len(solution_path) > 2:
            # Try to place treasure on safe path
            safe_path = self._find_safe_path(self.entrance, self.exit)
            if safe_path and len(safe_path) > 2:
                treasure_cell = random.choice(safe_path[1:-1])
                # Don't place on entrance/exit
                if treasure_cell != self.entrance and treasure_cell != self.exit:
                    self.maze[treasure_cell[0]][treasure_cell[1]] = MazeCell.TREASURE

    def validate_maze(self):
        """Validate that maze meets all requirements"""
        # Check if there's a path from entrance to exit
        basic_path = self._bfs(self.entrance, self.exit)
        if not basic_path:
            return False

        # Check if there's a safe path (player won't die from traps)
        safe_path = self._find_safe_path(self.entrance, self.exit)
        if not safe_path:
            return False

        # Check if treasure is reachable (if present)
        treasure_pos = None
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == MazeCell.TREASURE:
                    treasure_pos = (i, j)
                    break
            if treasure_pos:
                break

        if treasure_pos:
            treasure_path = self._find_safe_path(self.entrance, treasure_pos)
            if not treasure_path:
                return False

        return True

    def _regenerate_until_valid(self, max_attempts=10):
        """Regenerate maze until it meets all requirements"""
        for attempt in range(max_attempts):
            # Reset maze
            self.maze = [[MazeCell.WALL for _ in range(self.width)] for _ in range(self.height)]
            self.entrance = None
            self.exit = None

            # Regenerate
            self._carve_passages(1, 1)

            # Find border cells for entrance/exit
            border_cells = self._find_border_cells()
            if len(border_cells) >= 2:
                self.entrance, self.exit = random.sample(border_cells, 2)
            else:
                self.entrance = (1, 0)
                self.exit = (self.height - 2, self.width - 1)

            self.maze[self.entrance[0]][self.entrance[1]] = MazeCell.ENTRANCE
            self.maze[self.exit[0]][self.exit[1]] = MazeCell.EXIT

            solution_path = self._bfs(self.entrance, self.exit)
            self._place_traps_safely(solution_path)
            self._place_treasure_safely(solution_path)

            if self.validate_maze():
                return True

        return False

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
        safe_path = self._find_safe_path(self.entrance, self.exit)
        has_safe_path = bool(safe_path)

        stats = {
            'width': self.width,
            'height': self.height,
            'entrance': self.entrance,
            'exit': self.exit,
            'total_cells': self.width * self.height,
            'road_cells': sum(row.count(MazeCell.ROAD) for row in self.maze),
            'trap_cells': sum(row.count(MazeCell.TRAP) for row in self.maze),
            'has_treasure': any(MazeCell.TREASURE in row for row in self.maze),
            'has_safe_path': has_safe_path,
            'safe_path_length': len(safe_path) if safe_path else 0
        }
        return stats