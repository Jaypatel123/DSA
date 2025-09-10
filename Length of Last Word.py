Length of Last Word

Given a string s consisting of words and spaces, return the length of the last word in the string.

A word is a maximal substring consisting of non-space characters only.

 

Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.
    
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        # Using inbuilt functions
        count = 0
        for i in range(len(s)-1,-1,-1):
            if s[i].isalpha():
                count += 1
            elif not s[i].isalpha() and count > 0:
                return count
        return count
        
        # Using inbuilt functions
        s = s.strip()
        count = 0
        for i in range(len(s)-1,-1,-1):
            if s[i] == " ":
                break
            count += 1
        return count

        # not using inbuild functions
        i, length = len(s) - 1, 0
        while s[i] == " ":
            i -= 1
        while i >= 0 and s[i] != " ":
            length += 1
        return length