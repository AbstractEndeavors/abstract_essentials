"""
list_utils.py

This module provides a set of utility functions tailored for manipulating lists. It offers capabilities to:

- Sort lists and retrieve elements at specific positions.
- Combine two lists.
- Ensure that objects are contained within nested lists.
- Add multiple values to a list.

The `list_utils` module is designed to simplify and abstract common list operations, enhancing code readability and reusability.

Note: While Python's native list methods are comprehensive, the functions here provide additional checks and transformations that might be commonly needed in various applications.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
def get_sort(ls: list, k: int = 0):
    """
    Sorts a list in ascending order and returns the element at index k.

    Args:
        ls (list): The list to be sorted.
        k (int, optional): The index of the element to return. Defaults to 0.

    Returns:
        any: The element at index k after sorting the list.
    """
    ls.sort()
    return ls[k]

def combineList(ls: list, lsN: list) -> list:
    """
    Combines two lists and returns the combined list.

    Args:
        ls (list): The first list.
        lsN (list): The second list.

    Returns:
        list: The combined list.
    """
    for k in range(len(lsN)):
        ls.append(lsN[k])
    return ls
def ensure_nested_list(obj):
    """
    Ensure that the input object is a nested list.

    Args:
        obj (any): The object to ensure as a nested list.

    Returns:
        list: A nested list containing the object or the original list if it's already nested.
    """
    # Check if the input object is a list
    if not isinstance(obj, list):
        # If it's not a list, create a new nested list containing the object
        return [obj]
    # If it is a list, check if any of its elements are non-list objects
    for element in obj:
        if not isinstance(element, list):
            # If at least one element is not a list, wrap the original list in a new list
            return [obj]
    # If all elements are lists, return the original list
    return obj
def make_list_add(obj,values):
    """
    Add multiple values to a list and return the resulting list.

    Args:
        obj (list): The original list.
        values (iterable): Values to be added to the list.

    Returns:
        list: The modified list containing the original elements and the added values.
    """
    obj = list(obj)
    for each in list(values):
        obj.append(each)
    return obj
