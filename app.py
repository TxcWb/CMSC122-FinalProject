from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# UP Mindanao Campus Buildings
buildings = [
    "College of Science and Mathematics",
    "UP Mindanao Admin Building",
    "Davao City Sports Complex",
    "UP Mindanao Human Kinetics Building and Training Gym",
    "UP Mindanao Aquatics Center",
    "EBL Dorm",
    "CARIM Building",
    "Kalimudan",
    "Mindanao Studies & Cultural Center"
]

# Sample graph (you'll replace this with your actual graph structure from GeoJSON)
graph = {
    "College of Science and Mathematics": [("CARIM Building", 150), ("UP Mindanao Aquatics Center", 200)],
    "UP Mindanao Admin Building": [("EBL Dorm", 100), ("Mindanao Studies & Cultural Center", 250)],
    "Davao City Sports Complex": [("UP Mindanao Human Kinetics Building and Training Gym", 80)],
    "UP Mindanao Human Kinetics Building and Training Gym": [("Davao City Sports Complex", 80), ("UP Mindanao Aquatics Center", 300)],
    "UP Mindanao Aquatics Center": [("College of Science and Mathematics", 200), ("UP Mindanao Human Kinetics Building and Training Gym", 300)],
    "EBL Dorm": [("UP Mindanao Admin Building", 100), ("Kalimudan", 150)],
    "CARIM Building": [("College of Science and Mathematics", 150), ("Mindanao Studies & Cultural Center", 180)],
    "Kalimudan": [("EBL Dorm", 150), ("UP Mindanao Admin Building", 200)],
    "Mindanao Studies & Cultural Center": [("UP Mindanao Admin Building", 250), ("CARIM Building", 180)]
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
