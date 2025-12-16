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
from typing import Dict, List, Tuple, Optional, Set

# custom minheap implementation for dijkstra optimization
class MinHeap:
    def __init__(self):
        self.heap = []
    #minheap common functions
    def push(self, item: Tuple[float, str]) -> None:
        self.heap.append(item)
        self._bubble_up(len(self.heap) - 1)
    def pop(self) -> Tuple[float, str]:
        if len(self.heap) == 0:
            raise IndexError("pop from empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return min_item
    
    def __len__(self) -> int:
        return len(self.heap)
    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] < self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break
    def _bubble_down(self, index: int) -> None:
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            
            if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
                smallest = left_child
            if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
                smallest = right_child
            
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

# manual math functions

#convert degrees to radians
def manual_radians(degrees: float) -> float:
    pi = 3.141592653589793
    return degrees * (pi / 180.0)

# calc sine using taylor series approximation
def manual_sin(x: float) -> float:
    pi = 3.141592653589793
    two_pi = 2 * pi
    # normalize angle to [-pi, pi]
    x = x % two_pi
    if x > pi:
        x = x - two_pi
    # the taylor series
    result = 0.0
    term = x
    for n in range(1, 20):
        result += term
        term *= -x * x / ((2 * n) * (2 * n + 1))
    return result

# calc cos using taylor series approximation
def manual_cos(x: float) -> float:
    pi = 3.141592653589793
    two_pi = 2 * pi
    # normalize angle to [-pi, pi]
    x = x % two_pi
    if x > pi:
        x = x - two_pi
    result = 1.0
    term = 1.0
    for n in range(1, 20):
        term *= -x * x / ((2 * n - 1) * (2 * n))
        result += term
    return result

# manual square_root
def manual_sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    if x == 0:
        return 0.0
    # Newton's method: x_{n+1} = (x_n + x/x_n) / 2
    guess = x
    for _ in range(50):
        next_guess = (guess + x / guess) / 2.0
        if abs(next_guess - guess) < 1e-10:
            break
        guess = next_guess
    
    return guess

def manual_asin(x: float) -> float:
    """Calculate arcsine using Taylor series approximation"""
    if x < -1 or x > 1:
        raise ValueError("asin domain error")
    result = 0.0
    term = x
    x_squared = x * x
    for n in range(50):
        result += term
        term *= x_squared * (2.0 * n + 1) / (2.0 * n + 2)
    return result

# distance calc using haversine distance using args coord1 and coord2 to ret distance in meters
def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    lon1 = manual_radians(lon1)
    lat1 = manual_radians(lat1)
    lon2 = manual_radians(lon2)
    lat2 = manual_radians(lat2)

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = manual_sin(dlat/2)**2 + manual_cos(lat1) * manual_cos(lat2) * manual_sin(dlon/2)**2
    c = 2 * manual_asin(manual_sqrt(a))

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
    node_coords = {}  # NEW: store coordinates for path nodes
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
        node_coords[node_id] = (lon, lat)  # NEW: store original coordinates
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

    # Combine buildings and path nodes for complete coordinate dict
    all_coords = {**buildings, **node_coords}
    
    # Return graph, all coordinates, and building names set for distinction
    return graph, all_coords, set(buildings.keys())

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
    pq = MinHeap() # custom priority queue: (distance, node)
    pq.push((0, source))
    visited = set() # visited nodes tracker

    while len(pq) > 0:
        current_dist, current = pq.pop()
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
                pq.push((distance, neighbor))
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

# --- [New Pruning Logic] ---
def prune_mst(mst_edges: List[Tuple[str, str, float]], building_names: Set[str]) -> List[Tuple[str, str, float]]:
    """
    Removes 'fringe paths': edges that lead to a dead-end node that is NOT a building.
    Repeats until no such nodes exist.
    """
    # Build adjacency for the MST
    adj = {}
    for u, v, w in mst_edges:
        if u not in adj: adj[u] = []
        if v not in adj: adj[v] = []
        adj[u].append(v)
        adj[v].append(u)
        
    changed = True
    while changed:
        changed = False
        nodes_to_remove = []
        
        # Identify non-building leaves
        for node in list(adj.keys()):
            # Degree 1 means it's a leaf (dead end)
            if len(adj[node]) == 1 and node not in building_names:
                nodes_to_remove.append(node)
        
        if nodes_to_remove:
            changed = True
            for node in nodes_to_remove:
                neighbor = adj[node][0]
                adj[neighbor].remove(node)
                del adj[node]
                
    # Reconstruct edge list
    pruned = []
    seen = set()
    for u in adj:
        for v in adj[u]:
            edge_key = tuple(sorted((u, v)))
            if edge_key not in seen:
                # Find original weight
                weight = 0
                for ou, ov, ow in mst_edges:
                    if (ou == u and ov == v) or (ou == v and ov == u):
                        weight = ow
                        break
                pruned.append((u, v, weight))
                seen.add(edge_key)
    return pruned

# --- [Updated MST Functions] ---
class UnionFind:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}
    def find(self, n):
        if self.parent[n] != n: self.parent[n] = self.find(self.parent[n])
        return self.parent[n]
    def union(self, n1, n2):
        r1, r2 = self.find(n1), self.find(n2)
        if r1 == r2: return False
        if self.rank[r1] < self.rank[r2]: self.parent[r1] = r2
        elif self.rank[r1] > self.rank[r2]: self.parent[r2] = r1
        else:
            self.parent[r2] = r1
            self.rank[r1] += 1
        return True

def kruskal(graph, building_names):
    if not graph: return [], 0.0
    edges = []
    seen = set()
    for u in graph:
        for v, w in graph[u]:
            key = tuple(sorted((u, v)))
            if key not in seen:
                edges.append((w, u, v))
                seen.add(key)
    edges.sort()
    
    uf = UnionFind(list(graph.keys()))
    mst_edges = []
    
    for w, u, v in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            
    # PRUNE THE RESULT
    final_edges = prune_mst(mst_edges, building_names)
    total_weight = sum(w for _, _, w in final_edges)
    return final_edges, total_weight

def prim(graph, building_names, start_node=None):
    if not graph: return [], 0.0
    if start_node is None: start_node = next(iter(graph))
    
    visited = {start_node}
    mst_edges = []
    edges = []
    
    for v, w in graph[start_node]:
        edges.append((w, start_node, v))
        
    while edges and len(visited) < len(graph):
        # Manual min extract (replace with heap in prod)
        edges.sort(key=lambda x: x[0])
        w, u, v = edges.pop(0)
        
        if v in visited: continue
        
        visited.add(v)
        mst_edges.append((u, v, w))
        
        for next_v, next_w in graph[v]:
            if next_v not in visited:
                edges.append((next_w, v, next_v))

    # PRUNE THE RESULT
    final_edges = prune_mst(mst_edges, building_names)
    total_weight = sum(w for _, _, w in final_edges)
    return final_edges, total_weight
