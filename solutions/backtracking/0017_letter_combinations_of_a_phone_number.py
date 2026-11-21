"""
[17. Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Difficulty: Medium
Topics: string, backtracking

Approach
--------
Map each digit to its letters, then walk the digits left to right with DFS.
At position `ind` try every letter for `digits[ind]`, append it to the path,
recurse on `ind + 1`, and pop it on the way back. When `ind` reaches
`len(digits)` the path is one full combination, so join it and record it.

The empty input is special: with no digits there is no combination to build,
so return `[]` rather than `[""]` (the base case would otherwise fire once
with an empty path).

Complexity
----------
Time:  O(n * 4^n)  -- at most 4 letters per digit, so <= 4^n leaves, each
       joined in O(n)
Space: O(n)        -- recursion depth and the path; output is O(n * 4^n)

Why optimal
-----------
The answer can contain 4^n strings of length n, and every one must be
constructed, so Omega(n * 4^n) is a lower bound; this meets it. Each
recursive step does O(1) work per letter apart from the final join, so no
work is spent on prefixes that do not lead to an output.

Edge cases
----------
- "" -> [] (not [""]): there are zero digits and therefore zero combinations.
- "2" -> ["a", "b", "c"].
- "7" and "9" have four letters; "1" and "0" are not valid digits under the
  constraints.
- Repeated digits, e.g. "22" -> 9 two-letter combinations.

Pitfalls
--------
- Returning [""] for the empty string instead of [].
- Indexing `digits[ind]` before checking the base case, which crashes on "".
- Forgetting `path.pop()` after the recursive call, so letters leak into
  sibling branches.
- Building the string with repeated concatenation inside the loop instead of
  joining once at a leaf (works, but adds O(n) per node).

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        phone = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        result: List[str] = []
        path: List[str] = []

        def backtrack(ind: int) -> None:
            if ind == len(digits):
                result.append("".join(path))
                return

            for letter in phone[digits[ind]]:
                path.append(letter)
                backtrack(ind + 1)
                path.pop()

        backtrack(0)
        return result


def _self_test() -> None:
    s = Solution()
    assert s.letterCombinations("23") == [
        "ad",
        "ae",
        "af",
        "bd",
        "be",
        "bf",
        "cd",
        "ce",
        "cf",
    ]
    assert s.letterCombinations("") == []
    assert s.letterCombinations("2") == ["a", "b", "c"]
    assert s.letterCombinations("7") == ["p", "q", "r", "s"]
    assert s.letterCombinations("9") == ["w", "x", "y", "z"]
    assert len(s.letterCombinations("22")) == 9
    assert len(s.letterCombinations("234")) == 27
    assert len(s.letterCombinations("7777")) == 256
