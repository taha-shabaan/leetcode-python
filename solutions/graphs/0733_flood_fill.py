"""
733. Flood Fill
https://leetcode.com/problems/flood-fill/

Difficulty: Easy
Topics: array, depth-first-search, breadth-first-search, matrix

Approach
--------
The starting pixel belongs to a 4-connected region of same-coloured pixels.
Flood that region with an iterative DFS: recolor the start, push it on a
stack, and for every popped pixel push each in-bounds neighbour that still
has the original colour, recoloring it as it is pushed. Recoloring is the
visited marker, so each pixel is pushed at most once.

If the start already has the target colour, return immediately: otherwise
neighbouring pixels still "match" and the traversal would never make
progress (or, with a separate visited set, would do pointless work).

DFS is used instead of recursion so a 50x50 all-one-colour image cannot
overflow Python's recursion limit.

Complexity
----------
Time:  O(m * n)  -- every pixel is read once and pushed at most once
Space: O(m * n)  -- worst-case stack for one huge region (plus image mutation)

Why optimal
-----------
Whether a pixel is part of the region is not known until it is inspected, so
any correct algorithm must read all m*n pixels in the worst case: Omega(m*n)
time. Each pixel is processed a constant number of times here, so the bound
is tight. Space is the DFS frontier; BFS reaches the same asymptotics.

Edge cases
----------
- Start colour already equals the target colour: return the image unchanged.
- Single pixel: recolor it and stop.
- Region touching the borders: neighbour checks must not wrap around.
- 1xN or Nx1 image: only two neighbours per pixel exist.

Pitfalls
--------
- Recursing without an early return when `image[sr][sc] == color`, which
  loops forever because the recoloured pixels keep matching.
- Clearing the visited mark after returning from recursion, which lets the
  same pixel be re-entered through another path and blows up exponentially.
- Checking bounds after indexing neighbours.
- Using `row == rows and col == cols` as a boundary check: it never fires.
- Recursive DFS on a large uniform image hitting Python's recursion limit.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        original = image[sr][sc]
        if original == color:
            return image

        rows, cols = len(image), len(image[0])
        image[sr][sc] = color
        stack = [(sr, sc)]

        while stack:
            row, col = stack.pop()
            for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original:
                    image[nr][nc] = color
                    stack.append((nr, nc))

        return image


def _self_test() -> None:
    s = Solution()

    assert s.floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1],
    ]
    assert s.floodFill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [
        [0, 0, 0],
        [0, 0, 0],
    ]
    assert s.floodFill([[0, 0, 0], [0, 1, 1]], 1, 1, 1) == [
        [0, 0, 0],
        [0, 1, 1],
    ]
    assert s.floodFill([[1]], 0, 0, 5) == [[5]]
    assert s.floodFill([[1, 0, 1]], 0, 0, 2) == [[2, 0, 1]]
    assert s.floodFill([[1], [0], [1]], 0, 0, 3) == [[3], [0], [1]]
