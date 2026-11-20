"""
93. Restore IP Addresses
https://leetcode.com/problems/restore-ip-addresses/

Difficulty: Medium
Topics: string, backtracking

Approach
--------
An IP address is exactly four segments of 1..3 characters. Try every split with
DFS: at each step pick a segment of length 1, 2 or 3 starting at the current
index, reject it if it is invalid (leading zero with more than one digit, or
value above 255), append it to the path and recurse from the next index. When
four segments have been built, it is a valid address only if the whole string
was consumed.

Pruning that matters:
- a leading zero is only legal for the single digit "0";
- a segment longer than 3 characters cannot exist;
- stop as soon as four segments are chosen, but only record when `start`
  equals `len(s)`;
- any input shorter than 4 or longer than 12 characters has no answer.

Complexity
----------
Time:  O(3^4 * n)  -- at most 3^4 = 81 candidate splits, each costing O(n) to
       slice and join; with four fixed segments this is O(n) in the input size
Space: O(4) recursion depth, plus O(3^4 * n) for the returned strings

Why optimal
-----------
Every valid address corresponds to a distinct choice of the three split
points, so a correct solution must at least inspect each candidate split. The
search tree has at most 81 leaves and no node is visited unless it is a
prefix of a possible address, so the work is proportional to the (bounded)
answer space: no algorithm can do better than the output size.

Edge cases
----------
- "0000" -> ["0.0.0.0"]: each zero is a legal one-digit segment.
- "010010" -> ["0.10.0.10", "0.100.1.0"]; "01" must be rejected.
- "101023" -> five addresses; several splits are valid at once.
- Inputs with fewer than 4 or more than 12 characters return [].
- Segments like "256" or "999" are rejected by the 255 check.

Pitfalls
--------
- Accepting "00", "01", "001" (leading zeros).
- Recording the address when four segments exist even if characters remain.
- Using `break` instead of `continue` when a segment is invalid: a longer
  segment may still be valid (e.g. "1" ok, "10" ok, "100" ok, then stop at 4
  digits). Only the length bound justifies `break`.
- Forgetting `path.pop()` after the recursive call.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        result: List[str] = []
        if not 4 <= len(s) <= 12:
            return result

        path: List[str] = []

        def backtrack(start: int) -> None:
            if len(path) == 4:
                if start == len(s):
                    result.append(".".join(path))
                return

            for length in range(1, 4):
                if start + length > len(s):
                    break

                segment = s[start:start + length]
                if length > 1 and segment[0] == "0":
                    continue
                if int(segment) > 255:
                    continue

                path.append(segment)
                backtrack(start + length)
                path.pop()

        backtrack(0)
        return result


def _self_test() -> None:
    s = Solution()
    assert s.restoreIpAddresses("25525511135") == ["255.255.11.135", "255.255.111.35"]
    assert s.restoreIpAddresses("0000") == ["0.0.0.0"]
    assert s.restoreIpAddresses("101023") == [
        "1.0.10.23",
        "1.0.102.3",
        "10.1.0.23",
        "10.10.2.3",
        "101.0.2.3",
    ]
    assert s.restoreIpAddresses("010010") == ["0.10.0.10", "0.100.1.0"]
    assert s.restoreIpAddresses("1111") == ["1.1.1.1"]
    assert s.restoreIpAddresses("999999999999") == []
    assert s.restoreIpAddresses("123") == []
    assert s.restoreIpAddresses("1234567890123") == []
