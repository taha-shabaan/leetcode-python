"""
1. Two Sum
https://leetcode.com/problems/two-sum/

Difficulty: Easy
Topics: array, hash-table

Approach
--------
Walk the array once while keeping a map from value -> index of everything
seen so far. For each number x the partner we need is target - x. If that
partner is already in the map, both indices are known; otherwise store x
and move on.

This replaces the O(n) partner search of the brute force with an O(1)
expected hash lookup, collapsing the O(n^2) double loop into a single pass.

Complexity
----------
Time:  O(n)  -- one pass, O(1) expected per element
Space: O(n)  -- worst case every element is stored before the pair is found

Why optimal
-----------
Every element must be inspected at least once to rule out a pairing, so
Omega(n) time is a lower bound. A single O(n) pass with O(1) lookups meets
it, which no sorting-based O(n log n) approach can beat. The O(n) space is
also required: to answer in one pass you must remember the values already
seen.

Edge cases
----------
- The same value may be used twice, but never the same index: the partner
  is looked up *before* the current index is inserted.
- Negative values and zero need no special handling.
- Exactly one valid answer is guaranteed by the constraints, so the final
  `return []` is unreachable for valid input.

Pitfalls
--------
- Inserting the index before checking lets an element pair with itself.
- Returning the values instead of the indices.
- Sorting the array throws away the original indices.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen: dict[int, int] = {}
        for i, x in enumerate(nums):
            partner = target - x
            if partner in seen:
                return [seen[partner], i]
            seen[x] = i
        return []


def _self_test() -> None:
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    assert s.twoSum([3, 3], 6) == [0, 1]
    assert s.twoSum([-1, -2, -3, -4, -5], -8) == [2, 4]
    assert s.twoSum([0, 4, 3, 0], 0) == [0, 3]
