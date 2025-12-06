# Building Data and Hash Table
# This file manages building information using a hash table

# Building class
# - Store building information
# - Attributes: name, code, description, coordinates, type

# Constructor
# - Initialize building with all attributes
# - Validate input data

# String representation methods
# - __str__ for user-friendly display
# - __repr__ for debugging

# BuildingHashTable class
# - Hash table implementation for storing and retrieving building data
# - Uses separate chaining for collision resolution

# Constructor
# - Initialize hash table with default size
# - Create array of empty lists (buckets)
# - Track number of elements for load factor

# hash_function method
# - Convert building name/code to hash value
# - Use built-in hash() with modulo for table size
# - Handle string input

# insert method
# - Add building to hash table
# - Calculate hash value
# - Add to appropriate bucket
# - Handle duplicates (update or skip)
# - Track size

# search method
# - Find building by name or code
# - Calculate hash value
# - Search in appropriate bucket
# - Return Building object or None

# delete method
# - Remove building from hash table
# - Calculate hash value
# - Find and remove from bucket
# - Update size

# get_all_buildings method
# - Return list of all buildings in hash table
# - Iterate through all buckets

# resize method (optional)
# - Increase table size when load factor exceeds threshold
# - Rehash all existing elements

# display method
# - Print all buildings in organized format
# - Show bucket distribution for debugging

# UP Mindanao Buildings data
# - Define function or constant to initialize default buildings
# - Include major campus buildings:
#   - Academic buildings (colleges, classrooms)
#   - Administrative buildings
#   - Facilities (library, gym, cafeteria)
#   - Dormitories
#   - Landmarks
# - Each building should have name, code, type, and description
