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
CMSC122-FinalProject/
├── app.py                      # Flask web server
├── algorithms.py               # Pathfinding algorithms (to be implemented)
├── templates/
│   └── index.html             # Main web page
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet
│   ├── js/
│   │   └── script.js          # Frontend JavaScript
│   └── data/
│       └── campus_map.geojson # Campus map data
├── data/
│   └── campus_map.geojson     # Campus data (GeoJSON format)
└── requirements.txt           # Python dependencies
```

## Features

- Interactive campus map visualization
- Find shortest path between buildings
- Generate Minimum Spanning Trees (Kruskal & Prim)
- View all campus buildings
- Responsive design for mobile and desktop
- GeoJSON-based map data with real coordinates

## Technologies

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data**: GeoJSON

