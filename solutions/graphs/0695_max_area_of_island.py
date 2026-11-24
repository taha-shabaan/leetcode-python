"""
695. Max Area of Island
https://leetcode.com/problems/max-area-of-island/

Difficulty: Medium
Topics: array, depth-first-search, breadth-first-search, union-find, matrix

Approach
--------
Scan every cell. Each time an unvisited land cell ("1") is found, flood its
4-connected island with an iterative DFS, sinking each reached land cell to
water ("0") and counting it. Sinking cells as they are discovered is the
visited marker, so each cell is pushed at most once. Track the largest island
seen and return it.

DFS is used iteratively instead of recursion so a 50x50 all-land grid cannot
overflow Python's recursion limit.

Complexity
----------
Time:  O(m * n)  -- every cell is read once, and pushed at most once
Space: O(m * n)  -- worst-case stack for one huge island (plus grid mutation)

Why optimal
-----------
A cell's island membership is not known until it is inspected, so any correct
algorithm must read all m*n cells in the worst case: Omega(m*n) time. Each
cell is processed a constant number of times here, so the bound is tight.
Space is the DFS frontier; BFS/union-find reach the same asymptotics.

Edge cases
----------
- All water: returns 0, the scan skips every cell.
- All land: one island of size m*n.
- Single row or single column: neighbour checks must not wrap around.
- 1x1 grid of land or water.

Pitfalls
----------
- Marking a cell visited only when popped, which lets duplicates explode the
  stack and can produce a quadratic slowdown.
- Forgetting that diagonal cells are NOT connected (only 4-directional).
- Using `row == rows and col == cols` as a boundary check: it never fires.
- Recursive DFS on a 50x50 grid hitting Python's default recursion limit.
- Note this solution mutates `grid`; copy it first if the caller needs it.
"""

import copy
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        best = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    continue

                area = 1
                grid[r][c] = 0
                stack = [(r, c)]

                while stack:
                    cr, cc = stack.pop()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            grid[nr][nc] = 0
                            area += 1
                            stack.append((nr, nc))

                best = max(best, area)

        return best


class Solution2(object):
    """Alternative recursive DFS that keeps an explicit visited matrix."""

    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        if conected group backtracking it`s necessary but if the seprate nodes in the graph it`s only explore and choose not (unod)
        """
        dirs = ((1,0), (0,1), (-1,0), (0,-1))
        row_counts = len(grid)
        col_counts = len(grid[0])
        # island_num=0
        vis = [[False] * col_counts for _ in range(row_counts)]
        ans = 0
        # total=0

        def is_valid(row, col):
            return (
                0<= row <row_counts
                and 0<= col <col_counts
                and not vis[row][col]
                and grid[row][col]==1
            )
        def dfs(row, col):
            if row==row_counts and col==col_counts:
                return 1
            total=1
            vis[row][col]=True
            for dx, dy in dirs: #(0,2)
                rx=dx+row
                cy=dy+col
                if is_valid(rx, cy):
                    vis[rx][cy]=True
                    total+= dfs(rx, cy)
                    # vis[rx][cy]=False
            return total


        for row in range(row_counts):
            for col in range(col_counts):
                if grid[row][col]==1 and not vis[row][col]:
                    vis[row][col]=True
                    total = dfs(row,col)
                    # vis[row][col]=False
                    ans = max(ans, total)

        return ans


def _self_test() -> None:
    grid1 = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]

    for solver in (Solution(), Solution2()):
        assert solver.maxAreaOfIsland(copy.deepcopy(grid1)) == 6
        assert solver.maxAreaOfIsland([[0, 0, 0, 0, 0, 0, 0, 0]]) == 0
        assert solver.maxAreaOfIsland([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1]]) == 4
        assert solver.maxAreaOfIsland([[1]]) == 1
        assert solver.maxAreaOfIsland([[0]]) == 0
        assert solver.maxAreaOfIsland([[1, 1, 1, 1]]) == 4
        assert solver.maxAreaOfIsland([[1], [1], [0], [1]]) == 2

    # LeetCode guarantees at least one row and column; only the iterative
    # solution additionally handles an empty grid.
    assert Solution().maxAreaOfIsland([]) == 0
