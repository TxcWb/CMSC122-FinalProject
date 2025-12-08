from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path
from algorithms import dijkstra, build_graph_from_geojson

app = Flask(__name__)

#load geojson data
def load_geojson():
    geojson_path = Path(__file__).parent / 'data' / 'campus_map.geojson'
    with open(geojson_path, 'r') as f:
        return json.load(f)

# extract buildings and graph from geojson
geojson_data = load_geojson()
graph, building_coords = build_graph_from_geojson(geojson_data)
buildings = list(building_coords.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/buildings')
def get_buildings():
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

@app.route('/api/graph-info')
def graph_info():
    building_nodes = [node for node in graph if node in building_coords]
    path_nodes = [node for node in graph if node not in building_coords]

    building_connections = {}
    for building in building_nodes:
        building_connections[building] = {
            'total_connections': len(graph[building]),
            'connected_to_buildings': sum(1 for n, _ in graph[building] if n in building_coords),
            'connected_to_paths': sum(1 for n, _ in graph[building] if n not in building_coords),
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
    building_only_path = [node for node in full_path if node in building_coords]

    # calculate walking time (assumption is 80 meters/minute walking speed)
    time = round(distance / 80, 1)

    return jsonify({
        'path': building_only_path, 
        'full_path': full_path,
        'distance': round(distance, 2),
        'time': time
    })

# @app.route('/api/mst')
# def mst():
#     # Use Kruskal's algorithm by default
#     # You can also add a query parameter to choose between Kruskal and Prim
#     algorithm = request.args.get('algorithm', 'kruskal').lower()

#     if algorithm == 'prim':
#         mst_edges, total_weight = prim(graph)
#     else:
#         mst_edges, total_weight = kruskal(graph)

#     # Format edges for JSON response
#     edges = [(edge[0], edge[1], round(edge[2], 2)) for edge in mst_edges]

#     return jsonify({
#         'edges': edges,
#         'total_weight': round(total_weight, 2),
#         'algorithm': algorithm
#     })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
