# Amazon.com is distributing coupons in the form of a lottery system for loyal customers. The coupons are called "lucky numbers" and the customer with the largest lucky number gets the best discount. Devise a method to determine the maximum possible lucky number. A positive integer is a lucky number if its decimal representation contains onlydigits x and y. For example, if x = 2 and y = 5, then 2,552, and 5225 are lucky numbers, and 3, 24, 57 and 389 are not.

# Given two different digits x and y and a positive integer n, determine the maximum possible lucky number, the sum of whose digits is n. It is guaranteed that at least one lucky number exists for the given x, y, and n.

# Example:

# If the two digits that make up the number are x = 3 and y = 4, and the sum of the digits must be n = 13, then the lucky numbers are:
    
#     • 3334
#     • 3343
#     • 3433
#     • 4333
    
#     The maximum lucky number among these is 4333.

# This function is incorrect. however it works on the test cases provided.
def max_sum(i,j,k):
    num = []
    max = i if i >= j else j
    min = i if i < j else j
    current = 0
    temp = -1
    while current != k:
        if current < k:
            num.append(str(max))
            current += int(max)
            temp = -1
        else:
            num[temp] = str(min)
            current -= (int(max) - int(min))
            temp -= 1
    
    return (f'The maximum lucky number among these is {"".join(num)}')


# original and correct solution from chatgpt
def max_lucky_number(x, y, n):
# Ensure x < y (so y is the larger digit)
    if x > y:
        x, y = y, x

    # We try to use as many 'y' as possible
    for count_y in range(n // y, -1, -1):
        remaining = n - count_y * y
        if remaining % x == 0:
            count_x = remaining // x
            # construct number (larger digit first)
            result = str(y) * count_y + str(x) * count_x
            return result

    return None  # shouldn't happen (guaranteed solution)


# Example from the problem
print(max_lucky_number(3, 4, 13))  # Output: 4333


