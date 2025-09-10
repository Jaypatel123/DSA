# 367. Valid Perfect Square

# Given a positive integer num, return true if num is a perfect square or false otherwise.

# A perfect square is an integer that is the square of an integer. In other words, it is the product of some integer with itself.

# You must not use any built-in library function, such as sqrt.

 

# Example 1:

# Input: num = 16
# Output: true
# Explanation: We return true because 4 * 4 = 16 and 4 is an integer.
# Example 2:

# Input: num = 14
# Output: false
# Explanation: We return false because 3.742 * 3.742 = 14 and 3.742 is not an integer.
 

# Constraints:

# 1 <= num <= 231 - 1


class Solution:
    def isPerfectSquare(self, num: int) -> bool:
    
    # Binary (log n)
        l, r = 1, num
        while l <= r:
            m = (l + r) // 2
            if m * m > num: 
                r = m - 1
            elif m * m < num:
                l = m + 1
            else:
                return True
        return False
    
    # for loop
        # for i in range(num+1):
        #     if i * i == num:
        #         return True
        #     if i * i > num:
        #         return False
    
    # Newton's method
        # x = num
        # while x * x > num:
        #     x = (x + num // x) // 2
        # return x * x == num

    
