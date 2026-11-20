"""
200. Number of Islands
https://leetcode.com/problems/number-of-islands/

Difficulty: Medium
Topics: array, depth-first-search, breadth-first-search, union-find, matrix

Approach
--------
Scan every cell. Each time an unvisited land cell ("1") is found, it starts a
new island: flood it with an iterative BFS, turning every reached land cell
into water ("0") and enqueueing all in-bounds land neighbours. Sinking cells
as they are discovered is the visited set, and it guarantees each cell is
enqueued at most once.

BFS is used instead of recursion so a 300x300 all-land grid cannot overflow
Python's recursion limit.

Complexity
----------
Time:  O(m * n)  -- every cell is read once, and enqueued at most once
Space: O(m * n)  -- worst-case queue for one huge island (plus grid mutation)

Why optimal
-----------
A cell's membership in an island is not known until it is inspected, so any
correct algorithm must read all m*n cells in the worst case: Omega(m*n) time.
Each cell is processed a constant number of times here, so the bound is
tight. Space is the BFS frontier; a DFS/union-find variant reaches the same
asymptotics (union-find pays O(m*n * alpha) time instead).

Edge cases
----------
- All water: returns 0, the scan just skips every cell.
- All land: one island, the queue can hold an entire diagonal frontier.
- Single row or single column: neighbour checks must not wrap around.
- 1x1 grid of land or water.

Pitfalls
--------
- Checking bounds after indexing neighbours.
- Marking cells as visited only on dequeue, which lets duplicates explode
  the queue and can produce a quadratic slowdown.
- Recursive DFS on a 300x300 grid hitting Python's default recursion limit.
- Note this solution mutates `grid`; copy it first if the caller needs it.

Video
-----
(not published yet)
"""

from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "1":
                    continue

                islands += 1
                grid[r][c] = "0"
                queue = deque([(r, c)])

                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"
                            queue.append((nr, nc))

        return islands


def _self_test() -> None:
    s = Solution()

    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert s.numIslands(grid1) == 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert s.numIslands(grid2) == 3

    assert s.numIslands([["0"]]) == 0
    assert s.numIslands([["1"]]) == 1
    assert s.numIslands([["1", "0", "1"]]) == 2
    assert s.numIslands([["1"], ["0"], ["1"]]) == 2
    assert s.numIslands([]) == 0
