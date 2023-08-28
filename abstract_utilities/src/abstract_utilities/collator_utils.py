"""
collator_utils.py
Part of the abstract_utilities module

The collator_utils script offers utility functions that facilitate operations related to alphabets and numbers. This includes generating lists of alphabetic characters and numbers, finding the index of a character in a list, and more.

FUNCTIONS:
- get_alpha_list: Generates a list containing all lowercase alphabets.
- get_num_list: Creates a list of numbers represented as strings.
- find_it_alph: Searches for an element within a list and returns its index.
- get_alpha: Converts an index into its corresponding alphabetic character.

USAGE:

To obtain a list of all lowercase alphabets:
>>> from abstract_utilities.collator_utils import get_alpha_list
>>> alphabets = get_alpha_list()

To retrieve the alphabetic character for a given index:
>>> from abstract_utilities.collator_utils import get_alpha
>>> character = get_alpha(5)  # This would return the character for index 5

For further details on each function, refer to its specific docstring.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
from typing import Union
def get_alpha_list() -> list:
    """
    Generates a list of all lowercase alphabets.
    
    Returns:
        list: A list of all lowercase alphabets.
    """
    return list('abcdefghijklmnopqrstuvwxyz')


def get_num_list() -> list:
    """
    Generates a list of numbers as strings.
    
    Returns:
        list: A list of numbers as strings.
    """
    return list('0123456789')
def find_it_alph(ls: list, y: any) -> int:
    """
    Finds the index of an element in a list.

    Args:
        ls (list): The list to search.
        y (any): The element to find.

    Returns:
        int: The index of the element in the list. If not found, returns -1.
    """
    i = 0
    while str(ls[i]) != str(y):
        i += 1
    return i
def get_alpha(k: Union[int,float]) -> str:
    """
    Retrieves the alphabetic character corresponding to the given index.

    Args:
        k (int|float): The index of the character.

    Returns:
        str: The alphabetic character.
    """
    k, 
    if k <= len(get_alpha_list()):
        return 0, k
    mul = int(float(k) / float(len(get_alpha_list())))
    rem = int(k) - int(mul * len(get_alpha_list()))
    if mul - 1 > -1:
        return str(alph[mul]) + str(alph[rem])
    return str(alph[rem])

