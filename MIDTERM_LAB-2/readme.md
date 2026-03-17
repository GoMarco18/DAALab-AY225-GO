BRIEF REPORT (Approach, Algorithm, Challenges)

1) Approach
I developed an interactive network/graph visualization tool where users can build a graph manually by adding edges (or by bulk-pasting multiple edges). Each edge stores three attributes: distance, time, and fuel. After building/refreshing the graph, the program renders the network using a D3 force-directed layout with zoom/pan, draggable nodes, a “fit to screen” option, a random layout shuffle, and a static layout toggle that can freeze node positions.

The tool supports two main computations:
(1) Single-factor shortest path (A → B) by optimizing one attribute (distance OR time OR fuel).
(2) Multi-factor shortest path using a weighted combination of distance, time, and fuel.

Results are shown in an output panel and visually highlighted on the graph. For the multi-factor option, the program also displays a detailed calculation table showing each edge along the chosen path, including raw values, normalized values, and per-edge score contributions.

2) Algorithm Used

A) Single-Factor Shortest Path (Dijkstra’s Algorithm)
For the single-factor shortest path, I used Dijkstra’s algorithm. The algorithm maintains:
- dist[node]: the best known cost from the source to that node
- prev[node]: the previous node used to reconstruct the final path

Process summary:
1. Initialize all distances to infinity, except the source which is 0.
2. Repeatedly select the unvisited node with the smallest distance.
3. Relax its neighbors using the chosen edge weight (distance/time/fuel).
4. Stop when the target is reached or all nodes are processed.
5. Reconstruct the path using prev[].

Note: This implementation selects the minimum node by scanning a Set of remaining nodes (simple but O(V^2) behavior), which is acceptable for small/medium graphs typical in an assignment. A priority queue could optimize it to O((V+E) log V).

B) Multi-Factor Shortest Path (Normalized Weighted Score + Dijkstra)
For multi-factor routing, I still used Dijkstra’s algorithm, but I replaced the edge weight with a combined score:

score = wD * norm(D) + wT * norm(T) + wF * norm(F)

To make distance/time/fuel comparable, I applied min-max normalization across all edges in the graph:
norm(X) = (X - minX) / (maxX - minX)

To avoid division-by-zero when maxX == minX, I clamp the range using a very small epsilon (1e-9).

Dijkstra then runs using this combined edge score, producing the path with the minimum total combined score. I also store the chosen edges (prevEdge) so that the calculation table can show step-by-step values and totals.

3) Challenges Faced

1. Combining multiple metrics fairly:
Distance, time, and fuel can have very different numeric scales, so a raw weighted sum would be misleading. Normalization was necessary so the weights behave as intended.

2. Division-by-zero during normalization:
If all edges share the same value for a factor (e.g., all distances equal), the normalization denominator becomes zero. I handled this by clamping the range to a small epsilon to keep the program stable.

3. Making results understandable:
Multi-factor shortest paths can be hard to trust without explanation. To address this, I added a calculation table that displays raw values, normalized values, per-edge scores, and totals, plus the global min/max ranges used for normalization.

4. Performance vs simplicity:
I used a simple Set-based Dijkstra implementation (linear scan for the next minimum node) to keep the code straightforward. For larger graphs, switching to a priority queue would be a clear improvement.

5. Undirected graph handling:
The visualization stores each link once, but shortest-path traversal must work in both directions. I solved this by building the adjacency list in both directions when the graph is constructed.
