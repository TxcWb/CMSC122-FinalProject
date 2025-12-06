# Algorithm Implementations
# This file contains implementations of pathfinding and MST algorithms

# Dijkstra's Algorithm
# - Find shortest path between two vertices in a weighted graph
# - Use priority queue for efficient implementation
# - Parameters: graph, source vertex, destination vertex
# - Return: shortest path as list of vertices, total distance

# dijkstra function
# - Initialize distances to infinity for all vertices except source
# - Initialize priority queue with source vertex (distance 0)
# - Track previous vertices to reconstruct path
# - Main loop:
#   - Extract vertex with minimum distance from queue
#   - For each neighbor, calculate tentative distance
#   - Update distance if shorter path found
#   - Add/update neighbor in priority queue
# - Reconstruct path from source to destination
# - Return path and total distance

# Kruskal's Algorithm (MST)
# - Find Minimum Spanning Tree using edge-based approach
# - Use Union-Find (Disjoint Set) data structure
# - Parameters: graph
# - Return: list of edges in MST, total weight

# Union-Find helper class
# - parent dictionary for tracking set representatives
# - rank dictionary for union by rank optimization
# - find method with path compression
# - union method to merge sets

# kruskal function
# - Get all edges from graph
# - Sort edges by weight in ascending order
# - Initialize Union-Find structure for all vertices
# - For each edge (in sorted order):
#   - Check if adding edge creates cycle (using find)
#   - If no cycle, add edge to MST (using union)
# - Return MST edges and total weight

# Prim's Algorithm (MST)
# - Find Minimum Spanning Tree using vertex-based approach
# - Use priority queue for efficient implementation
# - Parameters: graph, starting vertex
# - Return: list of edges in MST, total weight

# prim function
# - Initialize visited set with starting vertex
# - Initialize priority queue with edges from starting vertex
# - Initialize MST edge list
# - While not all vertices visited:
#   - Extract minimum weight edge from queue
#   - If edge leads to unvisited vertex:
#     - Add edge to MST
#     - Mark vertex as visited
#     - Add all edges from new vertex to queue
# - Return MST edges and total weight
