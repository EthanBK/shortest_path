nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
distances = {
    'B': {'A': 2, 'c': 3},
    'A': {'B': 2, 'D': 5, 'E': 6},
    'D': {'A': 5, 'C': 4, 'F': 3},
    'G': {'E': 3, 'F': 4},
    'C': {'B': 3, 'D': 4, 'E': 1},
    'E': {'A': 6, 'F': 2, 'G': 3},
    'F': {'D': 3, 'E': 2, 'G': 4}}

unvisited = {node: None for node in nodes}  # using None as +inf
visited = {}
current = 'B'
currentDistance = 0
unvisited[current] = currentDistance

while True:
    for neighbour, distance in distances[current].items():
        if neighbour not in unvisited:
            continue
        newDistance = currentDistance + distance
        if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
            unvisited[neighbour] = newDistance
    visited[current] = currentDistance
    del unvisited[current]
    if not unvisited:
        break
    candidates = [node for node in unvisited.items() if node[1]]
    current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]

print(visited)
