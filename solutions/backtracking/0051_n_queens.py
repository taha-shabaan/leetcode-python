"""
51. N-Queens
https://leetcode.com/problems/n-queens/

Difficulty: Hard
Topics: array, backtracking

Approach
--------
Place one queen per row, choosing a column for each row in turn. A placement is
legal when its column and both of its diagonals are still free:

- a column is identified by `col`;
- a main diagonal (top-left to bottom-right) by `row - col`;
- an anti diagonal (top-right to bottom-left) by `row + col`.

Three sets hold the occupied values, so the legality check is O(1) instead of
scanning previously placed queens. After trying a column we record it, recurse
into the next row, then remove all three markers so sibling branches start
clean. Reaching `row == n` means every row holds a legal queen, so the recorded
column list is formatted into a board.

Complexity
----------
Time:  O(n!)  -- at most n choices for the first row, n-1 distinct columns for
       the next, and so on; diagonal pruning only removes branches. Each leaf
       costs O(n^2) to format, bounded by the O(n! * n^2) output size.
Space: O(n)   -- recursion depth plus the three sets and the column list; the
       output boards add O(n^2) per solution.

Why optimal
-----------
Any correct solver must emit every one of the solutions, and there can be
Theta(n!) partial placements to explore in the worst case, so the exponential
search cannot be avoided. The sets make each node's legality check O(1), which
is the best possible local cost; the O(n) recursion is required to remember the
placement of the current prefix.

Edge cases
---------
- `n <= 0` -> `[]`; there is no board to place.
- `n = 2` and `n = 3` -> `[]`; no valid arrangement exists.
- `n = 1` -> `[["Q"]]`, the smallest non-empty answer.

Pitfalls
--------
- Using `row - col` for both diagonals, or forgetting that the anti diagonal is
  `row + col`, which lets queens attack each other.
- Removing entries with `discard` versus `remove` inconsistently, or failing to
  undo a marker after recursion, leaking state into later branches.
- Formatting the board from the wrong index (e.g. `size` instead of
  `size - col - 1` padding) and producing rows of the wrong length.
"""

from typing import List

EMPTY_CELL = "."
QUEEN_CELL = "Q"


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        if n <= 0:
            return []

        occupied_cols = set()
        occupied_main_diags = set()
        occupied_anti_diags = set()
        queen_cols: List[int] = []
        queens: List[List[str]] = []

        def is_safe(row: int, col: int) -> bool:
            main_diag = row - col
            anti_diag = row + col
            return (
                col not in occupied_cols
                and main_diag not in occupied_main_diags
                and anti_diag not in occupied_anti_diags
            )

        def dfs(row: int) -> None:
            if row == n:
                queens.append(self._format_sol(queen_cols, n))
                return

            for col in range(n):
                if not is_safe(row, col):
                    continue

                main_diag = row - col
                anti_diag = row + col

                queen_cols.append(col)
                occupied_cols.add(col)
                occupied_main_diags.add(main_diag)
                occupied_anti_diags.add(anti_diag)

                dfs(row + 1)

                queen_cols.pop()
                occupied_cols.remove(col)
                occupied_main_diags.remove(main_diag)
                occupied_anti_diags.remove(anti_diag)

        dfs(0)
        return queens

    @staticmethod
    def _format_sol(col_queens: List[int], size: int) -> List[str]:
        return [
            EMPTY_CELL * col + QUEEN_CELL + EMPTY_CELL * (size - col - 1)
            for col in col_queens
        ]


def _self_test() -> None:
    s = Solution()

    assert s.solveNQueens(1) == [["Q"]]
    assert s.solveNQueens(2) == []
    assert s.solveNQueens(3) == []
    assert s.solveNQueens(4) == [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."],
    ]
    assert len(s.solveNQueens(8)) == 92
    assert len(s.solveNQueens(0)) == 0

    for board in s.solveNQueens(6):
        assert len(board) == 6
        assert all(len(row) == 6 and row.count("Q") == 1 for row in board)
