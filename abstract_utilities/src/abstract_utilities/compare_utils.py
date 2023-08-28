"""
compare_utils.py
Part of the abstract_utilities package

This script provides utility functions for comparing strings and objects. These functions include methods for calculating string similarity and comparing the lengths of objects.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
def get_comp(string:str, string_2:str):
    """
    Calculates the similarity between two strings.

    Args:
        string (str): The first string.
        string_2 (str): The second string.

    Returns:
        float: The similarity score between the two strings, calculated by comparing overlapping sequences of characters.
    """
    ls = [['']]
    for k in range(len(get_lower(string, string_2))):
        if string[k] in st2:
            if len(ls) == 0 or ls[-1][0] + string[k] in string_2:
                ls[-1].append(string[k])
            else:
                ls.append([string[k]])
        elif len(string) > 1:
            string = string[1:]
    for k in range(len(ls)):
        ls[k] = len(ls[k])
    ls.sort()
    return float(ls[0] / len(string_2))

def get_lower(obj, obj2):
    """
    Compares the lengths of two objects or their string representations and returns the shorter one. If an object isn't a string, it's compared using its natural length.

    Args:
        obj: The first object to compare.
        obj2: The second object to compare.

    Returns:
        any: The shorter of the two objects, based on their length or string representation length.
    """
    lowest = [obj, 0]
    if type(obj) == str:
        lowest = [len(obj), 0]
    if type(obj2) == str:
        return obj2 if len(obj2) > lowest[0] else obj
    return obj2 if obj2 > lowest[0] else obj
def is_in_list(obj: any, ls: list = []):
    """
    Checks if the given object is present in the list.

    Args:
        obj (any): The object to search for.
        ls (list, optional): The list in which to search. Defaults to an empty list.

    Returns:
        bool: True if the object is in the list, False otherwise.
    """
    if obj in ls:
        return True
def safe_len(obj: str = ''):
    """
    Safely gets the length of the string representation of the given object.

    Args:
        obj (str, optional): The object whose string length is to be determined. Defaults to an empty string.

    Returns:
        int: The length of the string representation of the object. Returns 0 if any exceptions are encountered.
    """
    try:
        length = len(str(obj))
    except:
        length = 0
    return length
def line_contains(string: str = None, compare: str = None, start: int = 0, length: int = None):
    """
    Determines if the substring `compare` is present at the beginning of a section of `string` starting at the index `start` and having length `length`.

    Args:
        string (str, optional): The main string to search within. Defaults to None.
        compare (str, optional): The substring to search for. Defaults to None.
        start (int, optional): The index to start the search from. Defaults to 0.
        length (int, optional): The length of the section to consider for the search. If not specified, the length is determined safely.

    Returns:
        bool: True if the substring is found at the specified position, False otherwise.
    """
    if is_in_list(None,[string,compare]):
        return False
    if length == None:
        length = safe_len(string)
    string = string[start:length]
    if safe_len(compare)>safe_len(string):
        return False
    if string[:safe_len(compare)]==compare:
        return True
    return False
