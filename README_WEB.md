# UP Mindanao Campus Navigation System - Web Version

## Setup Instructions

### 1. Install Dependencies
```bash
pip install flask flask-cors
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## Project Structure

```
upmindanao_system/
├── app.py                      # Flask web server
├── main.py                     # Original CLI application
├── graph.py                    # Graph implementation
├── algorithms.py               # Pathfinding algorithms
├── buildings.py                # Building data management
├── utils.py                    # Helper functions
├── templates/
│   └── index.html             # Main web page
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet
│   └── js/
│       └── script.js          # Frontend JavaScript
├── data/
│   └── campus_map.json        # Campus data
└── requirements.txt           # Python dependencies
```

## Features

- Interactive campus map visualization
- Find shortest path between buildings
- Generate Minimum Spanning Trees (Kruskal & Prim)
- View all campus buildings
- Responsive design for mobile and desktop

## Technologies

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Canvas/SVG (to be implemented)
- **Data**: JSON

## API Endpoints

- `GET /` - Main page
- `GET /api/buildings` - Get all buildings
- `POST /api/shortest-path` - Find shortest path
- `GET /api/mst/kruskal` - Generate MST using Kruskal
- `POST /api/mst/prim` - Generate MST using Prim
- `GET /api/graph` - Get complete graph data
