"""
155. Min Stack
https://leetcode.com/problems/min-stack/

Difficulty: Medium
Topics: stack, design

Approach
--------
Each stack entry stores a pair: the pushed value and the minimum of the whole
stack at the moment it was pushed. Pushing computes min(value, current_min);
popping simply drops one pair, which restores the previous minimum for free.
`getMin` reads the second field of the top pair.

Complexity
----------
Time:  O(1) per operation (push, pop, top, getMin)
Space: O(n)  -- two integers per stack element

Why optimal
-----------
All four operations only touch the top of the stack, so O(1) is the floor
for each of them. The space is optimal as well: after a pop the structure
must be able to report the previous minimum, and since the only way values
leave is LIFO, at least one minimum must be remembered per stack level in
the worst case (a strictly decreasing push sequence). Hence Omega(n) space.

Edge cases
----------
- Duplicate minimums: stored per level, so popping one copy restores the
  same minimum rather than losing it.
- Negative values: `min` handles them, no sentinel needed.
- `pop`, `top` and `getMin` are only called on a non-empty stack by the
  problem guarantees.

Pitfalls
--------
- Keeping a single `min` variable fails when the minimum is popped.
- Pushing the minimum only when it changes makes duplicate-minimum pops
  incorrect unless the counts are tracked.

Video
-----
(not published yet)
"""


class MinStack:
    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def getMin(self) -> int:
        return self._stack[-1][1]


def _self_test() -> None:
    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.getMin() == -3
    s.pop()
    assert s.top() == 0
    assert s.getMin() == -2

    d = MinStack()
    d.push(0)
    d.push(1)
    d.push(0)
    assert d.getMin() == 0
    d.pop()
    assert d.getMin() == 0
    d.pop()
    assert d.getMin() == 0
