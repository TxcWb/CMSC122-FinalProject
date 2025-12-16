from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path
from algorithms import dijkstra, build_graph_from_geojson, kruskal, prim
from hashtable import HashTable, load_building_data, get_embedded_data

app = Flask(__name__)

# --- INITIALIZATION BLOCK ---
# We use a global try-except block to ensure data loads before the app starts
try:
    # 1. Load GeoJSON Data
    geojson_path = Path(__file__).parent / 'data' / 'campus_map.geojson'
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    print(f"DEBUG: Loaded GeoJSON with {len(geojson_data.get('features', []))} features")
    
    # 2. Build the Graph (Using the updated algorithms.py logic)
    # Note: algorithms.py now returns (graph, all_coords, building_names)
    graph, building_coords, building_names = build_graph_from_geojson(geojson_data)
    
    buildings = list(building_names)
    print(f"DEBUG: Built graph with {len(graph)} nodes and {len(buildings)} buildings")

    building_hash_table = HashTable(50)
    geojson_buildings = load_building_data(geojson_path)
    for building in geojson_buildings:
        building_name = building['Name']
        coordinates = building['Coordinates']
        extra_info = get_embedded_data(building_name)
        if extra_info:  # Only add buildings that are not excluded
            building_hash_table.add(building_name, coordinates, extra_info)
    print(f"DEBUG: Initialized hash table with building information")
    
    # 3. Build 'edge_geometries' map
    # This maps specific node-to-node connections back to their curvy GeoJSON lines
    edge_geometries = {} 
    
    # Helper to match coordinates with floating point tolerance
    def coords_match(c1, c2):
        if not c1 or not c2: return False
        return abs(c1[0] - c2[0]) < 1e-7 and abs(c1[1] - c2[1]) < 1e-7
    
    for feature in geojson_data['features']:
        geom = feature['geometry']
        if geom['type'] in ['LineString', 'MultiLineString']:
            # Handle both single and multi-lines
            lines = geom['coordinates'] if geom['type'] == 'MultiLineString' else [geom['coordinates']]
            
            for coords in lines:
                if len(coords) >= 2:
                    start_c = coords[0]
                    end_c = coords[-1]
                    
                    # Identify which nodes sit at these coordinates
                    start_node = None
                    end_node = None
                    
                    for node, c in building_coords.items():
                        if coords_match(c, start_c): start_node = node
                        if coords_match(c, end_c): end_node = node
                    
                    if start_node and end_node:
                        # Store geometry for both directions
                        edge_geometries[(start_node, end_node)] = coords
                        edge_geometries[(end_node, start_node)] = list(reversed(coords))

    print(f"DEBUG: Mapped {len(edge_geometries)} road segments to geometry")

except Exception as e:
    print(f"CRITICAL ERROR during initialization: {e}")
    import traceback
    traceback.print_exc()
    # We don't raise here to allow Flask to start and show errors in browser, 
    # but the app will likely fail if data isn't loaded.

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/buildings')
def get_buildings():
    try:
        main_buildings = [
            'CHSS - Admin Building', 'School of Management Building', 
            'Cultural Complex Center', 'CARIM Building', 'CSM Building', 
            'Kalimudan / Student Center Lane', 'EBL Dorm', 'Library', 
            'Training Gym', 'Sports Complex Stadium'
        ]
        main = [b for b in main_buildings if b in buildings]
        others = sorted([b for b in buildings if b not in main_buildings])
        return jsonify({'main': main, 'others': others, 'all': buildings})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/building-info/<building_name>')
def get_building_info(building_name):
    """Fetch building information from the hash table."""
    try:
        record = building_hash_table.get(building_name)
        if record:
            return jsonify({
                'name': record['building_name'],
                'coordinates': record['coordinates'],
                'details': record['details']
            })
        else:
            return jsonify({'error': 'Building not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shortest-path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')

    if source not in buildings or destination not in buildings:
        return jsonify({'error': 'Invalid building selection'})

    full_path, distance = dijkstra(graph, source, destination)

    if full_path is None:
        return jsonify({'error': 'No path found between the selected buildings'})

    # Construct path edges with geometry for visualization
    path_edges = []
    for i in range(len(full_path) - 1):
        node1 = full_path[i]
        node2 = full_path[i + 1]
        
        # Look up the curvy geometry if it exists
        geometry = edge_geometries.get((node1, node2))
        
        # Get edge weight
        weight = 0
        for n, w in graph.get(node1, []):
            if n == node2:
                weight = w
                break

        path_edges.append({
            'node1': node1,
            'node2': node2,
            'coord1': building_coords.get(node1),
            'coord2': building_coords.get(node2),
            'geometry': geometry, # This is what was missing!
            'weight': weight
        })

    return jsonify({
        'path': [n for n in full_path if n in buildings], 
        'full_path': full_path,
        'path_edges': path_edges,
        'distance': round(distance, 2),
        'time': round(distance / 80, 1)
    })

@app.route('/api/mst')
def mst():
    algorithm = request.args.get('algorithm', 'kruskal').lower()
    
    # 1. Run the MST Algorithm
    if algorithm == 'prim':
        mst_edges, total_weight = prim(graph, set(buildings))
    else:
        mst_edges, total_weight = kruskal(graph, set(buildings))

    # 2. Format for Frontend
    all_edges_with_coords = []
    building_edges = []
    
    for edge in mst_edges:
        node1, node2, weight = edge
        
        # Retrieve strict geometry if available
        geometry = edge_geometries.get((node1, node2)) or edge_geometries.get((node2, node1))
        
        # Check if this is a direct connection between two buildings
        is_direct = (node1 in buildings) and (node2 in buildings)

        edge_data = {
            'node1': node1,
            'node2': node2,
            'weight': round(weight, 2),
            'coord1': building_coords.get(node1),
            'coord2': building_coords.get(node2),
            'geometry': geometry,
            'is_building_edge': is_direct
        }
        
        all_edges_with_coords.append(edge_data)
        if is_direct:
            building_edges.append(edge_data)

    # Calculate the sum of weights for building-only edges
    building_edges_weight = sum(e['weight'] for e in building_edges)

    return jsonify({
        'edges': building_edges,
        'all_edges': all_edges_with_coords,
        'total_weight': round(total_weight, 2),
        'building_edges_weight': round(building_edges_weight, 2), # <--- This was missing!
        'algorithm': algorithm,
        'buildings_connected_directly': len(building_edges)
    })

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, port=5000)