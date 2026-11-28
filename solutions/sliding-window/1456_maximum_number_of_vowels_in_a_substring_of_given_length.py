"""
1456. Maximum Number of Vowels in a Substring of Given Length
https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/

Difficulty: Medium
Topics: string, sliding-window

Approach
--------
Every substring here has the same fixed length `k`, so use a fixed-size sliding
window. Count the vowels in the first window `s[0:k]`, record it, then slide the
window one character at a time: add the entering character `s[right]` and remove
the leaving character `s[right - k]`, updating the vowel count by one for each.
Track the largest count seen. Membership in the vowel set is O(1), so each
character is inspected a constant number of times.

Complexity
----------
Time:  O(n)  -- each character enters and leaves the window at most once
Space: O(1)  -- one vowel set plus two counters, independent of n

Why optimal
-----------
Whether a character is a vowel is only knowable by reading it, so any correct
algorithm must inspect all n characters in the worst case: Omega(n) time. The
window touches each character a constant number of times, making the bound
tight. Only counters and a constant-size set are stored, so O(1) extra space is
also optimal.

Edge cases
----------
- k == n: the first window is the whole string and the slide loop is empty.
- k == 1: every single character is a candidate window.
- All vowels: the answer is k.
- No vowels: the answer is 0.
- n == 1: the loop still initializes and returns correctly.

Pitfalls
----------
- Re-counting every window from scratch, which is O(n * k) and can TLE.
- Removing the wrong index: the character leaving the window is `s[right - k]`,
  not `s[right - k + 1]`.
- Forgetting to seed the count with the first k characters before sliding.
- Off-by-one in the slide loop bounds (`range(k, n)`), missing the last window.
- Treating `y` as a vowel, or forgetting to handle the exact five vowels.

Video
-----
(not published yet)
"""


class Solution:
    def is_vowel(self, char: str) -> bool:
        vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
        return char in vowels

    def maxVowels(self, s: str, k: int) -> int:
        n = len(s)

        vowel_count = 0
        for i in range(k):
            if self.is_vowel(s[i]):
                vowel_count += 1

        best = vowel_count

        for right in range(k, n):
            if self.is_vowel(s[right]):
                vowel_count += 1
            if self.is_vowel(s[right - k]):
                vowel_count -= 1
            best = max(best, vowel_count)

        return best


def _self_test() -> None:
    solver = Solution()

    assert solver.maxVowels("abciiidef", 3) == 3
    assert solver.maxVowels("aeiou", 2) == 2
    assert solver.maxVowels("leetcode", 3) == 2

    assert solver.maxVowels("a", 1) == 1
    assert solver.maxVowels("b", 1) == 0
    assert solver.maxVowels("aeiou", 5) == 5
    assert solver.maxVowels("abcde", 5) == 2
    assert solver.maxVowels("tryhard", 4) == 1
    assert solver.maxVowels("aaa", 2) == 2
    assert solver.maxVowels("bbbb", 2) == 0
    assert solver.maxVowels("a" * 100000, 50000) == 50000
