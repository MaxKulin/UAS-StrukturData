# dijkstra.py
# Implementasi algoritma Dijkstra untuk mencari rute terpendek
# Input  : graph (adjacency list), node asal, node tujuan
# Output : jarak terpendek + jalur yang dilalui

import heapq
from core.graph import GRAPH

def get_step_by_step(path, distances_at_each_step=None):
    steps = []
    for i in range(len(path) - 1):
        steps.append({
            "from": path[i],
            "to"  : path[i + 1],
        })
    return steps

def dijkstra(start, end):
    # Jarak awal semua node = tak terhingga, kecuali node start = 0
    distances = {node: float('inf') for node in GRAPH}
    distances[start] = 0

    # Menyimpan jalur: dari mana kita sampai ke node ini
    previous = {node: None for node in GRAPH}

    # Priority queue: (jarak_sementara, node)
    queue = [(0, start)]

    visited = set()

    while queue:
        current_dist, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Kalau sudah sampai tujuan, hentikan
        if current_node == end:
            break

        for neighbor, weight in GRAPH[current_node].items():
            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(queue, (new_dist, neighbor))

    # Rekonstruksi jalur dari end ke start
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    # Kalau jalur tidak ditemukan
    if path[0] != start:
        return None, float('inf')

    return path, distances[end]



