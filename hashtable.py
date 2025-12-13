"""Hash table utilities for building lookup.

Loads buildings from the GeoJSON map and stores them in a simple hash table
with separate chaining to handle collisions. Each entry keeps at least three
pieces of information: name, dean (placeholder), contact (placeholder), and
map coordinates pulled from the GeoJSON.
"""
