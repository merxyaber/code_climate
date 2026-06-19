"""
This is a sample Python file to test the Code Climate Tool.
It contains:
- Comments
- Control structures
- Good and bad variable names
"""


# GOOD VARIABLES
user_name = "Alice"
user_age = 25


# BAD VARIABLES (should be flagged)
UserName = "Bob"
userAge = 30


# FUNCTION WITH COMPLEXITY
def process_data(numbers):
    total_sum = 0

    for num in numbers:
        if num > 0:
            total_sum += num
        elif num == 0:
            total_sum += 0
        else:
            total_sum -= num

    return total_sum


# ANOTHER FUNCTION
def check_even_odd(n):
    if n % 2 == 0:
        return "Even"
    else:
        return "Odd"


# WHILE LOOP
count = 0
while count < 5:
    print(count)
    count += 1


# COMMENTS SECTION
# This is a single-line comment
# Another comment here


"""
This is a multi-line comment (docstring style)
Used to test detection of docstrings
"""