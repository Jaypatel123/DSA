
# 242. Valid Anagram
# Solved
# Easy
# Topics
# premium lock icon
# Companies
# Given two strings s and t, return true if t is an anagram of s, and false otherwise.

 

# Example 1:

# Input: s = "anagram", t = "nagaram"

# Output: true

# Example 2:

# Input: s = "rat", t = "car"

# Output: false

 

# Constraints:

# 1 <= s.length, t.length <= 5 * 104
# s and t consist of lowercase English letters.
 

# Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

# solving this problem in my way
from collections import defaultdict
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        
        if len(s) != len(t):
            return False

        hash_set = defaultdict(int)

        for i in s:
            hash_set[i] += 1
        print(hash_set)

        for j in t:
            if j not in hash_set:
                return False
            hash_set[j] -= 1
            if hash_set[j] == 0:
                 del hash_set[j]
        return True
    
    
        # in one line return the result , 
        # Counter automatically count each character in the string and by comparing both gives boolean value 
        return Counter(s) == Counter(t)