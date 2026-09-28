import math
import heapq

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {}
}

def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            cost = sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))
            return path, cost

        for neighbor in hospital_graph[current]:
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    return None, None

def a_star(start, goal):
    g_cost = {start: 0}
    came_from = {start: None}
    frontier = [(heuristic(start, goal), start)]
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current]

        for neighbor, cost in hospital_graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_g + heuristic(neighbor, goal), neighbor))

    return None, None