# 238. Product of Array Except Self

# Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

# You must write an algorithm that runs in O(n) time and without using the division operation.

# Example 1:

# Input: nums = [1,2,3,4]
# Output: [24,12,8,6]
# Example 2:

# Input: nums = [-1,1,0,-3,3]
# Output: [0,0,9,0,0]
 
# Constraints:

# 2 <= nums.length <= 105
# -30 <= nums[i] <= 30
# The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.
 

# Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        prefixNums = [nums[0]]
        ans = []
        count = 0
        for i in range(0, len(nums)):
            if i == 0 and nums[i] != 0:
                continue
            if i == 0 and nums[i] == 0:
                count += 1
                prefixNums.append(prefixNums[i+1]) 
            elif nums[i] == 0: 
                count += 1
                prefixNums.append(prefixNums[i-1]) 
            else:
                prefixNums.append(prefixNums[i-1] * nums[i])
        print(prefixNums)
        if count >= 2:
            return [0] * len(nums)
        for j in range(len(prefixNums)):
            if count == 0:
                ans.append(prefixNums[-1] // nums[j])
            else:
                ans.append(0) if nums[j] != 0 else ans.append(prefixNums[-1]) 
        return ans