from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data - replace with your actual graph implementation
buildings = [
    "Main Library",
    "CSM Building",
    "CAS Building",
    "Admin Building",
    "Gymnasium",
    "Canteen",
    "Student Center"
]

# Sample graph (you'll replace this with your actual graph structure)
graph = {
    "Main Library": [("CSM Building", 150), ("Admin Building", 200)],
    "CSM Building": [("Main Library", 150), ("CAS Building", 100)],
    "CAS Building": [("CSM Building", 100), ("Gymnasium", 180)],
    "Admin Building": [("Main Library", 200), ("Student Center", 120)],
    "Gymnasium": [("CAS Building", 180), ("Canteen", 90)],
    "Canteen": [("Gymnasium", 90), ("Student Center", 110)],
    "Student Center": [("Admin Building", 120), ("Canteen", 110)]
}

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
