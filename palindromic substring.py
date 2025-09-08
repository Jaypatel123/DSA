# 647. Palindromic Substrings

# Given a string s, return the number of palindromic substrings in it.

# A string is a palindrome when it reads the same backward as forward.

# A substring is a contiguous sequence of characters within the string.

 

# Example 1:

# Input: s = "abc"
# Output: 3
# Explanation: Three palindromic strings: "a", "b", "c".
# Example 2:

# Input: s = "aaa"
# Output: 6
# Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
 

# Constraints:

# 1 <= s.length <= 1000
# s consists of lowercase English letters.


class Solution:
    def countSubstrings(self, s: str) -> int:
        count = len(s)
        l = 0
        for i in range(1, len(s)):
            while i < len(s):
                window_size = s[l:i+1]
                if window_size == window_size[::-1]:
                    count += 1
                i += 1
                l += 1
            l = 0
        return count 

        # count = len(s)
        # for r in range(1, len(s)):
        #     for j in range(len(s) - 1):
        #         if r <= len(s)-1:
        #             window_size = s[j:r+1]
        #             if window_size == window_size[::-1]:
        #                 count += 1
        #             r += 1
        # return count