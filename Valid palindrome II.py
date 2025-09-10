# 680. Valid Palindrome II

# Given a string s, return true if the s can be palindrome after deleting at most one character from it.

 

# Example 1:

# Input: s = "aba"
# Output: true
# Example 2:

# Input: s = "abca"
# Output: true
# Explanation: You could delete the character 'c'.
# Example 3:

# Input: s = "abc"
# Output: false
 

# Constraints:

# 1 <= s.length <= 105
# s consists of lowercase English letters.

class Solution:
    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1

        while l <= r:
            if s[l] != s[r]:
                left = s[:l] + s[l+1:]
                right = s[:r] + s[r+1:]
                if left == left[::-1]:
                    return True
                elif right == right[::-1]:
                    return True
                else:
                    return False
            l += 1
            r -= 1
        return True