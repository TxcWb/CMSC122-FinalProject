"""Hash table utilities for building lookup.

Loads buildings from the GeoJSON map and stores them in a simple hash table
with separate chaining to handle collisions. Each entry keeps at least three
pieces of information: name, dean (placeholder), contact (placeholder), and
map coordinates pulled from the GeoJSON.
"""
import json

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # Using lists to handle collisions (chaining)

    def hash_function(self, key):
        """Custom hash function to generate index based on the key (building name)."""
        return sum(ord(char) for char in key) % self.size

    def add(self, building_name, coordinates, extra_info):
        """Add a building record to the hash table."""
        index = self.hash_function(building_name)
        # Check if the building already exists
        for record in self.table[index]:
            if record['building_name'] == building_name:
                return f"Building {building_name} already exists."
        # Add the new record
        self.table[index].append({
            'building_name': building_name,
            'coordinates': coordinates,
            'details': extra_info
        })

    def get(self, building_name):
        """Retrieve a building record by name."""
        index = self.hash_function(building_name)
        for record in self.table[index]:
            if record['building_name'] == building_name:
                return record
        return None

    def delete(self, building_name):
        """Delete a building record by name."""
        index = self.hash_function(building_name)
        for i, record in enumerate(self.table[index]):
            if record['building_name'] == building_name:
                del self.table[index][i]
                return f"Building {building_name} deleted."
        return f"Building {building_name} not found."

    def display_building(self, building_name):
        """Retrieve and display a building in formatted way."""
        record = self.get(building_name)
        if not record:
            print(f"{building_name} not found.")
            return
        
        print(f"Building name : {record['building_name']}")
        print(f"Coordinates : {record['coordinates']}")
        
        for key, value in record['details'].items():
            print(f"{key} : {value}")
        return record  # Still returns the dict if needed


# Load data from campus_map.geojson
def load_building_data(file_path):
    """Loads building data from a geojson file."""
    with open(file_path, 'r') as file:
        geojson_data = json.load(file)
    building_data = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            name = feature['properties'].get('Name')
            coordinates = feature['geometry']['coordinates']
            if name:  # Only add entries with a defined name
                building_data.append({"Name": name, "Coordinates": coordinates})
    return building_data

# Embedded data for each building category
def get_embedded_data(building_name):
    """Get embedded data for a specific building name."""
    dean_buildings = {
        "CHSS - Admin Building": {"Dean": "Prof. Jhoanna Lynn B. Cruz ", "Tel. No.": "(082) 293 0084"},
        "School of Management Building": {"Dean": "Assoc. Prof. Aurelia Luzviminda V. Gomez", "Tel. No.": "(082) 295-2188"},
        "CSM Building": { "Dean": "Prof. Cleto L. Nanola Jr.", "Tel. No.": "(082) 293 0312"}
    }

    research_centers = {
        "CARIM Building": {"Research Focus Areas": "Innovation", "Personnel": "N/A"}
    }

    libraries = {
        "Library": {"Personnel": "Merlyn M. Pausanos, RL", "Opening Hours": "8 AM - 86 PM"}
    }

    sports_facilities = {
        "Sports Complex Stadium": {"Athletic training equipment" : "", "Opening Hours": "6 AM - 6 PM"},
        "Training Gym": {"Fitness Equipment": "Treadmills, Weights", "Opening Hours": "6 AM - 6 PM"},
        "Cultural Complex Center": {"Performance spaces" : "Stage", "Seating Configuration" : "None"}
    }

    unavailable_facilities = {
        "Aquatics Center": {"Status": "Unavailable"}
    }

    student_buildings = {
        "EBL Dorm": {"Personnel": "Ann Miraflor Batomalaque", "Contact": "https://www.facebook.com/annmiraflor.batomalaque", },
        "Kalimudan / Student Center Lane": {"Facilities": "Canteen, lounges", "Opening Hours": "7 AM - 6 PM"}
    }

    # Intersections: explicitly excluded from insertion
    excluded_intersections = [
        "TODA Intersection", "Rotunda 1", "Rotunda 2", "Rotunda 3",
        "CARIM Intersection", "Sports Complex Intersection"
    ]

    # Skip intersections
    if building_name in excluded_intersections:
        return None

    # Determine the category and return data
    return (
        dean_buildings.get(building_name)
        or research_centers.get(building_name)
        or libraries.get(building_name)
        or sports_facilities.get(building_name)
        or unavailable_facilities.get(building_name)
        or student_buildings.get(building_name)
        or {"Details": "Other or Unknown Building"}
    )

# Main program
if __name__ == "__main__":
    # Initialize hash table
    table = HashTable(20)

    # Load buildings from geojson file
    file_path = "campus_map.geojson"
    buildings = load_building_data(file_path)

    # Populate hash table with embedded data
    for building in buildings:
        building_name = building['Name']
        coordinates = building['Coordinates']
        extra_info = get_embedded_data(building_name)
        if extra_info:  # Only add buildings that are not excluded (e.g., intersections)
            table.add(building_name, coordinates, extra_info)

    # Fetch a building record
    table.display_building("CHSS - Admin Building")
    
