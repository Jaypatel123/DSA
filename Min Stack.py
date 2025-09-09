# 155. Min Stack

# Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

# Implement the MinStack class:

# MinStack() initializes the stack object.
# void push(int val) pushes the element val onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.
# You must implement a solution with O(1) time complexity for each function.

 

# Example 1:

# Input
# ["MinStack","push","push","push","getMin","pop","top","getMin"]
# [[],[-2],[0],[-3],[],[],[],[]]

# Output
# [null,null,null,null,-3,null,0,-2]

# Explanation
# MinStack minStack = new MinStack();
# minStack.push(-2);
# minStack.push(0);
# minStack.push(-3);
# minStack.getMin(); // return -3
# minStack.pop();
# minStack.top();    // return 0
# minStack.getMin(); // return -2
 

# Constraints:

# -231 <= val <= 231 - 1
# Methods pop, top and getMin operations will always be called on non-empty stacks.
# At most 3 * 104 calls will be made to push, pop, top, and getMin.

# # Your MinStack object will be instantiated and called as such:
# # obj = MinStack()
# # obj.push(val)
# # obj.pop()
# # param_3 = obj.top()
# # param_4 = obj.getMin()

# I have tried with dictionary, however time complexity is not better than current list method
# from collections import defaultdict 
class MinStack:

    def __init__(self):
        self.i = []
        self.min_i = []
        # self.min_hash = defaultdict(int) # dictionary method

    def push(self, val: int) -> None:
        self.i.append(val)
        self.min_i.append(min(self.min_i[-1] if self.min_i else val, val))
        # self.min_hash[val] += 1 # dictionary method
        return None

    def pop(self) -> None:
        self.i.pop()
        self.min_i.pop()
        # temp = self.i.pop() # dictionary method
        # if self.min_hash[temp] == 1: # dictionary method
        #     self.min_hash.pop(temp) # dictionary method
        # else: # dictionary method
        #     self.min_hash[temp] -= 1 # dictionary method
        return None

    def top(self) -> int:
        return self.i[-1]

    def getMin(self) -> int:
        return self.min_i[-1]
        # return min(self.min_hash) # dictionary method


