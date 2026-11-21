"""
47. Permutations II
https://leetcode.com/problems/permutations-ii/

Difficulty: Medium
Topics: array, backtracking

Approach
--------
Sort the input so equal values sit next to each other, then run the standard
"used" backtracking from problem 46. The only addition is the duplicate rule:
when scanning positions left to right, skip `nums[i]` if it equals the
previous value and that previous value is not currently used. That condition
means "an identical value could have been placed at this same spot in this
branch, so this branch is a duplicate of one already explored" -- pruning it
removes repeated permutations before they are ever built.

The sort plus the `not used[i - 1]` check replaces the naive
`if perm not in ans` deduplication, which would build every duplicate
permutation and then scan the whole answer list for each one.

Complexity
----------
Time:  O(n * n!)  -- worst case all values distinct; each leaf is copied in O(n)
Space: O(n)       -- recursion depth, `used` array, and sort buffer

Why optimal
-----------
The output can contain n! distinct permutations (all values distinct), and
each must be produced and copied, so Omega(n * n!) is a lower bound that this
meets. The dedup rule costs O(1) per branch and prevents any duplicate leaf
from being constructed, so no work is wasted on permutations that would be
thrown away.

Edge cases
----------
- All equal, e.g. [1, 1, 1] -> [[1, 1, 1]]: only one branch survives.
- Mixed duplicates, e.g. [1, 1, 2] -> three permutations, not six.
- Distinct values: behaves exactly like problem 46, n! results.
- Negative numbers sort and compare normally.
- A single element -> [[x]].

Pitfalls
--------
- Using `if nums[i] == nums[i - 1]: continue` without the `not used[i - 1]`
  guard, which wrongly kills legitimate branches that place the duplicate
  value deeper in the same permutation.
- Forgetting to sort first, so equal values are not adjacent and the rule
  never fires.
- Deduplicating with `perm not in ans`, which is O(n! * n) per leaf and blows
  up on large inputs.
- Appending `perm` without a copy, aliasing the same list across answers.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        nums.sort()
        result: List[List[int]] = []
        path: List[int] = []
        used = [False] * n

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return

            for i in range(n):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue

                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result


class SolutionAlternative:
    """Same pruning rule, written with an explicit depth argument and index loop."""

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ans: List[List[int]] = []
        perm: List[int] = []
        used = [False] * n

        def backtracking(s: int) -> None:
            if s == n:
                ans.append(perm[:])
                return

            for i in range(n):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue

                perm.append(nums[i])
                used[i] = True

                backtracking(s + 1)

                perm.pop()
                used[i] = False

        backtracking(0)
        return ans


def _self_test() -> None:
    for cls in (Solution, SolutionAlternative):
        s = cls()
        assert s.permuteUnique([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
        assert s.permuteUnique([1, 2, 3]) == [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1],
        ]
        assert s.permuteUnique([1, 1, 1]) == [[1, 1, 1]]
        assert s.permuteUnique([2, 2, 1, 1]) == [
            [1, 1, 2, 2],
            [1, 2, 1, 2],
            [1, 2, 2, 1],
            [2, 1, 1, 2],
            [2, 1, 2, 1],
            [2, 2, 1, 1],
        ]
        assert s.permuteUnique([1]) == [[1]]
        assert s.permuteUnique([-1, -1, 2]) == [[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]
        assert len(s.permuteUnique([1, 1, 2, 2, 3])) == 30
