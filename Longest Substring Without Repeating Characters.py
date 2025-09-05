# 3. Longest Substring Without Repeating Characters

# Given a string s, find the length of the longest substring without duplicate characters.

 

# Example 1:

# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3.
# Example 2:

# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.
# Example 3:

# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # unoptimized problem solving this is solved with O(n^2)
        # longest_str = 0
        # unique_set = set()
        # for i in range(len(s) - longest_str):
        #     unique_set.add(s[i])
        #     for j in range(i+1, len(s)):
        #         if s[j] in unique_set:
        #             unique_set = set()
        #             break
        #         else:
        #             unique_set.add(s[j])
        #         longest_str = max(len(unique_set), longest_str) 
        # return max(len(unique_set), longest_str)

        # neetcode problem solve, optimized
        # l = 0
        # unique_set = set()
        # ans = 0
        # for r in range(len(s)):
        #     while s[r] in unique_set:
        #         unique_set.remove(s[l])
        #         l += 1
        #     unique_set.add(s[r])
        #     ans = max(ans, len(unique_set))
        # return ans   

        # I have used only one loop even though complexity is not good then the one above this 
        l, r = 0, 0
        uni_set = set()
        ans = 0
        while r < len(s):
            if s[r] in uni_set:
                uni_set.remove(s[l])
                l += 1
                continue
            uni_set.add(s[r])
            r += 1
            ans = max(ans, len(uni_set))
        return ans