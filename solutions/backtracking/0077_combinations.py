"""
[77. Combinations](https://leetcode.com/problems/combinations/)
https://leetcode.com/problems/combinations/

Difficulty: Medium
Topics: backtracking

Approach
--------
Build each combination in increasing order so it is generated exactly once.
Start the next scan at `start` (the value after the last one chosen) and stop
as soon as the path holds `k` numbers, recording a copy. Because every branch
only ever appends larger values, no duplicate or reordered combination can
appear and no "already used" set is needed.

Bound pruning: when the path has `d` numbers, `k - d` more are required from
the range `[start, n]`, so `start` can be at most `n - (k - d) + 1`. Capping
the loop there skips branches that cannot possibly reach length `k`, without
changing the set of answers.

Complexity
----------
Time:  O(k * C(n, k))  -- C(n, k) combinations, each copied in O(k)
Space: O(k)            -- recursion depth and the current path; output is
                          O(k * C(n, k))

Why optimal
-----------
The answer contains C(n, k) combinations and each must be written out, so
Omega(k * C(n, k)) is a lower bound; this meets it. The `start` bound means
the search tree contains only prefixes that can still be completed to size
`k`, so no dead branch is explored.

Edge cases
----------
- k == 1 -> [[1], [2], ..., [n]].
- k == n -> [[1, 2, ..., n]]: the bound forces the single full range.
- n == 1, k == 1 -> [[1]].
- The constraints guarantee 1 <= k <= n, so no empty combination is produced.

Pitfalls
--------
- Forgetting to `return` after recording, which keeps extending the path
  past length `k` and wastes work (the output can still be right, but the
  recursion is not pruned).
- Looping from a fixed `1` each time without a `used` check, which yields
  ordered permutations instead of combinations.
- Appending `path` without a copy, aliasing one list across every answer.
- Off-by-one in the bound: it must be `n - (k - len(path)) + 1` inclusive.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int) -> None:
            if len(path) == k:
                result.append(path[:])
                return

            remaining = k - len(path)
            for num in range(start, n - remaining + 2):
                path.append(num)
                backtrack(num + 1)
                path.pop()

        backtrack(1)
        return result


def _self_test() -> None:
    s = Solution()
    assert s.combine(4, 2) == [
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4],
    ]
    assert s.combine(1, 1) == [[1]]
    assert s.combine(4, 4) == [[1, 2, 3, 4]]
    assert s.combine(4, 1) == [[1], [2], [3], [4]]
    assert s.combine(5, 3) == [
        [1, 2, 3],
        [1, 2, 4],
        [1, 2, 5],
        [1, 3, 4],
        [1, 3, 5],
        [1, 4, 5],
        [2, 3, 4],
        [2, 3, 5],
        [2, 4, 5],
        [3, 4, 5],
    ]
    assert len(s.combine(20, 10)) == 184756
