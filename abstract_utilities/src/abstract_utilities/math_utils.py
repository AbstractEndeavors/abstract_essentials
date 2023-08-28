import math
from .type_utils import det_bool_T
"""
math_utils.py

This module offers a set of mathematical utility functions tailored to perform specific calculations. Some of its functionalities include:
- Computing the quotient and remainder of dividing two numbers.
- Rounding up numbers to the nearest integer.
- Checking if a number falls outside a given range or boundary.

Usage:
    import abstract_utilities.math_utils as math_utils This module is part of the `abstract_utilities` package.

As part of the `abstract_utilities` package, the module serves to abstract and simplify certain mathematical operations that may be frequently used in various applications.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
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
def rounded_up_integer(number: (float or int)) -> int:
    """
    Rounds up a given number to the nearest integer and returns the result.

    Parameters:
    number (float or int): The number to be rounded up.

    Returns:
    int: The rounded up integer value of the input number.
    """
    if isinstance(number, int):
        number = float(number)
    
    if isinstance(number, float):
        number = math.ceil(number)
    
    return number
def out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1):
    """
    Checks if the given object is out of the specified upper and lower bounds.

    Args:
        upper (int or float): The upper bound.
        lower (int or float): The lower bound.
        obj (int or float): The object to check.

        bool: True if the object is out of bounds, False otherwise.
    """
    return det_bool_T(obj > 100 or obj < 0)
