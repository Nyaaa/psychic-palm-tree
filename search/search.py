import heapq
from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        total_time = end_time - start_time
        print(f'Function {func.__name__} took {total_time} ns')
        return result
    return timeit_wrapper


@timeit
def dijkstra(graph: dict, start, stop):
    """Basic Dijkstra"""
    distances = {vertex: float('infinity') for vertex in graph}
    traversed = {vertex: False for vertex in graph}
    parents = {vertex: None for vertex in graph}
    distances[start] = 0
    pointer = stop
    path = []

    for _ in range(len(distances)):
        shortest = min([k for k in traversed.keys() if not traversed[k]], key=lambda x: distances[x])

        for vertex in graph[shortest].keys():
            if distances[vertex] > distances[shortest] + graph[shortest][vertex]:
                distances[vertex] = distances[shortest] + graph[shortest][vertex]
                parents[vertex] = shortest
        traversed[shortest] = True

    while pointer is not None:
        path.append(pointer)
        pointer = parents[pointer]

    # print(distances)
    path.reverse()
    return path


@timeit
def dijkstra_queue(graph: dict, start, stop):
    """Dijkstra with priority queue"""
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    parents = {vertex: None for vertex in graph}
    pointer = stop
    path = []

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
                parents[neighbour] = current_vertex

    while pointer is not None:
        path.append(pointer)
        pointer = parents[pointer]

    # print(distances)
    path.reverse()
    return path


@timeit
def a_star(graph, start, stop):
    """A*"""
    open_list = set(start)
    closed_list = set()
    distances = {start: 0}
    parents = {start: start}
    heuristics = {vertex: 1 for vertex in graph}

    while len(open_list) > 0:
        n = None

        for vertex in open_list:
            if n is None or distances[vertex] + heuristics[vertex] < distances[n] + heuristics[n]:
                n = vertex

        if n is None:
            print('Path does not exist!')
            return None

        if n == stop:
            path = []

            while parents[n] != n:
                path.append(n)
                n = parents[n]

            path.append(start)
            path.reverse()
            # print(distances)
            return path

        for m, weight in graph[n].items():
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                distances[m] = distances[n] + weight
            else:
                if distances[m] > distances[n] + weight:
                    distances[m] = distances[n] + weight
                    parents[m] = n

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        open_list.remove(n)
        closed_list.add(n)

    print('Path does not exist!')
    return None