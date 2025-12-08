// Initialize map
let map;
let campusData;

// Load buildings when page loads
window.onload = function() {
    initMap();
    loadBuildings();
};

function initMap() {
    // Center on UP Mindanao coordinates
    map = L.map('map').setView([7.0851, 125.4790], 15);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Load and display GeoJSON
    fetch('/static/data/campus_map.geojson')
        .then(response => response.json())
        .then(data => {
            campusData = data;
            
            // Add GeoJSON layer
            L.geoJSON(data, {
                pointToLayer: function(feature, latlng) {
                    return L.marker(latlng).bindPopup(feature.properties.Name || 'Unknown');
                },
                style: function(feature) {
                    return {
                        color: '#667eea',
                        weight: 3,
                        opacity: 0.7
                    };
                }
            }).addTo(map);
        })
        .catch(error => console.error('Error loading map:', error));
}

function loadBuildings() {
    fetch('/api/buildings')
        .then(response => response.json())
        .then(data => {
            const sourceSelect = document.getElementById('source');
            const destSelect = document.getElementById('destination');
            // add main bldg group
            let mainGroup = '<optgroup label="(Main Buildings)">';
            data.main.forEach(building => {
                mainGroup += `<option value="${building}">${building}</option>`;
            });
            mainGroup += '</optgroup>';
            // others group
            let othersGroup = '<optgroup label="(Others)">';
            data.others.forEach(building => {
                othersGroup += `<option value="${building}">${building}</option>`;
            });
            othersGroup += '</optgroup>';
            //add both dropdowns
            sourceSelect.innerHTML += mainGroup + othersGroup;
            destSelect.innerHTML += mainGroup + othersGroup;
        })
        .catch(error => {
            document.getElementById('output').innerHTML = `<p style="color: red;">Error loading buildings: ${error}</p>`;
        });
}

function findPath() {
    const source = document.getElementById('source').value;
    const destination = document.getElementById('destination').value;
    
    if (!source || !destination) {
        document.getElementById('output').innerHTML = '<p style="color: red;">Please select both starting point and destination.</p>';
        return;
    }
    
    if (source === destination) {
        document.getElementById('output').innerHTML = '<p style="color: red;">Starting point and destination cannot be the same.</p>';
        return;
    }
    
    // Clear previous MST visualization when finding a new path
    clearMSTLayers();
    
    document.getElementById('output').innerHTML = '<p>Finding path...</p>';
    
    fetch('/api/shortest-path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            source: source,
            destination: destination
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            const pathHTML = `
                <div class="path-result">
                    <h4>📍 Route Found!</h4>
                    <p><strong>Path:</strong> ${data.path.join(' → ')}</p>
                    <p class="distance">Distance: ${data.distance} meters</p>
                    <p>Estimated time: ${data.time} minutes</p>
                </div>
            `;
            document.getElementById('output').innerHTML = pathHTML;
        }
    })
    .catch(error => {
        document.getElementById('output').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
    });
}

function showMST() {
    document.getElementById('output').innerHTML = '<p>Generating Minimum Spanning Tree...</p>';
    
    // Clear previous MST layers
    clearMSTLayers();
    
    fetch('/api/mst')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('output').innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                // Render all MST edges on map (including path nodes for full connectivity)
                renderMSTOnMap(data.all_edges);
                
                // Display results using only building-to-building edges
                let html = '<div class="path-result"><h4>🌳 Minimum Spanning Tree</h4>';
                html += `<p class="algorithm-info">Algorithm: ${data.algorithm.toUpperCase()}</p>`;
                
                if (data.edges && data.edges.length > 0) {
                    html += '<ul>';
                    data.edges.forEach(edge => {
                        html += `<li>${edge.node1} ↔ ${edge.node2} <span class="edge-weight">(${edge.weight}m)</span></li>`;
                    });
                    html += '</ul>';
                    html += `<p class="distance">Direct Building Connections: ${data.buildings_connected_directly}</p>`;
                    html += `<p class="distance">Total MST Weight: ${data.total_weight} meters</p>`;
                    html += `<p style="font-size: 0.9rem; color: #7f8c8d;">Building Edges Weight: ${data.building_edges_weight}m</p>`;
                } else {
                    html += '<p>No direct building-to-building connections in MST.</p>';
                    html += `<p class="distance">Total MST Weight (with paths): ${data.total_weight} meters</p>`;
                }
                
                html += '</div>';
                document.getElementById('output').innerHTML = html;
            }
        })
        .catch(error => {
            document.getElementById('output').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
        });
}

// Store MST layer group globally
let mstLayerGroup;

function renderMSTOnMap(edges) {
    // Create a feature group for MST edges
    mstLayerGroup = L.featureGroup();
    
    edges.forEach(edge => {
        // Draw lines for edges that have at least one coordinate
        if (edge.coord1 && edge.coord2) {
            const latlng1 = [edge.coord1[1], edge.coord1[0]]; // Convert [lon, lat] to [lat, lon]
            const latlng2 = [edge.coord2[1], edge.coord2[0]];
            
            // Determine color based on edge type
            const isDirectBuilding = edge.is_building_edge;
            const lineColor = isDirectBuilding ? '#e74c3c' : '#e67e22';  // Red for direct, orange for path
            const lineWeight = isDirectBuilding ? 4 : 2;
            const dashArray = isDirectBuilding ? '5, 5' : '3, 3';
            
            // Draw MST edge line on map with distinctive styling
            const line = L.polyline([latlng1, latlng2], {
                color: lineColor,
                weight: lineWeight,
                opacity: 0.8,
                dashArray: dashArray,
                lineCap: 'round',
                lineJoin: 'round'
            }).bindPopup(`${edge.node1} ↔ ${edge.node2} (${edge.weight}m)`);
            
            mstLayerGroup.addLayer(line);
        }
    });
    
    // Add the feature group to the map
    mstLayerGroup.addTo(map);
}

function clearMSTLayers() {
    if (mstLayerGroup) {
        map.removeLayer(mstLayerGroup);
        mstLayerGroup = null;
    }
}
