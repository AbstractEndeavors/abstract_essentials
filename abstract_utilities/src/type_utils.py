"""
type_utils.py
This module provides utility functions for working with data types.

Functions:
- is_number(obj:any) -> bool: Checks if the input object is a number.
- is_str(obj:any) -> bool: Checks if the input object is a string.
- is_int(obj:any) -> bool: Checks if the input object is an integer.
- get_type(obj:any) -> any: Determines the type of the input object.
- is_float(obj:any) -> bool: Checks if the input object is a float.
- is_bool(obj:any) -> bool: Checks if the input object is a boolean.
- is_list(obj:any) -> bool: Checks if the input object is a list.
- is_tuple(obj:any) -> bool: Checks if the input object is a tuple.
- is_set(obj:any) -> bool: Checks if the input object is a set.
- is_dict(obj:any) -> bool: Checks if the input object is a dictionary.
- is_frozenset(obj:any) -> bool: Checks if the input object is a frozenset.
- is_bytearray(obj:any) -> bool: Checks if the input object is a bytearray.
- is_bytes(obj:any) -> bool: Checks if the input object is a bytes object.
- is_memoryview(obj:any) -> bool: Checks if the input object is a memoryview object.
- is_range(obj:any) -> bool: Checks if the input object is a range object.
- is_enumerate(obj:any) -> bool: Checks if the input object is an enumerate object.
- is_zip(obj:any) -> bool: Checks if the input object is a zip object.
- is_filter(obj:any) -> bool: Checks if the input object is a filter object.
- is_map(obj:any) -> bool: Checks if the input object is a map object.
- is_property(obj:any) -> bool: Checks if the input object is a property object.
- is_slice(obj:any) -> bool: Checks if the input object is a slice object.
- is_super(obj:any) -> bool: Checks if the input object is a super object.
- is_type(obj:any) -> bool: Checks if the input object is a type object.
- is_Exception(obj:any) -> bool: Checks if the input object is an Exception object.
- is_none(obj:any) -> bool: Checks if the input object is None.
- is_dict_or_convertable(obj:any) -> bool: Checks if the input object is a dictionary or can be converted to a dictionary.
- dict_check_conversion(obj:any) -> any: Converts the input object to a dictionary if possible.
- make_list(obj:any) -> list: Converts the input object to a list.
- make_list_lower(ls: list) -> list: Converts all elements in a list to lowercase, ignoring None values.
- make_float(x) -> float: Converts the input object to a float.
- make_bool(x) -> bool: Converts the input object to a boolean.
- make_str(x: any) -> str: Converts the input object to a string.
- get_obj_obj(obj: str, x: any) -> any: Returns the object converted according to the given type string.
- get_len_or_num(obj: any) -> int: Returns the length of the object if it can be converted to a string, else the integer representation of the object.
- get_types_list() -> list: Returns a list of all supported types.
"""
from typing import Union
def is_iterable(obj:any):
    try:
        iterator=iter(obj)
    except TypeError:
        return False
    else:
        return True
    return True
def is_number(obj:any) -> bool:
    """
    Checks if the input object is a number.
    
    Args:
        obj: The object to check.
        
    Returns:
        bool: True if the object is a number (int or float), False otherwise.
    """
    try:
        float(obj)
        return True
    except ValueError:
        return False


def is_str(obj:any) -> bool:
    """
    Checks if the input object is a string.
    
    Args:
        obj: The object to check.
        
    Returns:
        bool: True if the object is a string, False otherwise.
    """
    return isinstance(obj, str)


def is_int(obj:any) -> bool:
    """
    Checks if the input object is an integer.
    
    Args:
        obj: The object to check.
        
    Returns:
        bool: True if the object is an integer, False otherwise.
    """
    return isinstance(obj, int)

def get_type(obj:any) -> any:
    """
    Determines the type of the input object.

    Args:
        obj: The object to determine the type of.

    Returns:
        any: The object with the updated type.
    """
    if is_number(obj):
        obj = int(obj)
    if is_float(obj):
        return float(obj)
    elif obj == 'None':
        obj = None
    elif is_str(obj):
        obj = str(obj)
    return obj
def is_float(obj:any) -> bool:
    """
    Checks if the input object is a float.
    
    Args:
        obj: The object to check.
        
    Returns:
        bool: True if the object is a float, False otherwise.
    """
    return isinstance(obj, float)
def get_type(obj):
    if is_number(obj):
        obj = int(obj)
    if is_float(obj):
        return float(obj)
    elif obj == 'None':
        obj =  None
    elif is_str(obj):
        obj =  str(obj)
    return obj
def is_number(obj:any) -> bool:
    """
    Checks whether the input object can be represented as a number.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object can be represented as a number, False otherwise.
    """
    try:
        float(obj)
        return True
    except (TypeError, ValueError):
        return False
def is_object(obj:any) -> bool:
    """
    Checks whether the input object is of type 'object'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'object', False otherwise.
    """
    return isinstance(obj, object)
