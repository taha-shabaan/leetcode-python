"""
212. Word Search II
https://leetcode.com/problems/word-search-ii/

Difficulty: Hard
Topics: array, string, backtracking, trie, matrix

Approach
--------
Searching every word independently is too slow: each word repeats the same
grid walk. Instead, put all words in a trie and do one DFS per grid cell,
walking the trie in lockstep with the board. A cell move is only allowed if
the trie has a child for that letter, so a branch dies the moment no word can
still be formed.

When a DFS reaches a terminal trie node, record the word and then clear that
node's `word` field. This both deduplicates the answer and prunes the trie: a
word already found can never be reported again, and its leaf path stops
matching.

Complexity
----------
Time:  O(m * n * 4 * 3^(L-1) + total_word_length)
       Each starting cell explores at most 4 directions, and every later step
       has at most 3 (the previous cell cannot be reused), bounded by the
       longest word length L. Building the trie costs the total word length.
Space: O(total_word_length) for the trie, plus O(L) recursion depth

Why optimal
-----------
The trie makes the shared prefix of all words be traversed once per board
path instead of once per word, which is what removes the repeated work that
causes TLE. The search still must consider every board path that could spell a
word prefix, so the grid traversal bound is inherent.

Edge cases
---------
- A word longer than the number of cells cannot be found; it is pruned by the
  DFS naturally.
- Duplicate words are returned once because the terminal node is cleared.
- `words` may contain a word that is a prefix of another ("a" and "ab"); both
  must be recorded when their terminal nodes are reached.
- A 1x1 board with the single letter as a word.

Pitfalls
--------
- Building a set of words and calling `startswith` at every node is O(words)
  per step and TLEs on large inputs; the trie is what fixes it.
- Forgetting to unmark `visited` (or mutate the board temporarily and restore)
  leaks state into sibling branches.
- Not clearing a found word's terminal marker returns duplicates.
- Re-checking the starting cell's neighbors against the trie root is
  unnecessary work; only follow existing children.

Video
-----
(not published yet)
"""

from typing import Dict, List


class TrieNode:
    __slots__ = ("children", "is_word", "word")

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False
        self.word: str | None = None


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        if not board or not board[0] or not words:
            return []

        def insert(word: str, root: TrieNode) -> None:
            node = root
            for char in word:
                node = node.children.setdefault(char, TrieNode())
            node.is_word = True
            node.word = word

        root = TrieNode()
        for word in words:
            insert(word, root)

        rows, cols = len(board), len(board[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        found: List[str] = []

        def dfs(row: int, col: int, node: TrieNode) -> None:
            char = board[row][col]
            child = node.children[char]

            if child.word is not None:
                found.append(child.word)
                child.word = None
                child.is_word = False

            board[row][col] = "#"
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in child.children:
                    dfs(nr, nc, child)
            board[row][col] = char

        for row in range(rows):
            for col in range(cols):
                if board[row][col] in root.children:
                    dfs(row, col, root)

        return found


def _self_test() -> None:
    s = Solution()
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    assert sorted(s.findWords(board, ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]

    assert s.findWords([["a", "b"], ["c", "d"]], ["abcb"]) == []
    assert s.findWords([["a", "a"]], ["aaa"]) == []
    assert s.findWords([["a"]], ["a"]) == ["a"]
    assert sorted(s.findWords([["a", "b"], ["c", "d"]], ["a", "ab", "abc"])) == ["a", "ab"]

    dupes = [["e", "a", "t"]]
    assert s.findWords(dupes, ["eat", "eat"]) == ["eat"]
