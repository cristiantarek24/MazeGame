from collections import deque
import heapq

# BFS

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



# DFS

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



# A*

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



# Heuristic (A*)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



# Neighbors

def get_neighbors(grid, node):
    rows, cols = len(grid), len(grid[0])
    x, y = node

    directions= [
        (0, 1),   # right
        (0, -1),  # left
        (1, 0),   # down
        (-1, 0)   # up
    ]

    neighbors= []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == 0:  # 0 = path, 1 = wall
                neighbors.append((nx, ny))

    return neighbors



# Path Reconstruction

def reconstruct_path(parent, start, goal):
    path= []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path

