"""
207. Course Schedule
https://leetcode.com/problems/course-schedule/

Difficulty: Medium
Topics: depth-first-search, breadth-first-search, graph, topological-sort

Approach
--------
Model prerequisites as a directed graph with an edge `prereq -> course`. The
courses can all be finished exactly when this graph is acyclic. Detect cycles
with a three-colour DFS:

- 0 = unvisited
- 1 = currently on the DFS path (visiting)
- 2 = fully processed (done)

Reaching a neighbour that is still 1 is a back edge, hence a cycle. A neighbour
that is 2 can be skipped safely.

The canonical `Solution` runs this DFS with an explicit stack (each frame stores
its node and the index of the next child to visit) so a 2000-course chain cannot
overflow Python's recursion limit. `Solution2` keeps the original recursive
formulation for reference; it is correct but can hit `RecursionError` on deep
chains.

Complexity
----------
Time:  O(V + E)  -- each course and each prerequisite edge is examined once
Space: O(V + E)  -- adjacency list plus colour array and DFS stack of O(V)

Why optimal
-----------
Every prerequisite edge must be inspected to rule out a cycle, so any correct
algorithm needs at least O(V + E) time. The DFS touches each vertex and edge a
constant number of times, so the bound is tight. Kahn's topological sort reaches
the same asymptotics.

Edge cases
----------
- No prerequisites: every course is free, return True.
- Self-loop `[c, c]`: immediately a cycle, return False.
- Duplicate prerequisite pairs: harmless, they just add parallel edges.
- Disconnected graph: every component must be started separately.
- A cycle confined to one component makes the whole answer False.
- A long DAG chain (e.g. 2000 courses): handled by the iterative DFS.

Pitfalls
----------
- Marking a node done before exploring all of its descendants, which hides
  back edges and reports a cyclic graph as valid.
- Using a plain visited set that cannot distinguish "on the current path" from
  "finished earlier"; only the former signals a cycle.
- Reversing the edge direction (`course -> prereq`), which still finds cycles
  but is easy to reason about incorrectly.
- Recursive DFS on a 2000-deep chain raising `RecursionError`.
- Only starting the DFS from course 0 instead of every unvisited course.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adjacency = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            adjacency[prereq].append(course)

        UNVISITED, VISITING, DONE = 0, 1, 2
        color = [UNVISITED] * numCourses

        for start in range(numCourses):
            if color[start] != UNVISITED:
                continue

            color[start] = VISITING
            stack = [(start, 0)]

            while stack:
                node, next_index = stack[-1]

                if next_index < len(adjacency[node]):
                    neighbor = adjacency[node][next_index]
                    stack[-1] = (node, next_index + 1)

                    if color[neighbor] == VISITING:
                        return False
                    if color[neighbor] == UNVISITED:
                        color[neighbor] = VISITING
                        stack.append((neighbor, 0))
                else:
                    color[node] = DONE
                    stack.pop()

        return True


class Solution2(object):
    """Original recursive three-colour DFS.

    Correct, but the recursion depth equals the longest dependency chain, so a
    chain near `numCourses == 2000` can exceed Python's default recursion limit.
    """

    def canFinish(self, numCourses, prerequisites):
        adjacency = [[] for _ in range(numCourses)]
        color = [0] * numCourses

        for course, prereq in prerequisites:
            adjacency[prereq].append(course)

        def dfs(node):
            color[node] = 1
            for neighbor in adjacency[node]:
                if color[neighbor] == 1:
                    return False
                if color[neighbor] == 0 and not dfs(neighbor):
                    return False
            color[node] = 2
            return True

        for course in range(numCourses):
            if color[course] == 0 and not dfs(course):
                return False
        return True


def _self_test() -> None:
    for solver in (Solution(), Solution2()):
        assert solver.canFinish(2, [[1, 0]]) is True
        assert solver.canFinish(2, [[1, 0], [0, 1]]) is False
        assert solver.canFinish(1, []) is True
        assert solver.canFinish(1, [[0, 0]]) is False
        assert solver.canFinish(3, []) is True
        assert solver.canFinish(4, [[1, 0], [2, 1], [3, 2]]) is True
        assert solver.canFinish(4, [[1, 0], [2, 1], [3, 2], [0, 3]]) is False
        assert solver.canFinish(2, [[1, 0], [1, 0]]) is True
        assert solver.canFinish(5, [[1, 0], [3, 2]]) is True
        assert solver.canFinish(5, [[1, 0], [0, 1], [3, 2]]) is False
        assert solver.canFinish(3, [[0, 1], [1, 2], [2, 0]]) is False

    # A 2000-course chain exceeds Python's default recursion limit; only the
    # iterative canonical solution is expected to survive it.
    n = 2000
    chain = [[i + 1, i] for i in range(n - 1)]
    assert Solution().canFinish(n, chain) is True
    assert Solution().canFinish(n, chain + [[0, n - 1]]) is False
