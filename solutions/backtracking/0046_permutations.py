"""
46. Permutations
https://leetcode.com/problems/permutations/

Difficulty: Medium
Topics: array, backtracking

Approach
--------
Build permutations position by position. At each depth pick any element that
has not been used yet, append it to the current path, mark it used, recurse,
then undo both changes. When the path has `len(nums)` elements every input
value has been placed exactly once, so the path is a complete permutation and
is copied into the answer.

A `used` boolean array makes the "is this value already in the path?" check
O(1) instead of scanning the path, which is the only difference from the
naive `if nums[i] in perm` version.

Complexity
----------
Time:  O(n * n!)  -- there are n! leaves; copying each path costs O(n)
Space: O(n)       -- recursion depth plus the `used` array; output is O(n * n!)

Why optimal
-----------
The output itself contains n! permutations of n elements, and every one must
be produced and copied, so Omega(n * n!) time is a lower bound. Generating
each leaf in O(1) amortised work and copying in O(n) meets it. The O(n)
auxiliary space is also necessary: the recursion must remember which values
are currently placed.

Edge cases
----------
- A single element -> [[x]]; the loop still produces one leaf.
- Duplicate values are not a concern here because the problem guarantees
  distinct integers (that is problem 47, Permutations II).
- The empty list is not valid input under the constraints, but the code
  returns [[]] for it.

Pitfalls
--------
- Forgetting to unmark `used[i]` (or to `pop`) after the recursive call, which
  leaks state into sibling branches.
- Appending `path` directly instead of a copy, so every answer aliases the
  same mutable list and ends up empty.
- Testing membership with `x in path` (O(n) per choice) instead of a `used`
  array, turning the inner work into O(n^2) per node.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
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
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result


def _self_test() -> None:
    s = Solution()
    assert s.permute([1, 2, 3]) == [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert s.permute([0, 1]) == [[0, 1], [1, 0]]
    assert s.permute([1]) == [[1]]
    assert s.permute([]) == [[]]
    assert len(s.permute([1, 2, 3, 4])) == 24
    assert sorted(s.permute([1, 2, 3, 4])) == sorted(
        [list(p) for p in __import__("itertools").permutations([1, 2, 3, 4])]
    )
