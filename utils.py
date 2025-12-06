# Utility Functions
# Helper functions for the UP Mindanao Campus Navigation System

# load_graph_from_json function
# - Load campus map data from JSON file
# - Parse JSON structure
# - Create graph object
# - Add vertices and edges from data
# - Handle file not found and JSON parsing errors
# - Return populated graph object

# save_graph_to_json function
# - Save current graph to JSON file
# - Convert graph structure to JSON format
# - Include vertices and edges with weights
# - Handle file writing errors

# validate_building_name function
# - Check if building name exists in hash table
# - Case-insensitive comparison
# - Return standardized building name or None

# format_path function
# - Convert path list to readable string
# - Include arrows or separators between locations
# - Add distance information

# format_distance function
# - Convert distance to readable format
# - Handle meters/kilometers
# - Round to appropriate decimal places

# calculate_travel_time function
# - Estimate walking time based on distance
# - Use average walking speed (e.g., 5 km/h)
# - Return time in minutes

# display_menu function
# - Print formatted menu options
# - Clear and user-friendly display

# get_user_choice function
# - Prompt user for menu selection
# - Validate input (numeric, within range)
# - Handle invalid input with error messages
# - Return valid choice

# clear_screen function (optional)
# - Clear terminal screen for better UI
# - Handle different operating systems

# print_header function
# - Display formatted header/title
# - Use ASCII art or formatted text for branding

# print_separator function
# - Print visual separator line
# - Improve readability of output

# format_mst_output function
# - Format MST edges for display
# - Calculate and show total weight
# - Display in organized table format
