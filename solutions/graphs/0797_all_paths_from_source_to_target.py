"""
797. All Paths From Source to Target
https://leetcode.com/problems/all-paths-from-source-to-target/

Difficulty: Medium
Topics: backtracking, depth-first-search, breadth-first-search, graph,
        directed-acyclic-graph

Approach
--------
Enumerate paths with a DFS that carries the current path on a shared list.
Start at node 0, append each neighbour before recursing, and pop it after the
call returns so sibling branches start from the same prefix. Reaching node
`n - 1` means a complete path was built, so append a snapshot (`path[:]`) to
the answer.

No visited set is needed: the input is a DAG, so a path can never return to a
node it already contains. Adding one would only risk dropping valid paths if it
were not undone correctly. The recursion depth is at most `n <= 15`, far below
Python's limit.

`Solution2` keeps the original submitted variant, which tracks the nodes on
the current path with a visited array that is undone on backtrack.

Complexity
----------
Time:  O(P * n)  -- each edge is walked once per path that uses it, and every
       emitted path of length up to n is copied; P is the number of paths.
Space: O(n)      -- the path list plus recursion depth; the output holds
       O(P * n) integers and is not counted as working space.

Why optimal
-----------
The answer itself can contain P paths of up to n nodes each, and a complete DAG
on n nodes has 2^(n-2) paths from 0 to n-1, so Omega(P * n) time is forced just
to write the output. DFS extends one path by one node per recursive step, so it
achieves that bound; BFS reaches the same asymptotics but copies every prefix.

Edge cases
----------
- Target unreachable from node 0 -> `[]`; the DFS simply finishes.
- Direct edge `0 -> n-1` -> the target is recorded immediately.
- Converging paths (a diamond) -> both paths are emitted, since the shared
  suffix is rebuilt after backtracking.
- Deepest chain 0 -> 1 -> ... -> n-1 -> exactly one path, recursion depth n.
- n = 2 -> either `[[0, 1]]` or `[]`.

Pitfalls
----------
- Appending `path` itself instead of `path[:]`, so every answer entry aliases
  the same list and ends up empty.
- Leaving a global visited mark set after recursion, which makes a node
  unavailable to later paths that share it (the diamond case).
- Forgetting to pop after the recursive call, growing the path across sibling
  branches.
- Adding a visited array out of habit: the graph is guaranteed acyclic, so it
  is unnecessary here.
- Leaving debug `print` calls inside the DFS, which floods stdout and slows
  the enumeration.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        target = len(graph) - 1
        path = [0]
        paths: List[List[int]] = []

        def dfs(node: int) -> None:
            if node == target:
                paths.append(path[:])
                return

            for neighbour in graph[node]:
                path.append(neighbour)
                dfs(neighbour)
                path.pop()

        dfs(0)
        return paths


class Solution2(object):
    """Original submission: same DFS, with a path-local visited array."""

    def allPathsSourceTarget(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: List[List[int]]
        """
        n = len(graph)
        path = []
        ans = []
        visited = [False] * n

        def dfs(i):
            if i == n - 1:
                ans.append(path[:])
                return

            if 0 not in path:
                path.append(0)

            for neighbour in graph[i]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    path.append(neighbour)
                    dfs(neighbour)
                    visited[neighbour] = False
                    path.pop()

        dfs(0)
        return ans


def _self_test() -> None:
    def normalise(paths):
        return sorted(tuple(path) for path in paths)

    solvers = (Solution(), Solution2())

    example_one = [[1, 2], [3], [3], []]
    expected_one = [[0, 1, 3], [0, 2, 3]]

    example_two = [[4, 3, 1], [3, 2, 4], [3], [4], []]
    expected_two = [
        [0, 4],
        [0, 3, 4],
        [0, 1, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 4],
    ]

    diamond = [[1, 2], [3], [3], [4], []]
    expected_diamond = [[0, 1, 3, 4], [0, 2, 3, 4]]

    complete = [
        [1, 2, 3, 4],
        [2, 3, 4],
        [3, 4],
        [4],
        [],
    ]

    chain = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], []]

    for solver in solvers:
        assert normalise(solver.allPathsSourceTarget(example_one)) == normalise(expected_one)
        assert normalise(solver.allPathsSourceTarget(example_two)) == normalise(expected_two)
        assert normalise(solver.allPathsSourceTarget(diamond)) == normalise(expected_diamond)

        # n = 2: direct edge, and an unreachable target.
        assert normalise(solver.allPathsSourceTarget([[1], []])) == [(0, 1)]
        assert solver.allPathsSourceTarget([[], []]) == []

        # Target reachable only through a longer route, with dead ends.
        assert normalise(solver.allPathsSourceTarget([[1, 2], [3], [4], [4], []])) == [
            (0, 1, 3, 4),
            (0, 2, 4),
        ]

        # Complete DAG on 5 nodes has exactly 2^(5-2) = 8 paths.
        assert len(solver.allPathsSourceTarget(complete)) == 8

        # Deepest allowed chain: one path of length 15, exercises recursion depth.
        assert solver.allPathsSourceTarget(chain) == [list(range(15))]

        # Every returned path must start at 0, end at n-1, and use real edges.
        for path in solver.allPathsSourceTarget(example_two):
            assert path[0] == 0 and path[-1] == len(example_two) - 1
            for src, dst in zip(path, path[1:]):
                assert dst in example_two[src]

    # Snapshots must be independent, not aliases of the working path list.
    result = Solution().allPathsSourceTarget(example_one)
    result[0].append(999)
    assert 999 not in result[1]
