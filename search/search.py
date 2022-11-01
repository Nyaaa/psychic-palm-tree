import heapq


def dijkstra(graph: dict, start, stop):
    """Basic Dijkstra"""
    distances = {vertex: float('infinity') for vertex in graph}
    traversed = {vertex: False for vertex in graph}
    backtrack = {vertex: None for vertex in graph}
    distances[start] = 0
    pointer = stop
    path = []

    for _ in range(len(distances)):
        shortest = min([k for k in traversed.keys() if not traversed[k]], key=lambda x: distances[x])

        for vertex in graph[shortest].keys():
            if distances[vertex] > distances[shortest] + graph[shortest][vertex]:
                distances[vertex] = distances[shortest] + graph[shortest][vertex]
                backtrack[vertex] = shortest
        traversed[shortest] = True

    while pointer is not None:
        path.append(pointer)
        pointer = backtrack[pointer]

    print(distances)
    path.reverse()
    return path


def dijkstra_pq(graph: dict, start):
    """Dijkstra with priority queue"""
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    priority_queue = [(0, start)]
    while len(priority_queue) > 0:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbour, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(priority_queue, (distance, neighbour))

    return distances
