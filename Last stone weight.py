# 1046. Last Stone Weight

# You are given an array of integers stones where stones[i] is the weight of the ith stone.

# We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

# If x == y, both stones are destroyed, and
# If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
# At the end of the game, there is at most one stone left.

# Return the weight of the last remaining stone. If there are no stones left, return 0.

 

# Example 1:

# Input: stones = [2,7,4,1,8,1]
# Output: 1
# Explanation: 
# We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
# we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
# we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
# we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.
# Example 2:

# Input: stones = [1]
# Output: 1
 

# Constraints:

# 1 <= stones.length <= 30
# 1 <= stones[i] <= 1000

from collections import defaultdict 
import heapq
from typing import List
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        # 1. Using Hashmap
        weight_hash = defaultdict(int)
        for i in stones:
            weight_hash[i] += 1
        counter = len(stones)
        while counter > 1:
            largest_val = 0
            if weight_hash[max(weight_hash)] > 1:
                weight_hash[max(weight_hash)] -= 1
                largest_val = max(weight_hash)
            else:
                largest_val = max(weight_hash)
                weight_hash.pop(largest_val)
            second_largest = 0
            if weight_hash[max(weight_hash)] > 1:
                weight_hash[max(weight_hash)] -= 1
                second_largest = max(weight_hash)
            else:
                second_largest = max(weight_hash)
                weight_hash.pop(second_largest)
            temp = largest_val - second_largest
            if temp != 0:
                weight_hash[temp] += 1
                counter -= 1
            else:
                counter -= 2
        return max(weight_hash) if weight_hash else 0
        
        # 2. Using Heap
        # stones = [-s for s in stones]
        # heapq.heapify(stones)

        # while len(stones) > 1:
        #     largest_val = -heapq.heappop(stones)
        #     second_largest = -heapq.heappop(stones)

        #     if largest_val != second_largest:
        #         heapq.heappush(stones, -(largest_val - second_largest))
        
        # return -stones[0] if stones else 0