from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

# Load GeoJSON data
def load_geojson():
    geojson_path = Path(__file__).parent / 'data' / 'campus_map.geojson'
    with open(geojson_path, 'r') as f:
        return json.load(f)

# Extract buildings and graph from GeoJSON
geojson_data = load_geojson()
buildings = []
graph = {}

# Extract building locations (Point features)
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Point':
        name = feature['properties'].get('Name', '')
        if name:
            buildings.append(name)
            graph[name] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/buildings')
def get_buildings():
    return jsonify(buildings)

@app.route('/api/shortest-path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    
    # Simple BFS for demo - replace with your Dijkstra implementation
    if source not in buildings or destination not in buildings:
        return jsonify({'error': 'Invalid building selection'})
    
    # Dummy response - replace with actual algorithm
    path = [source, "CSM Building", destination]
    distance = 250
    time = round(distance / 80, 1)  # 80m/min walking speed
    
    return jsonify({
        'path': path,
        'distance': distance,
        'time': time
    })

@app.route('/api/mst')
def mst():
    # Dummy MST - replace with actual Kruskal or Prim
    edges = [
        ("Main Library", "CSM Building", 150),
        ("CSM Building", "CAS Building", 100),
        ("CAS Building", "Gymnasium", 180),
        ("Gymnasium", "Canteen", 90),
        ("Main Library", "Admin Building", 200),
        ("Admin Building", "Student Center", 120)
    ]
    total = sum(e[2] for e in edges)
    
    return jsonify({
        'edges': edges,
        'total_weight': total
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
