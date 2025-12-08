# Plan: Implement MST Feature with Kruskal's Algorithm

## TL;DR
Implement Kruskal's algorithm with a custom Union-Find data structure in `algorithms.py` and uncomment the `/api/mst` route in `app.py`. The frontend is already prepared to display MST results. We'll implement Kruskal's algorithm (no built-in libraries beyond what's already imported) to find the minimum spanning tree connecting all campus buildings and pathways.

## Steps

1. **Implement Union-Find helper class** in `algorithms.py` with `find()` (path compression) and `union()` (union by rank) methods—needed for cycle detection in Kruskal's algorithm.

2. **Implement `kruskal()` function** in `algorithms.py` that extracts all edges from the graph, sorts by weight, applies Union-Find to build MST without cycles, and returns edges and total weight.

3. **Optionally implement `prim()` function** in `algorithms.py` as a fallback (vertex-based MST using manual priority queue handling).

4. **Uncomment and verify `/api/mst` route** in `app.py` to handle GET requests and call the appropriate MST algorithm.

5. **Test the endpoint** by calling `/api/mst` and verifying the frontend displays the MST edges with distances correctly.

## Further Considerations

1. **Built-in library constraint**: You mentioned "without using any built-in libraries"—do you mean only standard library (`heapq`, `math`) allowed, or completely custom everything? Current code uses `heapq` for Dijkstra; Kruskal's doesn't need it. Clarify if this restriction applies retroactively to existing code.

Don't use built-in library that provides MST directly (like NetworkX). The implementation should be manual.

2. **Starting vertex for Prim's**: If implementing Prim's as fallback, should it start from a specific building (e.g., first in list) or be configurable via query parameter like the commented code suggests?

Start from the first building in the list for simplicity.

3. **MST visualization**: Should the frontend highlight MST edges on the map differently from other paths, or just display the edge list in the Results section?

I believe it should do both: highlight on map and list edges with distances.

## Research Summary: Campus Navigator MST Implementation

### Current Status of /api/mst Route in app.py

The `/api/mst` route is **completely commented out** (lines 68-82):
```python
# @app.route('/api/mst')
# def mst():
#     algorithm = request.args.get('algorithm', 'kruskal').lower()
#     # ... rest commented
```

**What's needed**: Uncomment and implement the functions it calls (`kruskal()` and `prim()`). The route structure is already designed but both backend algorithms are missing.

### Frontend MST Handling

The frontend is **ready to use MST functionality**:

- **HTML Button** (index.html line 47): 
  ```html
  <button onclick="showMST()" class="btn-secondary">Generate MST</button>
  ```

- **JavaScript Implementation** (script.js lines 107-125):
  ```javascript
  function showMST() {
      fetch('/api/mst')
          .then(response => response.json())
          .then(data => {
              // Renders edge list with format: node1 ↔ node2 (distance)
          })
  }
  ```

The frontend expects a JSON response with `edges` (array of [node1, node2, weight]) and `total_weight`.

### Data Flow Frontend → Backend

1. User clicks "Generate MST" button → `showMST()` function called
2. Sends **GET request** to `/api/mst` 
3. Backend processes graph with MST algorithm
4. Returns JSON: `{ edges: [...], total_weight: ..., algorithm: ... }`
5. Frontend renders results as bulleted list with distances and total weight

The graph structure is:
- **Graph**: `Dict[str, List[Tuple[str, float]]]` (adjacency list with weights)
- **Building Coordinates**: `Dict[str, Tuple[float, float]]` (lon, lat)
- Nodes are either building names or auto-generated path nodes (node_0, node_1, etc.)

### Algorithm Recommendation: Kruskal's vs Prim's

**Kruskal's Algorithm is better suited** for this project:

| Criteria | Kruskal | Prim |
|----------|---------|------|
| **Implementation Complexity** | Medium (requires Union-Find) | Medium (requires priority queue) |
| **Data Structure Efficiency** | More efficient with sparse graphs | More efficient with dense graphs |
| **Campus Network Type** | ✓ Better (sparse tree structure) | Works but less ideal |
| **Edge vs Vertex Focus** | Edge-based (naturally suits path networks) | Vertex-based |
| **Startup Requirement** | No starting vertex needed | Requires starting vertex |

**Reasoning**: Campus pathways form a sparse, tree-like network. Kruskal's edge-based approach naturally models pathways and requires no arbitrary starting point. Also conceptually cleaner for connectivity problems.

### Missing Imports and Dependencies

**In algorithms.py - Already Present:**
- ✓ `heapq` (for Dijkstra's)
- ✓ `math` (for haversine)
- ✓ Type hints: `Dict`, `List`, `Tuple`, `Optional`, `Set`

**Missing for MST Implementation:**
- Nothing! All required libraries are already imported. Just need to implement the algorithms.

### Summary of Implementation

1. **Implement Union-Find class** in `algorithms.py`
2. **Implement `kruskal()` function** in `algorithms.py`
3. **Optionally implement `prim()` function** in `algorithms.py`
4. **Uncomment and verify** the `/api/mst` route in `app.py`
5. **Ensure Flask and dependencies** are installed

The frontend and route structure are **completely ready**—only the backend algorithms need to be implemented.
