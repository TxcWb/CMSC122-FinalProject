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
    
    fetch('/api/mst')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('output').innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                let html = '<div class="path-result"><h4>🌳 Minimum Spanning Tree</h4><ul>';
                data.edges.forEach(edge => {
                    html += `<li>${edge[0]} ↔ ${edge[1]} (${edge[2]}m)</li>`;
                });
                html += `</ul><p class="distance">Total Weight: ${data.total_weight} meters</p></div>`;
                document.getElementById('output').innerHTML = html;
            }
        })
        .catch(error => {
            document.getElementById('output').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
        });
}
