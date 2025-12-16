from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path
from algorithms import dijkstra, build_graph_from_geojson, kruskal, prim

app = Flask(__name__)

#load geojson data
def load_geojson():
    geojson_path = Path(__file__).parent / 'data' / 'campus_map.geojson'
    with open(geojson_path, 'r') as f:
        return json.load(f)

# extract buildings and graph from geojson
try:
    geojson_data = load_geojson()
    print(f"DEBUG: Loaded GeoJSON with {len(geojson_data.get('features', []))} features")
    
    graph, all_node_coords, building_names = build_graph_from_geojson(geojson_data)
    print(f"DEBUG: Built graph with {len(graph)} nodes and {len(building_names)} buildings")
    
    buildings = list(building_names)
    building_coords = all_node_coords  # All nodes (buildings + path nodes) with coordinates
    print(f"DEBUG: Initialized {len(buildings)} buildings and {len(building_coords)} coordinates")
except Exception as e:
    print(f"ERROR during initialization: {e}")
    import traceback
    traceback.print_exc()
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/buildings')
def get_buildings():
    try:
        # defiine main bldgs in the campus
        main_buildings = [
            'CHSS - Admin Building',
            'School of Management Building',
            'Cultural Complex Center',
            'CARIM Building',
            'CSM Building',
            'Kalimudan / Student Center Lane',
            'EBL Dorm',
            'Library',
            'Training Gym',
            'Sports Complex Stadium'
        ]

        main = [b for b in main_buildings if b in buildings]
        others = sorted([b for b in buildings if b not in main_buildings])

        return jsonify({
            'main': main,
            'others': others,
            'all': buildings
        })
    except Exception as e:
        print(f"ERROR in get_buildings: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/graph-info')
def graph_info():
    building_nodes = [node for node in graph if node in building_names]
    path_nodes = [node for node in graph if node not in building_names]

    building_connections = {}
    for building in building_nodes:
        building_connections[building] = {
            'total_connections': len(graph[building]),
            'connected_to_buildings': sum(1 for n, _ in graph[building] if n in building_names),
            'connected_to_paths': sum(1 for n, _ in graph[building] if n not in building_names),
            'neighbors': [(n, round(d, 2)) for n, d in graph[building]]
        }

    return jsonify({
        'total_nodes': len(graph),
        'building_nodes': len(building_nodes),
        'path_nodes': len(path_nodes),
        'buildings': list(building_nodes),
        'building_connections': building_connections
    })

@app.route('/api/shortest-path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')

    # validate input
    if source not in buildings or destination not in buildings:
        return jsonify({'error': 'Invalid building selection'})

    # use dijkstra's algorithm to find shortest path
    full_path, distance = dijkstra(graph, source, destination)

    # check if path exists
    if full_path is None:
        return jsonify({'error': 'No path found between the selected buildings'})

    # filter path to show bldgs only and not the invisible path nodes (ayaw tanggali ples)
    building_only_path = [node for node in full_path if node in building_names]

    # calculate walking time (assumption is 80 meters/minute walking speed)
    time = round(distance / 80, 1)

    # Build path edges with coordinates for map visualization
    path_edges = []
    for i in range(len(full_path) - 1):
        node1 = full_path[i]
        node2 = full_path[i + 1]
        
        # Get coordinates for both nodes
        coord1 = building_coords.get(node1)
        coord2 = building_coords.get(node2)
        
        # Find edge weight from graph
        edge_weight = None
        if node1 in graph:
            for neighbor, weight in graph[node1]:
                if neighbor == node2:
                    edge_weight = weight
                    break
        
        path_edges.append({
            'node1': node1,
            'node2': node2,
            'weight': round(edge_weight, 2) if edge_weight else 0,
            'coord1': coord1,
            'coord2': coord2,
            'is_building_edge': coord1 is not None and coord2 is not None
        })

    return jsonify({
        'path': building_only_path, 
        'full_path': full_path,
        'path_edges': path_edges,  # New: edges with coordinates for map visualization
        'distance': round(distance, 2),
        'time': time
    })

@app.route('/api/mst')
def mst():
    # Use Kruskal's algorithm by default
    # You can also add a query parameter to choose between Kruskal and Prim
    algorithm = request.args.get('algorithm', 'kruskal').lower()

    if algorithm == 'prim':
        mst_edges, total_weight = prim(graph)
    else:
        mst_edges, total_weight = kruskal(graph)

    # Separate edges: those with building nodes and those with path nodes
    # For display, we only show building-to-building edges
    # For visualization, we show all edges that can be rendered
    
    all_edges_with_coords = []
    building_edges = []
    
    for edge in mst_edges:
        node1, node2, weight = edge
        
        # Check if both nodes are buildings
        is_node1_building = node1 in building_names
        is_node2_building = node2 in building_names
        
        # Get coordinates
        coord1 = building_coords[node1] if node1 in building_coords else None
        coord2 = building_coords[node2] if node2 in building_coords else None
        
        edge_data = {
            'node1': node1,
            'node2': node2,
            'weight': round(weight, 2),
            'coord1': coord1,
            'coord2': coord2,
            'is_building_edge': is_node1_building and is_node2_building
        }
        
        all_edges_with_coords.append(edge_data)
        
        # Add to building_edges if both endpoints are buildings
        if is_node1_building and is_node2_building:
            building_edges.append(edge_data)

    # Calculate total weight for building-to-building edges only
    building_edges_weight = sum(e['weight'] for e in building_edges)

    return jsonify({
        'edges': building_edges,  # Only building-to-building for display
        'all_edges': all_edges_with_coords,  # All edges for complete map visualization
        'total_weight': round(total_weight, 2),  # Total MST weight (includes path nodes)
        'building_edges_weight': round(building_edges_weight, 2),  # Weight of building edges
        'algorithm': algorithm,
        'num_buildings': len(building_names),
        'buildings_connected_directly': len(building_edges)
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Flask application...")
    print(f"Buildings loaded: {len(buildings)}")
    print(f"Total nodes with coordinates: {len(building_coords)}")
    print("=" * 50)
    app.run(debug=False, port=5000, use_reloader=False)
