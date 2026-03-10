graph = {
    (1,2): {"D":10, "T":15, "F":1.2},
    (1,6): {"D":10, "T":15, "F":1.2},
    (2,1): {"D":10, "T":15, "F":1.2},
    (2,3): {"D":12, "T":25, "F":1.5},
    (2,6): {"D":10, "T":15, "F":1.2},
    (2,5): {"D":12, "T":25, "F":1.5},
    (3,2): {"D":12, "T":25, "F":1.5},
    (3,4): {"D":12, "T":25, "F":1.5},
    (3,5): {"D":12, "T":25, "F":1.5},
    (3,6): {"D":10, "T":25, "F":1.3},
    (4,3): {"D":12, "T":25, "F":1.5},
    (4,5): {"D":14, "T":25, "F":1.2},
    (5,2): {"D":12, "T":25, "F":1.5},
    (5,3): {"D":12, "T":25, "F":1.5},
    (5,4): {"D":14, "T":25, "F":1.2},
    (5,6): {"D":10, "T":25, "F":1.5},
    (6,1): {"D":10, "T":15, "F":1.2},
    (6,2): {"D":10, "T":15, "F":1.2},
    (6,3): {"D":10, "T":25, "F":1.3},
    (6,5): {"D":10, "T":25, "F":1.5}
}

cities = [1, 2, 3, 4, 5, 6]

def find_best_path(start, end, metric):
    """Find the shortest path from start to end based on metric (D, T, or F).
    Checks direct edge, 1 intermediate, and 2 intermediate nodes."""
    
    best_value = float('inf')
    best_path = None
    
    # Check direct edge
    if (start, end) in graph:
        best_value = graph[(start, end)][metric]
        best_path = [start, end]
    
    # Check indirect paths through one intermediate node
    for mid in cities:
        if mid == start or mid == end:
            continue
        if (start, mid) in graph and (mid, end) in graph:
            value = graph[(start, mid)][metric] + graph[(mid, end)][metric]
            if value < best_value:
                best_value = value
                best_path = [start, mid, end]
    
    # Check indirect paths through two intermediate nodes
    for mid1 in cities:
        if mid1 == start or mid1 == end:
            continue
        for mid2 in cities:
            if mid2 == start or mid2 == end or mid2 == mid1:
                continue
            if (start, mid1) in graph and (mid1, mid2) in graph and (mid2, end) in graph:
                value = graph[(start, mid1)][metric] + graph[(mid1, mid2)][metric] + graph[(mid2, end)][metric]
                if value < best_value:
                    best_value = value
                    best_path = [start, mid1, mid2, end]
    
    return best_path, best_value if best_path else None

def calculate_node_total(start, metric):
    """Calculate total of shortest paths from start node to all other nodes."""
    total = 0
    paths = []
    for end in cities:
        if start == end:
            continue
        path, value = find_best_path(start, end, metric)
        if path is None:
            return None, []  # Can't reach all nodes
        total += value
        paths.append((end, path, value))
    return total, paths

# Find the best starting node for each metric
print("=" * 50)
print("         FINDING BEST STARTING NODE")
print("=" * 50)

# Tiebreaker order: if tied on primary metric, use these secondary metrics
tiebreakers = {
    "D": ["T", "F"],  # Distance ties broken by Time, then Fuel
    "T": ["D", "F"],  # Time ties broken by Distance, then Fuel
    "F": ["D", "T"]   # Fuel ties broken by Distance, then Time
}

metric_names = {"D": "Distance", "T": "Time", "F": "Fuel"}
metric_units = {"D": "km", "T": "min", "F": "L"}

for metric, name, unit in [("D", "Distance", "km"), ("T", "Time", "min"), ("F", "Fuel", "L")]:
    print(f"\n{'─' * 50}")
    print(f"  BEST BY {name.upper()}")
    print(f"{'─' * 50}")
    
    # Collect all node totals
    node_results = []
    for start in cities:
        total, paths = calculate_node_total(start, metric)
        if total is not None:
            # Also get tiebreaker values
            total_tb1, _ = calculate_node_total(start, tiebreakers[metric][0])
            total_tb2, _ = calculate_node_total(start, tiebreakers[metric][1])
            node_results.append((start, total, total_tb1, total_tb2, paths))
    
    # Print table header
    print(f"\n  {'Node':<6} {name + ' (' + unit + ')':<15}")
    print(f"  {'-'*6} {'-'*15}")
    
    # Print each node's totals
    for r in node_results:
        print(f"  {r[0]:<6} {round(r[1], 2):<15}")
    
    # Find minimum primary total
    min_total = min(r[1] for r in node_results)
    tied_nodes = [r for r in node_results if round(r[1], 2) == round(min_total, 2)]
    
    if len(tied_nodes) > 1:
        # Tie detected - use tiebreakers
        print(f"\n  ⚠ TIE DETECTED: Nodes {[r[0] for r in tied_nodes]} tied at {round(min_total, 2)} {unit}")
        
        # Sort by tiebreaker metrics
        tied_nodes.sort(key=lambda r: (r[2], r[3]))
        winner = tied_nodes[0]
        
        tb1_name = metric_names[tiebreakers[metric][0]]
        tb1_unit = metric_units[tiebreakers[metric][0]]
        print(f"  → Tiebreaker by {tb1_name}:")
        for r in tied_nodes:
            marker = " ← Winner" if r[0] == winner[0] else ""
            print(f"      Node {r[0]}: {round(r[2], 2)} {tb1_unit}{marker}")
    else:
        winner = tied_nodes[0]
    
    print(f"\n  ★ BEST STARTING NODE: {winner[0]}")
    print(f"    Total {name}: {round(winner[1], 2)} {unit}")
    
    # Print paths table
    print(f"\n  {'To':<4} {'Path':<20} {name:<10}")
    print(f"  {'-'*4} {'-'*20} {'-'*10}")
    for end, path, value in winner[4]:
        path_str = " → ".join(map(str, path))
        print(f"  {end:<4} {path_str:<20} {round(value, 2)} {unit}")

print(f"\n{'=' * 50}")