"""
752. Open the Lock
https://leetcode.com/problems/open-the-lock/

Difficulty: Medium
Topics: array, breadth-first-search, string

Approach
--------
Model the lock as an unweighted graph: the 10^4 combinations are nodes and
each turn of one wheel connects two nodes with an edge of weight 1. The
answer is the shortest path from "0000" to `target`, so plain BFS suffices.

Start from "0000" unless it is a deadend. For every dequeued state generate
its 8 neighbours (each of the 4 wheels turned up or down with wraparound),
skip deadends and states already seen, and return the depth as soon as the
target is dequeued. Visiting is marked at enqueue time to avoid duplicates.

Complexity
----------
Time:  O(10^4)  -- at most 10^4 states, 8 constant-time neighbours each
Space: O(10^4)  -- visited set, queue and deadend set

Why optimal
-----------
BFS visits every state at most once and, on an unweighted graph, the first
time a node is reached is at its minimum distance, so any algorithm must in
the worst case distinguish all 10^4 combinations: Omega(10^4) is a lower
bound and this meets it. Space is linear in the state space, which is also
required to remember what has been tried.

Edge cases
----------
- `"0000"` in `deadends`: the start is blocked, return -1 immediately.
- Deadends adjacent to or equal to nothing relevant: just skip them.
- No path to the target: the queue drains and returns -1.
- A wheel turning "9" up to "0" and "0" down to "9" (wraparound).

Pitfalls
--------
- Forgetting the wraparound, so "0000" and "9999" are not neighbours.
- Not adding `"0000"` to visited, which can enqueue it again.
- Using DFS or Dijkstra: unnecessary here because all edges have weight 1.
- Building neighbours with `int` and losing leading zeros in the string.

Video
-----
(not published yet)
"""

from collections import deque
from typing import List


class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        blocked = set(deadends)
        if "0000" in blocked:
            return -1
        if target == "0000":
            return 0

        visited = {"0000"}
        queue = deque([("0000", 0)])

        while queue:
            state, turns = queue.popleft()
            for i in range(4):
                digit = int(state[i])
                for step in (-1, 1):
                    new_digit = (digit + step) % 10
                    neighbour = state[:i] + str(new_digit) + state[i + 1:]
                    if neighbour in blocked or neighbour in visited:
                        continue
                    if neighbour == target:
                        return turns + 1
                    visited.add(neighbour)
                    queue.append((neighbour, turns + 1))

        return -1


def _self_test() -> None:
    s = Solution()
    assert s.openLock(["0201", "0101", "0102", "1212", "2002"], "0202") == 6
    assert s.openLock(["8888"], "0009") == 1
    assert s.openLock(["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888") == -1
    assert s.openLock(["0000"], "0009") == -1
    assert s.openLock([], "0000") == 0
    assert s.openLock([], "9999") == 4
