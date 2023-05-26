"""
This module, 'math_utils.py', contains utility functions related to mathematical operations. 
Here we have a function to compute the quotient and the remainder of a division operation.

The specific functions and their descriptions should be included in their respective docstrings.
The docstrings should provide details on the purpose of each function, their inputs, and outputs.
"""

def get_multiply_remainder(x: int, y: int) -> tuple:
    """
    Computes the quotient and remainder of dividing x by y.

    Args:
        x (int): The dividend.
        y (int): The divisor.

    Returns:
        tuple: A tuple containing the quotient and remainder.
    """
    if x <= y:
        return 0, x
    mul = int(float(x) / float(y))
    return mul, int(x) - int(mul * y)
# Function: get_multiply_remainder
