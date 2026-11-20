"""
704. Binary Search
https://leetcode.com/problems/binary-search/

Difficulty: Easy
Topics: array, binary-search

Approach
--------
Maintain an inclusive window `[lo, hi]`. Look at the middle element: if it is
the target, return it; if it is smaller the answer can only be to the right,
otherwise only to the left. Each step halves the window, so at most
ceil(log2(n + 1)) steps are needed.

Complexity
----------
Time:  O(log n)
Space: O(1)

Why optimal
-----------
A binary comparison has only two outcomes, so a search among n ordered
elements is a decision tree of depth log2(n); Omega(log n) comparisons are
unavoidable in the worst case. This loop performs exactly that many, and
uses constant extra memory.

Edge cases
----------
- Empty array: `lo = 0`, `hi = -1`, loop body never runs, returns -1.
- Target smaller than the first or larger than the last element.
- Single-element array, both hit and miss.
- `lo + hi` can overflow in fixed-width languages; Python integers cannot,
  and `lo + (hi - lo) // 2` is used below to keep the habit portable.

Pitfalls
--------
- Using `lo < hi` with an inclusive `hi` skips the last candidate.
- Forgetting to move `lo` past the midpoint causes an infinite loop.
- Applying this to an unsorted array.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1


def _self_test() -> None:
    s = Solution()
    assert s.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert s.search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert s.search([], 7) == -1
    assert s.search([5], 5) == 0
    assert s.search([5], -5) == -1
