
from typing import Dict, List, Set
from collections import defaultdict


# Node states for DFS
WHITE = 0  # Not visited
GRAY = 1   # Being processed (in recursion stack)
BLACK = 2  # Completely processed


def has_cycle(graph: Dict[int, List[int]]) -> bool:
    
    # Get all nodes in the graph
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    # Initialize all nodes as WHITE (not visited)
    color = {node: WHITE for node in all_nodes}
    
    def dfs(node: int) -> bool:
        
        # Mark current node as being processed
        color[node] = GRAY
        
        # Visit all neighbors
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                # Found a back edge (cycle detected)
                return True
            if color[neighbor] == WHITE:
                # Visit unvisited neighbor
                if dfs(neighbor):
                    return True
        
        # Mark node as completely processed
        color[node] = BLACK
        return False
    
    # Run DFS from each unvisited node
    for node in all_nodes:
        if color[node] == WHITE:
            if dfs(node):
                return True
    
    return False


def has_cycle_with_path(graph: Dict[int, List[int]]) -> tuple:
    
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    color = {node: WHITE for node in all_nodes}
    parent = {node: None for node in all_nodes}
    
    def dfs(node: int) -> int:
        
        color[node] = GRAY
        
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                parent[neighbor] = node  # Mark the back edge
                return neighbor  # Cycle starts here
            if color[neighbor] == WHITE:
                parent[neighbor] = node
                result = dfs(neighbor)
                if result != -1:
                    return result
        
        color[node] = BLACK
        return -1
    
    for node in all_nodes:
        if color[node] == WHITE:
            cycle_start = dfs(node)
            if cycle_start != -1:
                # Reconstruct the cycle
                cycle = [cycle_start]
                current = parent[cycle_start]
                while current != cycle_start:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(cycle_start)
                cycle.reverse()
                return True, cycle
    
    return False, None


def has_cycle_iterative(graph: Dict[int, List[int]]) -> bool:

    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    color = {node: WHITE for node in all_nodes}
    
    for start in all_nodes:
        if color[start] != WHITE:
            continue
        
        # Stack contains (node, iterator over neighbors)
        stack = [(start, iter(graph.get(start, [])))]
        color[start] = GRAY
        
        while stack:
            node, neighbors_iter = stack[-1]
            
            try:
                neighbor = next(neighbors_iter)
                if color[neighbor] == GRAY:
                    return True  # Cycle found
                if color[neighbor] == WHITE:
                    color[neighbor] = GRAY
                    stack.append((neighbor, iter(graph.get(neighbor, []))))
            except StopIteration:
                # All neighbors processed
                color[node] = BLACK
                stack.pop()
    
    return False


def has_cycle_kahns(graph: Dict[int, List[int]]) -> bool:
    
    # Calculate in-degree for each node
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    in_degree = {node: 0 for node in all_nodes}
    
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Queue of nodes with in-degree 0
    queue = [node for node in all_nodes if in_degree[node] == 0]
    processed = 0
    
    while queue:
        node = queue.pop(0)
        processed += 1
        
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we couldn't process all nodes, there's a cycle
    return processed != len(all_nodes)


def find_all_cycles(graph: Dict[int, List[int]]) -> List[List[int]]:
    
    all_nodes = list(set(graph.keys()).union(*[set(v) for v in graph.values()]))
    cycles = []
    
    def dfs(start: int, current: int, path: List[int], visited: Set[int]) -> None:
        visited.add(current)
        path.append(current)
        
        for neighbor in graph.get(current, []):
            if neighbor == start and len(path) > 1:
                cycles.append(path.copy())
            elif neighbor not in visited:
                dfs(start, neighbor, path, visited)
        
        path.pop()
        visited.remove(current)
    
    for node in all_nodes:
        dfs(node, node, [], set())
    
    return cycles


# Test the solutions
if __name__ == "__main__":
    print("Graph Cycle Detection (Directed Graph)")
    print("=" * 50)
    
    # Example from the problem (has cycle)
    graph1 = {
        0: [1],
        1: [2],
        2: [3],
        3: [0]
    }
    
    print("Graph 1 (with cycle):")
    print("0 -> 1 -> 2 -> 3 -> 0")
    print(f"Adjacency list: {graph1}")
    
    result1 = has_cycle(graph1)
    print(f"Has cycle (DFS): {result1}")
    
    result1_iter = has_cycle_iterative(graph1)
    print(f"Has cycle (Iterative): {result1_iter}")
    
    result1_kahn = has_cycle_kahns(graph1)
    print(f"Has cycle (Kahn's): {result1_kahn}")
    
    has_cycle_result, cycle_path = has_cycle_with_path(graph1)
    print(f"Cycle path: {' -> '.join(map(str, cycle_path)) if cycle_path else 'None'}")
    
    print()
    print("=" * 50)
    print()
    
    # Graph without cycle (DAG)
    graph2 = {
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }
    
    print("Graph 2 (DAG - no cycle):")
    print("0 -> 1 -> 3")
    print("0 -> 2 -> 3")
    print(f"Adjacency list: {graph2}")
    
    result2 = has_cycle(graph2)
    print(f"Has cycle (DFS): {result2}")
    
    result2_kahn = has_cycle_kahns(graph2)
    print(f"Has cycle (Kahn's): {result2_kahn}")
    
    print()
    print("=" * 50)
    print()
    
    # Graph with self-loop
    graph3 = {
        0: [1],
        1: [1],  # Self-loop
        2: [0]
    }
    
    print("Graph 3 (with self-loop):")
    print(f"Adjacency list: {graph3}")
    
    result3 = has_cycle(graph3)
    print(f"Has cycle: {result3}")
    
    print()
    print("=" * 50)
    print()
    
    # Graph with multiple components, one has cycle
    graph4 = {
        0: [1],
        1: [2],
        2: [],
        3: [4],
        4: [5],
        5: [3]  # Cycle in second component
    }
    
    print("Graph 4 (multiple components, cycle in one):")
    print("Component 1: 0 -> 1 -> 2 (no cycle)")
    print("Component 2: 3 -> 4 -> 5 -> 3 (has cycle)")
    print(f"Adjacency list: {graph4}")
    
    result4 = has_cycle(graph4)
    print(f"Has cycle: {result4}")
    
    print()
    print("=" * 50)
    print()
    
    # Complex graph with multiple cycles
    graph5 = {
        0: [1, 2],
        1: [3],
        2: [3, 4],
        3: [0],  # Cycle: 0 -> 1 -> 3 -> 0
        4: [5],
        5: [2]   # Cycle: 2 -> 4 -> 5 -> 2
    }
    
    print("Graph 5 (multiple cycles):")
    print(f"Adjacency list: {graph5}")
    
    result5 = has_cycle(graph5)
    print(f"Has cycle: {result5}")
    
    all_cycles = find_all_cycles(graph5)
    print(f"All cycles found: {all_cycles}")
