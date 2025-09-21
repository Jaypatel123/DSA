# 51. N-Queens

# The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

# Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

# Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

 

# Example 1:


# Input: n = 4
# Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
# Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above
# Example 2:

# Input: n = 1
# Output: [["Q"]]
 

# Constraints:

# 1 <= n <= 9

# Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The relative order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        
        col = set()
        positive_diag = set()
        negative_diag =  set()

        res = []
        board = [["."] * n for _ in range(n)]

        def queenPlacement(r):
            if r == n:
                copy = ["".join(i) for i in board]
                res.append(copy)
                return
            
            for c in range(n):
                if c in col or (r - c) in negative_diag or (r + c) in positive_diag:
                    continue
                col.add(c)
                negative_diag.add(r - c)
                positive_diag.add(r + c)
                board[r][c] = 'Q'

                queenPlacement(r + 1)

                col.remove(c)
                negative_diag.remove(r - c)
                positive_diag.remove(r + c)
                board[r][c] = '.'

        queenPlacement(0)
        return res
