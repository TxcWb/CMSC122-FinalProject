// Load buildings when page loads
window.onload = function() {
    loadBuildings();
};

function loadBuildings() {
    fetch('/api/buildings')
        .then(response => response.json())
        .then(buildings => {
            const sourceSelect = document.getElementById('source');
            const destSelect = document.getElementById('destination');
            
            buildings.forEach(building => {
                // Add to dropdowns
                sourceSelect.innerHTML += `<option value="${building}">${building}</option>`;
                destSelect.innerHTML += `<option value="${building}">${building}</option>`;
            });
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
