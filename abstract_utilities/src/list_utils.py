"""
This module, 'list_utils.py', contains utility functions for operating on lists.

Functions:
    get_sort(ls: list, k: int = 0): Sorts a list in ascending order and returns the element at index k.
    combineList(ls: list, lsN: list): Combines two lists and returns the combined list.
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
# Function: get_sort
# Function: combineList
