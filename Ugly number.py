# 263. Ugly Number

# An ugly number is a positive integer which does not have a prime factor other than 2, 3, and 5.

# Given an integer n, return true if n is an ugly number.

 

# Example 1:

# Input: n = 6
# Output: true
# Explanation: 6 = 2 × 3
# Example 2:

# Input: n = 1
# Output: true
# Explanation: 1 has no prime factors.
# Example 3:

# Input: n = 14
# Output: false
# Explanation: 14 is not ugly since it includes the prime factor 7.
 

# Constraints:

# -231 <= n <= 231 - 1

class Solution:
    def isUgly(self, n: int) -> bool:
        if n < 1:
            return False
        while n > 1:
            if n%5 == 0:
                n = n/5
            elif n%3 == 0:
                n = n/3
            elif n%2 == 0:
                n = n/2
            else:
                return False
        return True