# 

# solution from neetcode
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        ans = max(nums)
        max_val, min_val = 1, 1
        for i in nums:
            if i == 0:
                max_val, min_val = 1, 1
                continue
            tmp = max_val * i
            max_val = max(max_val * i, min_val * i, i)
            min_val = min(tmp, min_val * i, i)
            ans = max(ans, max_val)
        return ans