"""
This module, 'class_utils.py', contains utility functions for dealing with classes, objects, and modules.
These include functions to:

1. Manipulate global variables.
2. Fetch and check object types and their membership in a module.
3. Fetch and inspect function signatures within a module.
4. Call functions with supplied arguments.
5. Convert layout to components.
6. Retrieve directory of a module.

Each function includes a docstring to further explain its purpose, input parameters, and return values.
"""

import inspect
import json
def get_type_list()->list:
    return ['None','str','int','float','bool','list','tuple','set','dict','frozenset','bytearray','bytes','memoryview','range','enumerate','zip','filter','map','property','slice','super','type','Exception','object']
def remove_key(js: dict, key: any) -> dict:
    """Remove a key from a dictionary. If the key is not present,
    no action is taken."""
    js.pop(key, None)
    return js
def ret_globals(globs: dict = globals()) -> dict:
    """
    Returns the global variables.

    Args:
        globs (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        dict: The global variables dictionary.
    """
    return globs


def change_glob(var: str, val: any, glob: dict = ret_globals()) -> any:
    """
    Changes the value of a global variable.

    Args:
        var (str): The name of the global variable.
        val (any): The new value.
        glob (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        any: The new value of the variable.
    """
    glob[var] = val
    return val


def get_module_obj(instance: any, obj: any):
    """
    Retrieves an object from a module.

    Args:
        instance (any): The module instance.
        obj (any): The object to retrieve.

    Returns:
        any: The retrieved object.
    """
    return getattr(module, obj)


def spec_type_mod(obj: any, st: str) -> bool:
    """
    Checks if an object has a specific type.

    Args:
        obj (any): The object to check.
        st (str): The specific type to check.

    Returns:
        bool: True if the object has the specified type, False otherwise.
    """
    if obj.__class__.__name__ == st:
        return True
    return False


def get_type_mod(obj: any) -> str:
    """
    Retrieves the type of an object.

    Args:
        obj (any): The object to get the type of.

    Returns:
        str: The type of the object.
    """
    type_ls = get_types_list()
    for k in range(len(type_ls)):
        typ = str(type_ls[k])
        if spec_type_mod(obj, typ):
            return typ
    return "NoneType"


def is_module_obj(instance: any, obj: str) -> bool:
    """
    Checks if an object is part of a module.

    Args:
        instance (any): The module instance.
        obj (str): The name of the object to check.

    Returns:
        bool: True if the object is part of the module, False otherwise.
    """
    try:
        if get_type_mod(getattr(instance, obj)) in [None, 'NoneType']:
            return False
        return True
    except:
        return False


def inspect_signature(instance: any, function: str):
    """
    Inspects the signature of a function.

    Args:
        instance (any): The instance containing the function.
        function (str): The name of the function to inspect.

    Returns:
        inspect.Signature: The signature of the function.
    """
    return inspect.signature(get_module_obj(instance, function))


def get_parameter_defaults(module, function):
    """
    Retrieves the default parameter values of a function.

    Args:
        module: The module instance.
        function (str): The name of the function.

    Returns:
        dict: A dictionary containing the parameter names and their default values.
    """
    signature = inspect_signature(module, function)
    if signature is None:
        return {}
    return json.dumps(remove_key({param_name: param.default if param.default != inspect.Parameter.empty else None for param_name, param in signature.parameters.items()}, 'icon'))


def call_functions_hard(function_name: str, instance: any = None, **kwargs):
    """
    Calls a function with the given arguments.

    Args:
        function_name (str): The name of the function.
        instance (any, optional): The instance to call the function on. Defaults to None.
        **kwargs: The keyword arguments for the function.

    Returns:
        any: The result of the function call.
    """
    if instance is not None:
        return getattr(instance, function_name)(**kwargs)
    else:
        return globals()[function_name](**kwargs)


def convert_layout_to_components(instance: any = None, component: str = 'function', js: dict = {}):
    """
    Converts a layout to components.

    Args:
        instance (any, optional): The instance containing the components. Defaults to None.
        component (str, optional): The name of the component. Defaults to 'function'.
        js (dict, optional): The dictionary of component properties. Defaults to an empty dictionary.

    Returns:
        any: The result of the component conversion.
    """
    jsN = json.loads(get_parameter_defaults(instance, component))
    keys = list(js.keys())
    for key in jsN:
        if key in js:
            jsN[key] = js[key]
    return call_functions_hard(instance, component, **jsN)


def get_dir(mod):
    """
    Retrieves the directory of a module.

    Args:
        mod: The module.

    Returns:
        list: The list of attributes and methods in the module.
    """
    return dir(mod)
def get_fun(js):
    """
    Retrieves and calls a function with the given parameters.

    Args:
        js (dict): A dictionary that contains function details, including name, arguments, instance (optional), and global scope (optional).

    Returns:
        any: The result of the function call.
    """
    # Get function details
    function_name = js['name']
    function_args = js.get('args', {})
    instance = js.get('instance')
    glob = js.get('global')
    # Process arguments
    function_args = process_args(function_args)
    # If instance is not None, get the function from the instance, else get from globals
    if instance is not None:
        function = getattr(instance, function_name)
    else:
        function = glob[function_name]
    # Get function's valid parameter keys
    sig = inspect.signature(function)
    valid_keys = sig.parameters.keys()
    # Filter arguments to only those accepted by the function
    filtered_args = {k: v for k, v in function_args.items() if k in valid_keys}
    return call_functions(function_name, filtered_args, instance, glob)
def call_functions(function_name: str, args: dict = None, instance=None, glob=globals()):
    """
    Calls a function or a method with the given arguments.

    Args:
        function_name (str): The name of the function.
        args (dict, optional): A dictionary of arguments to pass to the function. Defaults to None.
        instance (optional): The instance on which to call the method. Defaults to None.
        glob (optional): The global scope from which to retrieve the function. Defaults to globals().

    Returns:
        any: The result of the function or method call.
    """
    if glob == None:
      glob = globals()
    if args is None:
        args = {}
    if instance is not None:
        # Calls method on instance
        method = getattr(instance, function_name)
        return method(*args) if isinstance(args, list) else method(**args)
    else:
        # Calls function from globals
        function = glob[function_name]
        return function(*args) if isinstance(args, list) else function(**args)
def process_args(args):
    """
    Processes the arguments for a function, replacing nested function calls with their results.

    Args:
        args (dict): A dictionary of arguments. 

    Returns:
        dict: A dictionary of processed arguments.
    """
    for key, value in args.items():
        # check if value is a dict and has a 'type' key with value 'get'
        if isinstance(value, dict) and value.get('type') == 'get':
            function_name = value['name']
            function_args = value.get('args', {})
            instance = value.get('instance')
            glob = value.get('global')
            # call the function and replace the arg with its result
            args[key] = call_functions(function_name, function_args, instance, glob)
    return args
# Check if the function exists
def mk_fun(module,function):
    """
    Checks if a function exists in a given module.

    Args:
        module: The module in which to look for the function.
        function: The function to check.

    Prints a statement indicating whether the function exists.
    """
    if hasattr(sg, 'window'):
      print("The function exists.")
    else:
      print("The function does not exist.")
    input(instance)
