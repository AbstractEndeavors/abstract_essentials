"""
compare_utils.py

This script provides utility functions for comparing strings and objects. These functions include methods for calculating string similarity and comparing the lengths of objects.

"""

def get_comp(st, st2):
    """
    Calculates the similarity between two strings.

    Args:
        st (str): The first string.
        st2 (str): The second string.

    Returns:
        float: The similarity score between the two strings, calculated by comparing overlapping sequences of characters.
    """
    ls = [['']]
    st = get_lower(st, st2)
    for k in range(len(st)):
        if st[k] in st2:
            if len(ls) == 0 or ls[-1][0] + st[k] in st2:
                ls[-1].append(st[k])
            else:
                ls.append([st[k]])
        elif len(st) > 1:
            st = st[1:]
    for k in range(len(ls)):
        ls[k] = len(ls[k])
    ls.sort()
    return ls[0] / len(st2)

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

