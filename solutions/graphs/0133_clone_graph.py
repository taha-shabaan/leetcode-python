"""
133. Clone Graph
https://leetcode.com/problems/clone-graph/

Difficulty: Medium
Topics: graph, depth-first-search, breadth-first-search, hash-table

Approach
--------
Depth-first search with a dictionary that maps every original node to its
clone. When a node is first reached, create its copy and record the mapping
*before* walking its neighbours. That early mark is what makes cycles safe:
a neighbour that points back to an ancestor finds the clone already in the
dictionary and reuses it instead of recursing forever. Each neighbour is then
cloned and appended to the copy's neighbour list.

The dictionary doubles as the visited set, so every node is copied exactly
once and every edge is traversed exactly once.

Complexity
----------
Time:  O(V + E)  -- each node is copied once and each adjacency entry visited
       once
Space: O(V)      -- the original-to-clone dictionary plus the recursion stack,
       which is at most V deep

Why optimal
-----------
A deep copy must create one new object per node and reproduce every edge, so
Omega(V + E) time is a lower bound; the single DFS pass meets it. The mapping
from originals to copies is required to recognise already-cloned nodes, and it
holds V entries, so the space bound is also unavoidable.

Edge cases
----------
- Empty graph (`node is None`) -> return None.
- Single node with no neighbours -> one fresh node with an empty list.
- A cycle of any length -> the early dictionary mark prevents infinite
  recursion.
- The maximum 100-node graph -> recursion depth is at most 100, well inside
  Python's default limit.
- Shared neighbours (a diamond) -> the shared node is cloned once and both
  copies point at the same clone, preserving the graph's structure.

Pitfalls
----------
- Marking a node in the dictionary only after visiting its neighbours, which
  loops forever on any cycle.
- Creating a fresh copy on every visit instead of checking the dictionary
  first, which duplicates shared nodes.
- Returning the original node, or letting the clone share neighbour objects
  with the original instead of building a genuinely independent graph.
- Forgetting the `None` case when the graph is empty.

Video
-----
(not published yet)
"""

from typing import List, Optional


class Node:
    def __init__(
        self, val: int = 0, neighbors: Optional[List["Node"]] = None
    ) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        clones = {}

        def dfs(original: Optional[Node]) -> Optional[Node]:
            if original is None:
                return None
            if original in clones:
                return clones[original]

            copy = Node(original.val)
            clones[original] = copy
            for neighbor in original.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy

        return dfs(node)


def _self_test() -> None:
    def build(adj_list):
        if not adj_list:
            return None
        nodes = [Node(i + 1) for i in range(len(adj_list))]
        for i, neighbors in enumerate(adj_list):
            nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
        return nodes[0]

    def adjacency(node):
        if node is None:
            return []
        seen = {}
        stack = [node]
        while stack:
            current = stack.pop()
            if current.val in seen:
                continue
            seen[current.val] = current
            stack.extend(current.neighbors)
        return [
            [neighbor.val for neighbor in sorted(seen[val].neighbors, key=lambda n: n.val)]
            for val in sorted(seen)
        ]

    def collect(node):
        if node is None:
            return []
        seen = {}
        stack = [node]
        while stack:
            current = stack.pop()
            if current.val in seen:
                continue
            seen[current.val] = current
            stack.extend(current.neighbors)
        return [seen[val] for val in sorted(seen)]

    s = Solution()

    example = [[2, 4], [1, 3], [2, 4], [1, 3]]
    original = build(example)
    cloned = s.cloneGraph(original)
    assert adjacency(cloned) == example
    assert cloned is not original
    assert cloned.val == 1

    # Empty graph.
    assert s.cloneGraph(None) is None

    # Single node without neighbours.
    single = build([[]])
    single_clone = s.cloneGraph(single)
    assert adjacency(single_clone) == [[]]
    assert single_clone is not single
    assert single_clone.neighbors == []

    # Two-node graph.
    assert adjacency(s.cloneGraph(build([[2], [1]]))) == [[2], [1]]

    # Diamond: node 1 reaches node 4 through both 2 and 3.
    diamond = [[2, 3], [1, 4], [1, 4], [2, 3]]
    diamond_clone = s.cloneGraph(build(diamond))
    assert adjacency(diamond_clone) == diamond
    cloned_nodes = collect(diamond_clone)
    node_two, node_three = cloned_nodes[1], cloned_nodes[2]
    assert node_two.neighbors[1] is node_three.neighbors[1]

    # Maximum-size cycle (100 nodes) exercises the deepest allowed recursion.
    n = 100
    cycle = [
        [((i - 2) % n) + 1, (i % n) + 1]
        for i in range(1, n + 1)
    ]
    cycle_clone = s.cloneGraph(build(cycle))
    assert adjacency(cycle_clone) == [sorted(row) for row in cycle]
    assert len(collect(cycle_clone)) == n

    # The clone must be fully independent of the original.
    original = build(example)
    cloned = s.cloneGraph(original)
    original.val = 999
    original.neighbors.append(Node(42))
    assert cloned.val == 1
    assert adjacency(cloned) == example
    original_ids = {id(node) for node in collect(original)}
    cloned_ids = {id(node) for node in collect(cloned)}
    assert original_ids.isdisjoint(cloned_ids)
