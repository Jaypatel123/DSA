# Given a string s, return the longest palindromic substring in s.

# Example 1:

# Input: s = "babad"
# Output: "bab"
# Explanation: "aba" is also a valid answer.
# Example 2:

# Input: s = "cbbd"
# Output: "bb"
 

# Constraints:

# 1 <= s.length <= 1000
# s consist of only digits and English letters.

class Solution:
    def longestPalindrome(self, s: str) -> str:
        ans = s[0]
        l = 0
        if len(s) < 2:
            return s
        for r in range(1, len(s)):
            while r < len(s):
                window_size = s[l:r+1]
                if window_size == window_size[::-1]:
                    ans = window_size
                    break
                r += 1
                l += 1
            l = 0
        return ans