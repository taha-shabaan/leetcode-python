"""
2271. Maximum White Tiles Covered by a Carpet
https://leetcode.com/problems/maximum-white-tiles-covered-by-a-carpet/

Difficulty: Medium
Topics: array, binary-search, greedy, sorting, prefix-sum, sliding-window

Approach
--------
Sort the tiles by their left endpoint. An optimal carpet can always be slid
right until its left edge lines up with the left endpoint of some tile, so it
is enough to try, for every tile i, a carpet spanning
[tiles[i][0], tiles[i][0] + carpetLen - 1].

Keep a monotonic right pointer over the tiles and a running sum `cover` of the
tiles fully inside the current window. For each left tile i, advance `right`
while the next tile ends before the carpet's end, adding its whole length to
`cover`. If the following tile starts inside the window but extends past it,
add only the covered prefix as `partial`. The answer is the best
`cover + partial`. Before moving i forward, drop tile i from `cover` when it
was fully covered; otherwise bump `right` past it.

Complexity
----------
Time:  O(n log n)  -- dominated by sorting; the two-pointer scan is O(n)
Space: O(n)        -- Timsort's temporary buffer; O(1) extra for the window

Why optimal
-----------
The tiles arrive unsorted and any correct solution must reason about their
order, so a comparison sort's Omega(n log n) is a lower bound here. After
sorting, each tile enters and leaves the window at most once, making the scan
linear and the overall bound tight.

Edge cases
----------
- carpetLen == 1: only a single tile value can be covered.
- One tile, or a carpet longer than every tile combined: the whole total.
- Large gaps between tiles: the window must skip them without counting them.
- Tiles that touch or are adjacent: they still count individually.
- Only part of the next tile fits: `partial` handles it.
- Coordinates up to 1e9: Python integers avoid overflow.

Pitfalls
----------
- Forgetting to sort, which breaks the monotonic right pointer.
- Recomputing the window sum from scratch per i, turning O(n) into O(n^2).
- Off-by-one: intervals are inclusive, so the carpet ends at
  `start + carpetLen - 1`.
- Subtracting tile i from `cover` even when it was only partially covered
  (`right == i`); in that case only `right` should advance.
- In languages with fixed-width integers, `start + carpetLen` can overflow.
"""

from typing import List


class Solution:
    def maximumWhiteTiles(self, tiles: List[List[int]], carpetLen: int) -> int:
        tiles.sort()
        n = len(tiles)
        best = 0
        cover = 0
        right = 0

        for i in range(n):
            end = tiles[i][0] + carpetLen - 1

            while right < n and tiles[right][1] <= end:
                cover += tiles[right][1] - tiles[right][0] + 1
                right += 1

            partial = 0
            if right < n and tiles[right][0] <= end:
                partial = end - tiles[right][0] + 1

            best = max(best, cover + partial)

            if right > i:
                cover -= tiles[i][1] - tiles[i][0] + 1
            else:
                right += 1

        return best


def _self_test() -> None:
    solver = Solution()

    assert solver.maximumWhiteTiles([[1, 5], [10, 11], [12, 18], [20, 25], [30, 32]], 10) == 9
    assert solver.maximumWhiteTiles([[10, 11], [1, 1]], 2) == 2

    assert solver.maximumWhiteTiles([[1, 1]], 1) == 1
    assert solver.maximumWhiteTiles([[1, 10]], 1) == 1
    assert solver.maximumWhiteTiles([[1, 10]], 100) == 10
    assert solver.maximumWhiteTiles([[1, 2], [3, 4]], 10) == 4
    assert solver.maximumWhiteTiles([[1, 2], [10, 12]], 3) == 3
    assert solver.maximumWhiteTiles([[1, 5], [6, 10]], 6) == 6
    assert solver.maximumWhiteTiles([[1, 1000000000]], 1000000000) == 1000000000
    assert solver.maximumWhiteTiles([[5, 5], [9, 9], [13, 13]], 4) == 1
