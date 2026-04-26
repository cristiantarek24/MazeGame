from collections import deque
import heapq


# Explores the grid level by level using a queue.
# Guarantees the shortest path from start to goal.
def bfs(grid, start, goal):
    queue = deque([start])
    visited = set([start])
    parent = {}
    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(parent, start, goal)
        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return None


# Explores as deep as possible along each branch before backtracking.
# Does not guarantee the shortest path.
def dfs(grid, start, goal):
    stack = [start]
    visited = set([start])
    parent = {}
    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(parent, start, goal)
        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    return None


# Uses a cost function (distance so far + heuristic estimate) to find
# the shortest path efficiently by always expanding the most promising node.
def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_cost = {start: 0}
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        for neighbor in get_neighbors(grid, current):
            tentative_g = g_cost[current] + 1
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_cost, neighbor))
    return None


# Estimates the remaining distance between two grid cells
# using Manhattan distance (no diagonals).
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Returns all walkable adjacent cells (up, down, left, right)
# for a given node, staying within grid bounds.
def get_neighbors(grid, node):
    rows, cols = len(grid), len(grid[0])
    x, y = node
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))
    return neighbors


# Traces back through the parent map from goal to start
# and returns the path in forward order.
def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


# Converts the maze grid (list of strings with X/P/E/ )
# into a 2D list of 1s (walls) and 0s (open cells) for the algorithms.
def maze_to_grid(level_grid):
    return [[1 if ch == "X" else 0 for ch in row] for row in level_grid]


# Scans the grid strings to locate the player start (P)
# and the exit goal (E), returning both as (row, col) tuples.
def find_start_goal(level_grid):
    start = goal = None
    for r, row in enumerate(level_grid):
        for c, ch in enumerate(row):
            if ch == "P":
                start = (r, c)
            elif ch == "E":
                goal = (r, c)
    return start, goal


# Converts a grid (row, col) position into turtle screen coordinates (x, y).
def grid_to_screen(row, col, cell_size=24):
    sx = -288 + col * cell_size
    sy = 288 - row * cell_size
    return sx, sy