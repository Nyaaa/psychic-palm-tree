import search

test = {'A': {'B': 2, 'C': 5},
        'B': {'A': 2, 'C': 2, 'D': 4},
        'C': {'A': 5, 'B': 2, 'D': 5},
        'D': {'B': 4, 'C': 5, 'E': 2},
        'E': {'C': 5, 'D': 2}
        }

print(search.dijkstra(test, "A", "D"))
print(search.dijkstra_queue(test, "A", "D"))
print(search.a_star(test, 'A', 'D'))
