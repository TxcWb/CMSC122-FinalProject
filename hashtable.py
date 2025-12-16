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


# Main program
if __name__ == "__main__":
    # Initialize hash table
    table = HashTable(20)

    # Load buildings from geojson file
    file_path = "campus_map.geojson"
    buildings = load_building_data(file_path)

    # Classifications and their details
    intersections = ["TODA Intersection", "Rotunda 1", "Rotunda 2", "Rotunda 3", "CARIM Intersection", "Sports Complex Intersection"]
    dean_buildings = ["CHSS - Admin Building", "School of Management Building", "CSM Building"]
    research_buildings = ["CARIM Building"]
    libraries = ["Kanto Library"]
    sports_facilities = ["Sports Complex Stadium", "Training Gym", "Cultural Complex Center"]
    unavailable_facilities = ["Aquatics Center"]
    dormitories = ["EBL Dorm"]

    # Collect user input for buildings
    print("Provide the necessary details for the following buildings:")
    for building in buildings:
        building_name = building['Name']
        coordinates = building['Coordinates']
        extra_info = {}

        if building_name in intersections:
            print(f"\nBuilding Name (Intersection): {building_name}")
            extra_info["Traffic Flow Pattern"] = input("Enter Traffic Flow Pattern: ")
            extra_info["Pedestrian Crossing Availability"] = input("Enter Pedestrian Crossing Availability (Yes/No): ")
            extra_info["Peak Congestion Times"] = input("Enter Peak Congestion Times (e.g., '7-8 AM, 5-6 PM'): ")

        elif building_name in dean_buildings:
            print(f"\nBuilding Name (Dean Building): {building_name}")
            extra_info["Departments Housed"] = input("Enter Departments Housed: ")
            extra_info["Dean"] = input("Enter Dean Name: ")
            extra_info["Contact Number"] = input("Enter Contact Number: ")

        elif building_name in research_buildings:
            print(f"\nBuilding Name (Research Center): {building_name}")
            extra_info["Research Focus Areas"] = input("Enter Research Focus Areas (e.g., 'Medical, Innovation'): ")
            extra_info["Personnel"] = input("Enter Personnel Name: ")
            extra_info["Contact Number"] = input("Enter Contact Number: ")

        elif building_name in libraries:
            print(f"\nBuilding Name (Library): {building_name}")
            extra_info["Personnel"] = input("Enter Personnel Name: ")
            extra_info["Contact Number"] = input("Enter Contact Number: ")
            extra_info["Opening Hours"] = input("Enter Opening Hours (e.g., '8 AM - 6 PM'): ")

        elif building_name in sports_facilities:
            print(f"\nBuilding Name (Sports Facility): {building_name}")
            extra_info["Personnel"] = input("Enter Personnel Name: ")
            extra_info["Contact Number"] = input("Enter Contact Number: ")
            extra_info["Opening Hours"] = input("Enter Opening Hours (e.g., '8 AM - 6 PM'): ")

        elif building_name in unavailable_facilities:
            print(f"\nBuilding Name: {building_name}")
            extra_info["Status"] = "Unavailable"

        elif building_name in dormitories:
            print(f"\nBuilding Name (Dormitory): {building_name}")
            extra_info["Personnel"] = input("Enter Personnel Name: ")
            extra_info["Contact Number"] = input("Enter Contact Number: ")
            extra_info["Number of Rooms Available"] = input("Enter Number of Rooms Available: ")

        else:
            print(f"\nBuilding Name (Other): {building_name}")
            extra_info["Details"] = input("Enter Additional Details: ")

        table.add(building_name, coordinates, extra_info)

    # Fetch a building record
    building_to_fetch = input("\nEnter the name of the building to fetch its details: ")
    fetched_building = table.get(building_to_fetch)
    if fetched_building:
        print(f"Details for {building_to_fetch}:")
        print(fetched_building)
    else:
        print(f"{building_to_fetch} not found.")

    # Delete a building record
    building_to_delete = input("\nEnter the name of the building to delete: ")
    print(table.delete(building_to_delete))

    # Verify deletion
    print(f"Verifying deletion of {building_to_delete}:")
    print(table.get(building_to_delete))
