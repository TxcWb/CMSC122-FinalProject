# Graph Implementation
# This file contains the graph data structure for representing the campus map

# Graph class
# - Uses adjacency list representation
# - Stores vertices (buildings/locations) and edges (paths with weights/distances)

# Constructor
# - Initialize empty adjacency list
# - Set up data structures for vertices and edges

# add_vertex method
# - Add a new vertex (building/location) to the graph
# - Check for duplicates

# add_edge method
# - Add an edge between two vertices with a weight (distance)
# - Handle undirected edges (bidirectional paths)
# - Validate vertices exist before adding edge

# get_neighbors method
# - Return all adjacent vertices for a given vertex
# - Include edge weights

# get_vertices method
# - Return list of all vertices in the graph

# get_edges method
# - Return list of all edges in the graph
# - Format: (vertex1, vertex2, weight)

# has_vertex method
# - Check if a vertex exists in the graph

# has_edge method
# - Check if an edge exists between two vertices

# get_edge_weight method
# - Return the weight of an edge between two vertices
# - Return None if edge doesn't exist

# display_graph method
# - Print visual representation of the graph
# - Show all vertices and their connections with weights
