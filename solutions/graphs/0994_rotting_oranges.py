"""
994. Rotting Oranges
https://leetcode.com/problems/rotting-oranges/

Difficulty: Medium
Topics: array, breadth-first-search, matrix

Approach
--------
Multi-source BFS. Every rotten orange starts in the queue at minute 0, and
each BFS layer is one minute: all fresh neighbours of the current frontier rot
together. A `fresh` counter is decremented at enqueue time, so the loop stops
as soon as the last fresh orange is reached and the layer count is the answer.

A `visited` matrix marks rotten oranges before they enter the queue and marks
each fresh orange when it is enqueued, so no cell is processed twice.

Complexity
----------
Time:  O(m * n)  -- each cell is enqueued and inspected at most once
Space: O(m * n)  -- visited matrix plus the BFS queue

Why optimal
-----------
Every cell must be examined at least once to know whether it is fresh, so
Omega(m * n) is a lower bound and the single BFS pass meets it. The queue and
visited matrix are linear in the grid, which is unavoidable for a level-order
traversal that must remember the frontier.

Edge cases
----------
- No fresh oranges at the start: return 0, even if the queue is empty.
- Fresh oranges but no rotten source: the queue is empty, return -1.
- Fresh oranges disconnected from every source: the queue drains with
  `fresh > 0`, return -1.
- A single cell that is fresh (return -1) or rotten (return 0).
- All-empty grid (no fresh, no rotten): return 0.

Pitfalls
--------
- Returning the layer count without checking that every fresh orange rotted.
- Marking fresh cells only when popped, which lets duplicates into the queue.
- Incrementing the minute after processing a layer instead of before, or
  returning `minutes + 1`.
- Using DFS: the answer is a shortest-path distance, so BFS is required.

Video
-----
(not published yet)
"""

from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        rows = len(grid)
        cols = len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    fresh += 1
                elif grid[row][col] == 2:
                    visited[row][col] = True
                    queue.append((row, col))

        if fresh == 0:
            return 0

        minutes = 0
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                row, col = queue.popleft()
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and not visited[nr][nc]
                        and grid[nr][nc] == 1
                    ):
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        fresh -= 1

        return minutes if fresh == 0 else -1


def _self_test() -> None:
    from copy import deepcopy

    s = Solution()

    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    assert s.orangesRotting(deepcopy(grid)) == 4

    grid = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    assert s.orangesRotting(deepcopy(grid)) == -1

    grid = [[0, 2]]
    assert s.orangesRotting(deepcopy(grid)) == 0

    grid = [[0, 0], [0, 0]]
    assert s.orangesRotting(deepcopy(grid)) == 0

    grid = [[1, 1]]
    assert s.orangesRotting(deepcopy(grid)) == -1

    grid = [[1]]
    assert s.orangesRotting(deepcopy(grid)) == -1

    grid = [[2]]
    assert s.orangesRotting(deepcopy(grid)) == 0

    grid = [[2, 0], [0, 1]]
    assert s.orangesRotting(deepcopy(grid)) == -1

    grid = [[2, 1, 1, 1, 1]]
    assert s.orangesRotting(deepcopy(grid)) == 4

    grid = [[2, 1, 0, 2, 1]]
    assert s.orangesRotting(deepcopy(grid)) == 1
