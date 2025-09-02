# 53. Maximum Subarray

# Given an integer array nums, find the subarray with the largest sum, and return its sum.

 

# Example 1:

# Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
# Output: 6
# Explanation: The subarray [4,-1,2,1] has the largest sum 6.
# Example 2:

# Input: nums = [1]
# Output: 1
# Explanation: The subarray [1] has the largest sum 1.
# Example 3:

# Input: nums = [5,4,-1,7,8]
# Output: 23
# Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
 

# Constraints:

# 1 <= nums.length <= 105
# -104 <= nums[i] <= 104
 

# Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # this is brute force appraoch, which is not working, ERROR: TIME EXCEEDING for some inputs.
        # current_max = max(nums)
        # temp = 0
        # for i in range(len(nums)):
        #     temp = nums[i]
        #     for j in range(i+1, len(nums)):
        #         temp += nums[j]
        #         current_max = max(temp, current_max)
        # return current_max
        
        # Time complexity O(1)
        prefix = nums[0]
        l = 0
        for r in range(len(nums)):
            if l < 0:
                l = 0
            l += nums[r]
            prefix = max(l, prefix)

        return prefix