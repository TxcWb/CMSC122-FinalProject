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

# dijkstra
import heapq
import math
from typing import Dict, List, Tuple, Optional, Set
# distance calc using haversine distance using args coord1 and coord2 to ret distance in meters
def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # hversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371000
    return c * r


#weighted graph building in geojson using multilinestring pathways where bldgs are positioned on the pathway coorsd

def build_graph_from_geojson(geojson_data: dict) -> Tuple[Dict[str, List[Tuple[str, float]]], Dict[str, Tuple[float, float]]]:
    # extract all bldgs and their coordds
    buildings = {}
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            name = feature['properties'].get('Name', '')
            if name and name != 'Campus Pathways':
                coords = feature['geometry']['coordinates']
                buildings[name] = (coords[0], coords[1])  # (lon, lat)
    #idenitfy bldg name of the node
    def get_building_at_coord(lon: float, lat: float) -> Optional[str]:
        TOLERANCE = 0.0000001  # Very small tolerance for coordinate matching
        for building_name, (b_lon, b_lat) in buildings.items():
            if abs(lon - b_lon) < TOLERANCE and abs(lat - b_lat) < TOLERANCE:
                return building_name
        return None
    # fetch and create node id if none
    coord_to_node = {}
    node_counter = 0
    def get_node_id(lon: float, lat: float) -> str:
        nonlocal node_counter
        # bldg checker if theres bldg in this coord
        building_name = get_building_at_coord(lon, lat)
        if building_name:
            return building_name
        # round coords
        coord_key = (round(lon, 8), round(lat, 8))
        # check if there's created node for this already
        if coord_key in coord_to_node:
            return coord_to_node[coord_key]
        node_id = f"node_{node_counter}"
        coord_to_node[coord_key] = node_id
        node_counter += 1
        return node_id

    # build weighted graph from multilinestring pathways using adjacnecy list
    graph = {}

    #process all features to find multilinestring and linestirng
    for feature in geojson_data['features']:
        geom_type = feature['geometry']['type']

        if geom_type == 'MultiLineString':
            line_list = feature['geometry']['coordinates']

            for line_coords in line_list:
                for i in range(len(line_coords) - 1):
                    start_lon, start_lat = line_coords[i][0], line_coords[i][1]
                    end_lon, end_lat = line_coords[i + 1][0], line_coords[i + 1][1]
                    start_node = get_node_id(start_lon, start_lat)
                    end_node = get_node_id(end_lon, end_lat)
                    # distance calcs
                    distance = haversine_distance(
                        (start_lon, start_lat),
                        (end_lon, end_lat)
                    )
                    #init start and end node
                    if start_node not in graph:
                        graph[start_node] = []
                    if end_node not in graph:
                        graph[end_node] = []
                    #bidirectional edges
                    edge_exists = False
                    for neighbor, dist in graph[start_node]:
                        if neighbor == end_node and abs(dist - distance) < 0.001:
                            edge_exists = True
                            break
                    if not edge_exists:
                        graph[start_node].append((end_node, distance))
                        graph[end_node].append((start_node, distance))

        elif geom_type == 'LineString':
            line_coords = feature['geometry']['coordinates']
            for i in range(len(line_coords) - 1):
                start_lon, start_lat = line_coords[i][0], line_coords[i][1]
                end_lon, end_lat = line_coords[i + 1][0], line_coords[i + 1][1]
                start_node = get_node_id(start_lon, start_lat)
                end_node = get_node_id(end_lon, end_lat)
                distance = haversine_distance(
                    (start_lon, start_lat),
                    (end_lon, end_lat)
                )

                if start_node not in graph:
                    graph[start_node] = []
                if end_node not in graph:
                    graph[end_node] = []

                edge_exists = False
                for neighbor, dist in graph[start_node]:
                    if neighbor == end_node and abs(dist - distance) < 0.001:
                        edge_exists = True
                        break

                if not edge_exists:
                    graph[start_node].append((end_node, distance))
                    graph[end_node].append((start_node, distance))

    return graph, buildings

# dijkstra's algorithm with min-heap optimization using graph adjacency list, source or starting node, and destination as args
def dijkstra(graph: Dict[str, List[Tuple[str, float]]],
             source: str,
             destination: str) -> Tuple[Optional[List[str]], Optional[float]]:
    # input validation
    if source not in graph:
        return None, None
    if destination not in graph:
        return None, None
    if source == destination:
        return [source], 0.0
    # init distances to infinity for all nodes
    distances = {node: float('infinity') for node in graph}
    distances[source] = 0

    previous = {node: None for node in graph} # track previous node for path reconstruction
    pq = [(0, source)] # prio queue: (distance, node)
    visited = set() # visited nodes tracker

    while pq:
        current_dist, current = heapq.heappop(pq)
        # skip if already visited
        if current in visited:
            continue
        visited.add(current)
        #stop when we reach destination
        if current == destination:
            break
        # skip if we found a better path
        if current_dist > distances[current]:
            continue
        # check all neighbors
        for neighbor, weight in graph[current]:
            if neighbor in visited:
                continue
            # calculate tentative distance
            distance = current_dist + weight
            # update if we found a shorter path
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    # check if destination is reachable
    if distances[destination] == float('infinity'):
        return None, None
    # reconstruct path from end to start
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    # Reverse to get path from source to destination
    path.reverse()

    return path, distances[destination]