def is_str(obj:any) -> bool:
    """
    Checks whether the input object is of type 'str'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'str', False otherwise.
    """
    return isinstance(obj, str)
def is_int(obj:any) -> bool:
    """
    Checks whether the input object is of type 'int'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'int', False otherwise.
    """
    return isinstance(obj, int)
def is_float(obj:any) -> bool:
    """
    Checks whether the input object is of type 'float'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'float', False otherwise.
    """
    return isinstance(obj, float)
def is_bool(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bool'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bool', False otherwise.
    """
    return isinstance(obj, bool)


def is_list(obj:any) -> bool:
    """
    Checks whether the input object is of type 'list'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'list', False otherwise.
    """
    return isinstance(obj, list)
def is_tuple(obj:any) -> bool:
    """
    Checks whether the input object is of type 'tuple'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'tuple', False otherwise.
    """
    return isinstance(obj, tuple)
def is_set(obj:any) -> bool:
    """
    Checks whether the input object is of type 'set'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'set', False otherwise.
    """
    return isinstance(obj, set)
def is_dict(obj:any) -> bool:
    """
    Checks whether the input object is of type 'dict'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'dict', False otherwise.
    """
    return isinstance(obj, dict)
def is_frozenset(obj:any) -> bool:
    """
    Checks whether the input object is of type 'frozenset'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'frozenset', False otherwise.
    """
    return isinstance(obj, frozenset)
def is_bytearray(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bytearray'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bytearray', False otherwise.
    """
    return isinstance(obj, bytearray)
def is_bytes(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bytes'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bytes', False otherwise.
    """
    return isinstance(obj, bytes)
def is_memoryview(obj:any) -> bool:
    """
    Checks whether the input object is of type 'memoryview'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'memoryview', False otherwise.
    """
    return isinstance(obj, memoryview)
def is_range(obj:any) -> bool:
    """
    Checks whether the input object is

 of type 'range'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'range', False otherwise.
    """
    return isinstance(obj, range)
def is_enumerate(obj:any) -> bool:
    """
    Checks whether the input object is of type 'enumerate'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'enumerate', False otherwise.
    """
    return isinstance(obj, enumerate)
def is_zip(obj:any) -> bool:
    """
    Checks whether the input object is of type 'zip'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'zip', False otherwise.
    """
    return isinstance(obj, zip)
def is_filter(obj:any) -> bool:
    """
    Checks whether the input object is of type 'filter'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'filter', False otherwise.
    """
    return isinstance(obj, filter)
def is_map(obj:any) -> bool:
    """
    Checks whether the input object is of type 'map'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'map', False otherwise.
    """
    return isinstance(obj, map)
def is_property(obj:any) -> bool:
    """
    Checks whether the input object is of type 'property'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'property', False otherwise.
    """
    return isinstance(obj, property)


def is_slice(obj:any) -> bool:
    """
    Checks whether the input object is of type 'slice'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'slice', False otherwise.
    """
    return isinstance(obj, slice)


def is_super(obj:any) -> bool:
    """
    Checks whether the input object is of type 'super'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'super', False otherwise.
    """
    return isinstance(obj, super)


def is_type(obj:any) -> bool:
    """
    Checks whether the input object is of type 'type'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'type', False otherwise.
    """
    return isinstance(obj, type)


def is_Exception(obj:any) -> bool:
    """
    Checks whether the input object is of type 'Exception'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'Exception', False otherwise.
    """
    return isinstance(obj, Exception)


def is_none(obj:any) -> bool:
    """
    Checks whether the input object is of type 'None'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'None', False otherwise.
    """
    if type(obj) is None:
        return True
    else:
        return False


def is_dict(obj:any) -> bool:
    """
    Checks whether the input object is of type 'dict'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'dict', False otherwise.
    """
    if isinstance(obj, dict):
        return True
    return False


def is_str_convertible_dict(obj:any) -> bool:
    """
    Checks whether the input object can be converted to a dictionary.

    Args:
        obj

: The object to check.

    Returns:
        bool: True if the object can be converted to a dictionary, False otherwise.
    """
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
            return True
        except json.JSONDecodeError:
            return False
    return False


def is_dict_or_convertable(obj:any) -> bool:
    """
    Checks whether the input object is of type 'dict' or can be converted to a dictionary.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'dict' or can be converted to a dictionary, False otherwise.
    """
    if is_dict(obj):
        return True
    if is_str_convertible_dict(obj):
        return True
    return False


def dict_check_conversion(obj:any) -> any:
    """
    Converts the input object to a dictionary if possible.

    Args:
        obj: The object to convert.

    Returns:
        any: The converted object if conversion is possible, otherwise the original object.
    """
    if is_dict_or_convertable(obj):
        if is_dict(obj):
            return obj
        return json.loads(obj)
    return obj


def is_list(obj:any) -> bool:
    """
    Checks whether the input object is of type 'list'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'list', False otherwise.
    """
    if type(obj) is list:
        return True
    return False
def is_str_convertible_dict(obj:any) -> bool:
    """
    Checks whether the input object is a string that can be converted to a dict.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object can be converted to a dict, False otherwise.
    """
    import json

    if isinstance(obj, str):
        try:
            json.loads(obj)
            return True
        except json.JSONDecodeError:
            return False

    return False

def is_dict_or_convertable(obj:any) -> bool:
    """
    Checks whether the input object is a dictionary or can be converted to a dictionary.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is a dictionary or can be converted to one, False otherwise.
    """
    return is_dict(obj) or is_str_convertible_dict(obj)

def dict_check_conversion(obj:any) -> Union[dict,any]:
    """
    Converts the input object to a dictionary if possible.

    Args:
        obj: The object to convert.

    Returns:
        The object converted to a dictionary if possible, otherwise the original object.
    """
    import json

    if is_dict_or_convertable(obj):
        if is_dict(obj):
            return obj
        return json.loads(obj)
    
    return obj
def make_list(obj:any) -> list:
    """
    Converts the input object to a list. If the object is already a list, it is returned as is.
    
    Args:
        obj: The object to convert.
        
    Returns:
        list: The object as a list.
    """
    return obj if isinstance(obj, list) else [obj]
def make_list_lower(ls: list) -> list:
    """
    Converts all elements in a list to lowercase. Ignores None values.
    
    Args:
        ls: The list to convert.
        
    Returns:
        list: The list with all strings converted to lowercase.
    """
    return [item.lower() if isinstance(item, str) else item for item in ls]


def make_float(obj:Union[str,float,int]) -> float:
    """
    Converts the input object to a float.
    
    Args:
        x: The object to convert.
        
    Returns:
        float: The float representation of the object.
    """
    try:
        return float(obj)
    except (TypeError, ValueError):
        return 1.0

def make_bool(obj: Union[bool, int, str]) -> Union[bool, str]:
    """
    Converts the input object to a boolean representation if possible.

    The function attempts to convert various objects, including integers and strings, to their boolean equivalents. 
    If the conversion is not possible, the original object is returned.

    Args:
        obj: The object to be converted.

    Returns:
        bool or original type: The boolean representation of the object if conversion is possible. Otherwise, it returns the original object.

    Examples:
        make_bool("true") -> True
        make_bool(1)      -> True
        make_bool("0")    -> False
        make_bool(2)      -> 2
    """
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        if obj == 0:
            return False
        if obj == 1:
            return True
    if isinstance(obj, str):
        if obj.lower() in ['0', "false"]:
            return False
        if obj.lower() in ['1', "true"]:
            return True
    return obj

def make_str(obj: any) -> str:
    """
    Converts the input object to a string.
    
    Args:
        obj: The object to convert.
        
    Returns:
        str: The string representation of the object.
    """
    return str(obj)


def get_obj_obj(obj_type: str, obj: any) -> any:
    """
    Returns the object converted according to the given type string.
    
    Args:
        obj_type: The string representing the type to convert to.
        obj: The object to convert.
        
    Returns:
        any: The object converted to the specified type.
    """
    if obj_type == 'str':
        return make_str(obj)
    elif obj_type == 'bool':
        return make_bool(obj)
    elif obj_type == 'float':
        return make_float(obj)
    elif obj_type == 'int':
        try:
            return int(obj)
        except (TypeError, ValueError):
            return obj
    else:
        return obj
def get_len_or_num(obj: any) -> int:
    """
    Returns the length of the object if it can be converted to a string, else the integer representation of the object.
    
    Args:
        obj: The object to process.
        
    Returns:
        int: The length of the object as a string or the integer representation of the object.
    """
    if is_int(obj) or is_float(obj):
        return int(obj)
    else:
        try:
            return len(str(obj))
        except (TypeError, ValueError):
            return 0
def get_types_list()->list:
    return ['list', 'bool', 'str', 'int', 'float', 'set', 'dict', 'frozenset', 'bytearray', 'bytes', 'memoryview', 'range', 'enumerate', 'zip', 'filter', 'map', 'property', 'slice', 'super', 'type', 'Exception', 'NoneType']

# Function: is_number
# Function: is_str
# Function: is_int
# Function: get_type
# Function: is_float
# Function: is_object
# Function: is_bool
# Function: is_list
# Function: is_tuple
# Function: is_set
# Function: is_dict
# Function: is_frozenset
# Function: is_bytearray
# Function: is_bytes
# Function: is_memoryview
# Function: is_range
# Function: is_enumerate
# Function: is_zip
# Function: is_filter
# Function: is_map
# Function: is_property
# Function: is_slice
# Function: is_super
# Function: is_type
# Function: is_Exception
# Function: is_none
# Function: is_str_convertible_dict
# Function: is_dict_or_convertable
# Function: dict_check_conversion
# Function: make_list
# Function: make_list_lower
# Function: make_float
# Function: make_bool
# Function: make_str
# Function: get_obj_obj
# Function: get_len_or_num
# Function: get_types_list
