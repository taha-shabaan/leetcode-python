"""
[40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)
https://leetcode.com/problems/combination-sum-ii/

Difficulty: Medium
Topics: array, backtracking

Approach
--------
Sort the candidates, then DFS from a start index. At each level choose one
candidate, recurse from `i + 1` (each number may be used only once), and pop
it on the way back. Record the path when the running sum equals the target.

Two rules keep the output exact:
- skip a value equal to the previous one at the same depth
  (`i > start and candidates[i] == candidates[i - 1]`), which removes
  duplicate combinations that differ only in which copy was picked;
- because the array is sorted, `break` as soon as `sum + candidates[i] >
  target`: every later candidate is at least as large, so none can fit.

Unlike Combination Sum (problem 39), the recursion moves to `i + 1`, not `i`,
because each candidate may be chosen at most once.

Complexity
----------
Time:  O(n * 2^n)  -- each candidate is in or out, so <= 2^n paths; each
       recorded path is copied in O(n)
Space: O(n)        -- recursion depth and the current path; output is
                      O(n * 2^n)

Why optimal
-----------
Any subset of the candidates is a candidate combination, so there can be up
to 2^n of them and each must be built and copied: Omega(n * 2^n) is a lower
bound that this meets. Sorting plus the duplicate skip and the `break` prune
branches that cannot yield a new, valid combination, so no output is
generated twice and no dead branch is expanded.

Edge cases
----------
- Duplicates, e.g. [1, 1, 1], 2 -> [[1, 1]] only (not three copies).
- [2, 5, 2, 1, 2], 5 -> [[1, 2, 2], [5]].
- No solution, e.g. [1], 2 -> [].
- target smaller than the smallest candidate -> [] via the `break`.
- A single candidate equal to target -> [[x]].
- The base case must `return`: otherwise the loop keeps running after a
  match (harmless here only because the next add exceeds the target).

Pitfalls
--------
- Recurring on `i` instead of `i + 1`, which reuses a number and turns this
  into Combination Sum.
- Skipping duplicates with `i > 0` instead of `i > start`, which wrongly
  drops legitimate branches that pick the same value deeper in the path.
- Using `continue` instead of `break` when the sum overflows: with a sorted
  array, `break` is both correct and faster.
- Forgetting to `pop` after the recursive call.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        n = len(candidates)
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, n):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remaining:
                    break

                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return result


def _self_test() -> None:
    s = Solution()
    assert s.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8) == [
        [1, 1, 6],
        [1, 2, 5],
        [1, 7],
        [2, 6],
    ]
    assert s.combinationSum2([2, 5, 2, 1, 2], 5) == [[1, 2, 2], [5]]
    assert s.combinationSum2([1, 1, 1], 2) == [[1, 1]]
    assert s.combinationSum2([1], 2) == []
    assert s.combinationSum2([1], 1) == [[1]]
    assert s.combinationSum2([3, 1, 3, 5, 1, 1], 8) == [
        [1, 1, 1, 5],
        [1, 1, 3, 3],
        [3, 5],
    ]
    assert s.combinationSum2([1, 2, 3], 7) == []
