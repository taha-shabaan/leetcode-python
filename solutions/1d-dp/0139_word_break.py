"""
[139. Word Break](https://leetcode.com/problems/word-break/)
https://leetcode.com/problems/word-break/

Difficulty: Medium
Topics: string, dynamic-programming, backtracking, trie, memoization

Approach
--------
Let `dp[i]` mean "the prefix `s[:i]` can be split into dictionary words".
`dp[0]` is True (the empty prefix). For each end position `i`, look for a
split `j < i` such that `dp[j]` is True and `s[j:i]` is in the dictionary; if
one exists, `dp[i]` becomes True. The answer is `dp[len(s)]`.

Two details make this fast:
- put the dictionary in a set for O(1) expected membership checks;
- track the longest word `L` and only try splits with `i - j <= L`, since no
  longer substring can ever match. This caps the inner loop at `L` steps.

The alternative class below is the same recurrence expressed top-down with a
memo, which is the natural backtracking formulation.

Complexity
----------
Time:  O(n * L^2)  -- n end positions, up to L split points each, and slicing
       plus hashing a substring of length <= L
Space: O(n)        -- the dp table (the set costs O(total dictionary length))

Why optimal
-----------
A split must be tested at every position where the prefix is reachable, and
there are O(n) positions and O(L) candidate last words, so O(n * L) membership
tests are needed; each test compares up to L characters, giving O(n * L^2).
The DP never re-explores a prefix once its result is known, unlike plain
backtracking which can be exponential on inputs like "aaaa...a".

Edge cases
----------
- "leetcode" with ["leet", "code"] -> True.
- "catsandog" with ["cats", "dog", "sand", "and", "cat"] -> False; reachable
  prefixes exist but the full string cannot be covered.
- Words longer than `s` are ignored by the `L` bound.
- Duplicate words in the dictionary are harmless (the set deduplicates).
- Overlapping words such as ["a", "aa"] require trying every split, not just
  the longest match.

Pitfalls
--------
- Greedily taking the longest matching word, which fails on overlapping cases.
- Forgetting `dp[0] = True`, so no split can ever start.
- Recomputing `s[j:i]` membership without a set, turning the check into a
  linear scan of the dictionary.
- Plain DFS without memoization, which is exponential on repetitive inputs.

Video
-----
(not published yet)
"""

from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        max_len = max((len(w) for w in words), default=0)
        n = len(s)

        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break

        return dp[n]


class SolutionAlternative:
    """Top-down memoized search over reachable prefixes."""

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        max_len = max((len(w) for w in words), default=0)
        n = len(s)
        memo: dict[int, bool] = {}

        def dfs(i: int) -> bool:
            if i == n:
                return True
            if i in memo:
                return memo[i]

            for j in range(i + 1, min(n, i + max_len) + 1):
                if s[i:j] in words and dfs(j):
                    memo[i] = True
                    return True

            memo[i] = False
            return False

        return dfs(0)


def _self_test() -> None:
    for cls in (Solution, SolutionAlternative):
        s = cls()
        assert s.wordBreak("leetcode", ["leet", "code"]) is True
        assert s.wordBreak("applepenapple", ["apple", "pen"]) is True
        assert (
            s.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"])
            is False
        )
        assert s.wordBreak("aaaaaaa", ["aaaa", "aaa"]) is True
        assert s.wordBreak("aaaaaaab", ["aaaa", "aaa"]) is False
        assert s.wordBreak("a", ["a"]) is True
        assert s.wordBreak("a", ["b"]) is False
        assert s.wordBreak("cars", ["car", "ca", "rs"]) is True
        assert s.wordBreak("bb", ["a", "b", "bbb", "bbbb"]) is True
        assert s.wordBreak("abcdef", ["abcdefg"]) is False
