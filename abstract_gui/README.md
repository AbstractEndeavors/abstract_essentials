# Abstract GUI Module

The `abstract_gui` module provides classes and functions to manage PySimpleGUI windows and events in a more abstract manner. It includes a class called `WindowGlobalBridge` to manage global variables shared between different scripts and a class called `WindowManager` to manage PySimpleGUI windows and their events.

# Installation

You can install the `abstract_gui` module using `pip`:

```
pip install abstract_gui
```
## Features
`abstract_browser()`:
![Screenshot from 2023-08-31 01-13-20](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/68fea923-e555-452d-ab6e-6c6b516ce919)

![Screenshot from 2023-08-31 01-13-45](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/b38233cf-ed4b-485f-b6c3-e31865758c5b)

`scan_browser()`
![Screenshot from 2023-08-31 01-19-42](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/b22214fa-cd5a-40c4-904b-be9c4136ac0a)

* Feature 1
* Feature 2
* ... 

Certainly! Here's the "Dependencies" section formatted similarly to the previous sections:

## **Dependencies**:

- ### `import PySimpleGUI as sg`
    - **Purpose**: PySimpleGUI offers a simpler way to create desktop applications.

- ### `from abstract_utilities.thread_utils import thread_alive`
    - **Purpose**: Imports the `thread_alive` function from the `thread_utils` module of the `abstract_utilities` package. This function is likely used to check if a particular thread is still running.

- ### `from abstract_utilities.class_utils import get_fun`
    - **Purpose**: Imports the `get_fun` function from the `class_utils` module of the `abstract_utilities` package. The function might retrieve a specific function or method from a class or module.

- ### `from abstract_utilities.path_utils import get_current_path`
    - **Purpose**: Imports the `get_current_path` function from the `path_utils` module of the `abstract_utilities` package. This function is probably used to retrieve the current working directory or path.

## Components


### abstract_gui.py
#### Functions
##### Class Functions
###### WindowGlobalBridge
* **Attributes**
  * `global_vars (dict)`:  A dictionary to store global variables for each script.
* **Methods**
  * `__init__`
    ```python
    def __init__(self):
    """
    Initializes the WindowGlobalBridge with an empty dictionary for global_vars.
    """
    self.global_vars = {}
    ```
    **Purpose:**
    Initializes the WindowGlobalBridge with an empty dictionary for global_vars.

  * `retrieve_global_variables`
    ```python
    def retrieve_global_variables(self, script_name:str, global_variables:dict, tag_script_name:bool=False):
    """
    Stores the global variables of a script in the global_vars dictionary.

    Args:
        script_name (str): The name of the script.
        global_variables (dict): The global variables to store for the script.
        tag_script_name (bool, optional): If True, the script_name will be stored in the global_variables dictionary.
                                          Defaults to False.
    """
    self.global_vars[script_name] = global_variables
    if tag_script_name:
        self.global_vars[script_name]["script_name"] = script_name

    ```
    **Purpose:**
    Stores the global variables of a script in the global_vars dictionary.

    **Arguments:**
    * script_name (str): The name of the script.
    * global_variables (dict): The global variables to store for the script.
    * tag_script_name (bool, optional): If True, the script_name will be stored in the global_variables dictionary. Defaults to False.

  * `return_global_variables`
    ```python
    def return_global_variables(self, script_name=None):
    """
    Returns the global variables of a script.

    Args:
        script_name (str, optional): The name of the script. If None, all global variables will be returned.

    Returns:
        dict: The global variables of the script. If no global variables are found, it returns an empty dictionary.
    """
    if script_name is not None:
        return self.global_vars.get(script_name, {})
    else:
        return self.global_vars

    ```
    **Purpose:**
    Returns the global variables of a script.

    **Arguments:**
    * script_name (str, optional): The name of the script. If None, all global variables will be returned.

    **Returns:**
    * dict: The global variables of the script. If no global variables are found, it returns an empty dictionary.

  * `change_globals`
    ```python
    def change_globals(self, variable:str, value:any, script_name:str=None):
    """
    Modifies a global variable value for a specified script.

    Args:
        variable (str): The name of the global variable to modify.
        value (any): The new value to assign to the global variable.
        script_name (str, optional): The name of the script. If None, the global variable in the base context will be modified.
    """
    if script_name is not None:
        self.global_vars[script_name][variable] = value
        return value
    ```
    **Purpose:**
    Modifies a global variable value for a specified script.

    **Arguments:**
    * variable (str): The name of the global variable to modify.
    * value (any): The new value to assign to the global variable.
    * script_name (str, optional): The name of the script. If None, the global variable in the base context will be modified.

  * `search_globals_values`
    ```python
    def search_globals_values(self, value:any, script_name:str=None):
    """
    Searches for a specific value in the global variables of a script.

    Args:
        value (any): The value to search for in the global variables.
        script_name (str, optional): The name of the script. If None, the search will be performed in the base context.

    Returns:
        str or False: The name of the first global variable containing the given value, or False if not found.
    """
    if script_name is not None:
        for each in self.global_vars[script_name].keys():
            if self.global_vars[script_name][each] == value:
    ```
    **Purpose:**
    Searches for a specific value in the global variables of a script.

    **Arguments:**
    * value (any): The value to search for in the global variables.
    * script_name (str, optional): The name of the script. If None, the search will be performed in the base context.

    **Returns:**
    * str or False: The name of the first global variable containing the given value, or False if not found.

###### WindowManager
* **Attributes**
  * `all_windows (dict)`:  A dictionary to store registered windows along with their details.
  * `last_window (str)`:  The name of the last accessed window.
  * `script_name (str)`:  The name of the script that is using the WindowManager.
  * `global_bridge`:  The global bridge to access shared variables between different scripts.
  * `global_vars (dict)`:  A dictionary to store global variables for this script.
* **Methods**
  * `__init__`
    ```python
    def __init__(self, script_name, global_bridge):
    """
    Initialize a WindowManager instance.

    Args:
        script_name (str): The name of the script that is using the WindowManager.
        global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.
    """
    self.all_windows = {'last_window': None}
    self.script_name = script_name
    self.global_bridge = global_bridge
    self.global_vars = self.global_bridge.return_global_variables(self.script_name)
    if "all_windows" in self.global_vars:
        self.all_windows = self.global_vars["all_windows"]
    self.global_vars["all_windows"] = self.all_windows
    ```
    **Purpose:**
    Initialize a WindowManager instance.

    **Arguments:**
    * script_name (str): The name of the script that is using the WindowManager.
    * global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.

  * `get_all_windows`
    ```python
    def get_all_windows(self):
    """
    Get all registered windows.

    Returns:
        dict: A dictionary containing all registered windows and their details.
    """
    return self.all_windows
    ```
    **Purpose:**
    Get all registered windows.

  * `get_window_names`
    ```python
    def get_window_names(self):
    """
    Get the names of all registered windows.

    Returns:
        list: A list of names of all registered windows.
    """
    return self.delete_from_list(list(self.get_all_windows().keys()), 'last_window')
    ```
    **Purpose:**
    Get the names of all registered windows.

  * `register_window`
    ```python
    def register_window(self, window=None):
    """
    Register a window.

    Args:
        obj (any, optional): The window to register. If not provided, a new window is created.

    Returns:
        str: The name of the registered window.
    """
    if window in self.get_window_names():
        name = window
    if self.is_window_object(window):
        name = self.search_global_windows(window)
        if name is False:
            name = self.create_window_name()
        self.all_windows[name] = {"method": window,"title":None,"closed":False, "values": {}, "event": "", "event_function": None,"exit_events":None}
        self.all_windows[name]["closed"]=False
    if window == None:
        name = self.create_window_name()
        self.all_windows[name] = {"method": None,"title":None,"closed":False, "values": {}, "event": "", "event_function": None, "exit_events":None}
    return name
    ```
    **Purpose:**
    Register a window.

    **Arguments:**
    * obj (any, optional): The window to register. If not provided, a new window is created.

    **Returns:**
    * str: The name of the registered window.

  * `get_new_window`
    ```python
    def get_new_window(self, title:str=None, layout:list=None, args:dict=None, event_function:str=None,exit_events:(list or str)=None):
    """
    Create a new window.

    Args:
        title (str, optional): The title of the window. If not provided, 'window' is used.
        layout (list, optional): The layout of the window. If not provided, an empty layout is used.
        args (dict, optional): Additional arguments for the window.
        event_function (str, optional): The event function for the window.

    Returns:
        any: A new PySimpleGUI window.
    """
    args = verify_args(args=args, layout=layout, title=title, event_function=event_function,exit_events=exit_events)
    name = self.register_window()
    self.all_windows[name]["method"] = get_window(title=title, layout=layout, args=args)
    self.all_windows[name]["event_function"] = args["event_function"]
    self.all_windows[name]["exit_events"] = args["exit_events"]
    self.all_windows[name]["title"] = title
    return self.all_windows[name]["method"]
    ```
    **Purpose:**
    Create a new window.

    **Arguments:**
    * title (str, optional): The title of the window. If not provided, 'window' is used.
    * layout (list, optional): The layout of the window. If not provided, an empty layout is used.
    * args (dict, optional): Additional arguments for the window.
    * event_function (str, optional): The event function for the window.

    **Returns:**
    * any: A new PySimpleGUI window.

  * `search_global_windows`
    ```python
    def search_global_windows(self, window):
    """
    Search for a window in the global variables.

    Args:
        window (any): The window to search for.

    Returns:
        any: The name of the window if found, False otherwise.
    """
    window_names = self.get_window_names()
    if self.is_window_object(window):
        for name in window_names:
            if self.all_windows[name]["method"] == window:
                return name
    elif window in window_names:
        name = window
        return self.all_windows[window]["method"]
    return False
    ```
    **Purpose:**
    Search for a window in the global variables.

    **Arguments:**
    * window (any): The window to search for.

    **Returns:**
    * any: The name of the window if found, False otherwise.

  * `verify_window`
    ```python
    def verify_window(self, window=None) -> bool:
    """
    Verifies if the given object is a valid PySimpleGUI window.

    Args:
        win (any): The object to verify.

    Returns:
        bool: True if the object is a valid window, False otherwise.
    """
    return self.search_global_windows(window=window) != False
    ```
    **Purpose:**
    Verifies if the given object is a valid PySimpleGUI window.

    **Arguments:**
    * win (any): The object to verify.

    **Returns:**
    * bool: True if the object is a valid window, False otherwise.

  * `update_last_window`
    ```python
    def update_last_window(self, window):
    """
    Update the last accessed window.

    Args:
        window (any): The window to set as the last accessed window.
    """
    name = window
    if self.is_window_object(window):
        name = self.search_global_windows(window)
        if name is False:
            name = self.register_window(window)
    if name in self.get_window_names():
        self.all_windows['last_window'] = name
    ```
    **Purpose:**
    Update the last accessed window.

    **Arguments:**
    * window (any): The window to set as the last accessed window.

  * `send_to_bridge`
    ```python
    def send_to_bridge(self):
    """
    Update the global bridge with the current state of the windows.
    """
    self.global_vars["all_windows"] = self.all_windows
    self.global_bridge.retrieve_global_variables(self.script_name, self.global_vars)
    ```
    **Purpose:**
    Update the global bridge with the current state of the windows.

  * `close_window`
    ```python
    def close_window(self, window=None):
    """
    Closes the given PySimpleGUI window.

    Args:
        win (any): The window to close.
    """
    if self.verify_window(window):
        self.update_last_window(window)
        self.all_windows[self.search_global_windows(window)]["closed"] = True
        self.send_to_bridge()
        window.close()
    ```
    **Purpose:**
    Closes the given PySimpleGUI window.

    **Arguments:**
    * win (any): The window to close.

  * `read_window`
    ```python
    def read_window(self, window):
    """
    Read the event and values from a window and update the WindowManager's state.

    Args:
        window (any): The window to read from.
    """
    name = self.create_window_name()
    if self.is_window_object(window):
        name = self.search_global_windows(window)
        if name is False:
            name = self.register_window(window)
    if name not in self.get_window_names():
        return False
    window = self.all_windows[name]["method"]
    event, values = window.read()
    if event == self.close_window_element() and self.all_windows[name]["closed"] == False:
        self.all_windows[name]["closed"] = True
        self.all_windows[name]["event"] = 'EXIT'
        return 
    self.all_windows[name]["event"] = event
    self.all_windows[name]["values"] = values
    self.update_last_window(window)
    ```
    **Purpose:**
    Read the event and values from a window and update the WindowManager's state.

    **Arguments:**
    * window (any): The window to read from.

  * `get_last_window_info`
    ```python
    def get_last_window_info(self):
    """
    Retrieve the details of the last accessed window.

    Returns:
        dict: Dictionary containing information about the last accessed window or None if there's no such window.
    """
    last_window = self.all_windows['last_window']
    if last_window != None:
        return self.all_windows[last_window]
    ```
    **Purpose:**
    Retrieve the details of the last accessed window.

  * `get_last_window_method`
    ```python
    def get_last_window_method(self):
    """
    Get the method associated with the last accessed window.

    Returns:
        any: Method of the last accessed window or None if there's no such method.
    """
    window_info = self.get_last_window_info()
    if window_info != None:
        if "method" in window_info:
            return window_info["method"]

    ```
    **Purpose:**
    Get the method associated with the last accessed window.

  * `update_values`
    ```python
    def update_values(self, window=None, key:str=None, value:any=None, values:any=None, args:dict=None):
    """
    Update the values associated with a given window.

    Args:
        window (any, optional): The window to update values for. Defaults to the last accessed window.
        key (str, optional): The key to be updated in the window.
        value (any, optional): The value to set for the given key.
        values (any, optional): Multiple values to set.
        args (dict, optional): Additional arguments to update the window with.
    """
    if window == None:
        window = self.get_last_window_method()
    if window != None and key != None:
        if self.verify_window(window):
            if args == None:
                args = {}
            if values != None:
                args["values"]=values
            if value != None:
                args["value"]=value
            if args != {}:
                window[key].update(**args)
    ```
    **Purpose:**
    Update the values associated with a given window.

    **Arguments:**
    * window (any, optional): The window to update values for. Defaults to the last accessed window.
    * key (str, optional): The key to be updated in the window.
    * value (any, optional): The value to set for the given key.
    * values (any, optional): Multiple values to set.
    * args (dict, optional): Additional arguments to update the window with.

  * `get_event`
    ```python
    def get_event(self, window=None):
    """
    Get the last event from a window.

    Args:
        win (any, optional): The window to get the event from. If not provided, the last accessed window is used.

    Returns:
        any: The last event from the window.
    """
    if window is None:
        return self.all_windows[self.all_windows['last_window']]['event']
    name = self.search_global_windows(window)
    if name is not False:
        return self.all_windows[self.search_global_windows(window)]['event']

    ```
    **Purpose:**
    Get the last event from a window.

    **Arguments:**
    * win (any, optional): The window to get the event from. If not provided, the last accessed window is used.

    **Returns:**
    * any: The last event from the window.

  * `get_values`
    ```python
    def get_values(self, window=None):
    """
    Get the values from a window.

    Args:
        win (any, optional): The window to get the values from. If not provided, the last accessed window is used.

    Returns:
        dict: The values from the window.
    """
    if window is None:
        return self.all_windows[self.all_windows['last_window']]['values']
    name = self.search_global_windows(window)
    if name is not False:
        return self.all_windows[self.search_global_windows(window)]['values']

    ```
    **Purpose:**
    Get the values from a window.

    **Arguments:**
    * win (any, optional): The window to get the values from. If not provided, the last accessed window is used.

    **Returns:**
    * dict: The values from the window.

  * `while_basic`
    ```python
    def while_basic(self, window=None):
    """
    Run an event loop for a window.

    Args:
        window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.
    """
    self.global_vars = self.global_bridge.return_global_variables(self.script_name)
    while self.verify_window(window):
        self.read_window(window)
        if self.win_closed(window):
            self.close_window(window)
            return self.all_windows[self.search_global_windows(window)]["values"]  # Return the stored data instead of all_windows
        event_function = self.all_windows[self.search_global_windows(window)]["event_function"]

        if event_function is not None:
            self.global_vars[event_function](self.get_event(window))
    self.close_window(window)
    return self.all_windows  # Return the stored data instead of all_windows
    ```
    **Purpose:**
    Run an event loop for a window.

    **Arguments:**
    * window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.

  * `get_window_name`
    ```python
    def get_window_name(self, obj=None):
    """
    Get the names of all registered windows.

    Returns:
        list: A list of names of all registered windows.
    """
    window_names = self.get_window_names()
    if obj in window_names:
        name = obj
    if self.is_window_object(obj):
        name = self.search_global_windows(obj)
        if name is False:
            name = self.create_window_name()
    return name
    ```
    **Purpose:**
    Get the names of all registered windows.

  * `win_closed`
    ```python
    def win_closed(self, window):
    """
    Check if a window event calls to close the window.

    Args:
        event (str): The event to check.

    Returns:
        bool: True if the window is closed, False otherwise.
    """
    event = self.get_event(window)
    window_info = self.all_windows[self.search_global_windows(window)]
    exit_events = []
    if "exit_events" in window_info:
        exit_events = list(window_info['exit_events'])
    ```
    **Purpose:**
    Check if a window event calls to close the window.

    **Arguments:**
    * event (str): The event to check.

    **Returns:**
    * bool: True if the window is closed, False otherwise.

##### Stand Alone Functions
* `create_row`
  ```python
  def create_row(*args):
    """
    Create a row layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the row layout.

    Returns:
        list: A row layout containing the provided elements.
    """
    return [arg for arg in args]
  ```
  **Purpose:**
  Create a row layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the row layout.

  **Returns:**
  * list: A row layout containing the provided elements.

---
* `create_column`
  ```python
  def create_column(*args):
    """
    Create a column layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the column layout.

    Returns:
        list: A column layout containing the provided elements.
    """
    elements = []
    for arg in args:
        if isinstance(arg, list):  # If the argument is a list, expand it
            elements.extend(arg)
        else:
            elements.append(arg)
    return [[element] for element in elements]
  ```
  **Purpose:**
  Create a column layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the column layout.

  **Returns:**
  * list: A column layout containing the provided elements.

---
* `concatenate_rows`
  ```python
  def concatenate_rows(*args):
    """
    Concatenate multiple row layouts into a single row layout.

    Args:
        *args: Row layouts to be concatenated.

    Returns:
        list: A row layout containing concatenated elements from input row layouts.
    """
    result = []
    for arg in args:
        result += arg
    return result
  ```
  **Purpose:**
  Concatenate multiple row layouts into a single row layout.

  **Arguments:**
  * *args: Row layouts to be concatenated.

  **Returns:**
  * list: A row layout containing concatenated elements from input row layouts.

---
* `concatenate_layouts`
  ```python
  def concatenate_layouts(*args):
    """
    Concatenate multiple layouts into a single layout.

    Args:
        *args: Layouts to be concatenated.

    Returns:
        list: A layout containing concatenated elements from input layouts.
    """
    return concatenate_lists(args)
  ```
  **Purpose:**
  Concatenate multiple layouts into a single layout.

  **Arguments:**
  * *args: Layouts to be concatenated.

  **Returns:**
  * list: A layout containing concatenated elements from input layouts.

---
* `create_row_of_buttons`
  ```python
  def create_row_of_buttons(*args):
    """
    Create a row layout containing buttons generated from the provided arguments.

    Args:
        *args: Arguments for creating buttons.

    Returns:
        list: A row layout containing buttons created from the provided arguments.
    """
    return [button for arg in args for button in get_buttons(arg)]

  ```
  **Purpose:**
  Create a row layout containing buttons generated from the provided arguments.

  **Arguments:**
  * *args: Arguments for creating buttons.

  **Returns:**
  * list: A row layout containing buttons created from the provided arguments.

---
* `get_buttons`
  ```python
  def get_buttons(*args):
    """
    Generate button elements based on the provided arguments.

    Args:
        *args: Arguments specifying button elements.

    Returns:
        list: Button elements generated from the provided arguments.
    """
    if isinstance(args, tuple):
        args = [list(args)]
    # If no args or more than one arg, raise an exception
    if len(args) != 1:
        raise ValueError("The function expects a single argument which can be a str, dict, list, or tuple.")
    arg = args[0]
    arg_type = type(arg)

    # If it's a dictionary, use it as arguments for a single button
    if isinstance(arg, dict):
        return get_gui_fun("Button", args=arg)
    
    # If it's a string, use it as the text for a single button
    elif isinstance(arg, str):
        return get_gui_fun("Button", args={"button_text": arg})

    # If it's a list or tuple, iterate through its items
    elif isinstance(arg, (list, tuple)):
        buttons = []
        for each in arg:
            if isinstance(each, list):
               each = tuple(each)
            # For each string item, use it as the text for a button
            if isinstance(each, str):
                component = get_gui_fun("Button", args={"button_text": each})
      
            # If it's a tuple, consider first element as text and second as dictionary
            elif isinstance(each, tuple) and len(each) == 2 and isinstance(each[0], str) and isinstance(each[1], dict):
                btn_text = each[0]
                btn_args = each[1]
                btn_args["button_text"] = btn_text  # Add button_text to the arguments
                component = get_gui_fun("Button", args=btn_args)

            # For each dict item, use it as arguments for a button
            elif isinstance(each, dict):
                component = get_gui_fun("Button", args=each)

            else:
                raise ValueError("Unsupported item type in the list/tuple: {}".format(type(each)))
            buttons.append(component)
        return buttons
    else:
        raise ValueError("Unsupported argument type: {}".format(arg_type))

  ```
  **Purpose:**
  Generate button elements based on the provided arguments.

  **Arguments:**
  * *args: Arguments specifying button elements.

  **Returns:**
  * list: Button elements generated from the provided arguments.

---
* `if_not_window_make_window`
  ```python
  def if_not_window_make_window(window):
    """
    Checks if the provided object is a window and creates a new window if it isn't.
    
    Args:
        window: The object to be checked. If not a window, it's expected to be a dictionary with layout information.
        
    Returns:
        window: The valid window object.
    """
    if isinstance(window, type(get_window())) == False:
        if isinstance(window, dict):
            if "layout" in window:
                window["layout"]=ensure_nested_list(window["layout"])
        window=get_window(args=window)
    return window
  ```
  **Purpose:**
  Checks if the provided object is a window and creates a new window if it isn't.

  **Arguments:**
  * window: The object to be checked. If not a window, it's expected to be a dictionary with layout information.

  **Returns:**
  * window: The valid window object.

---
* `while_quick`
  ```python
  def while_quick(window,return_events:(list or str)=[],exit_events:(list or str)=[sg.WIN_CLOSED],event_return=False):
    """
    Reads events from the given window and handles them based on the provided conditions.
    
    Args:
        window: The window to read events from.
        return_events (list or str): Events that would lead to the window being closed and a value returned.
        exit_events (list or str): Events that would lead to the window being closed without returning a value.
        event_return (bool): If True, returns the event. If False, returns the values.
        
    Returns:
        event or values: Depending on the event_return flag.
    """
    exit_events = make_list_add(exit_events,[sg.WIN_CLOSED])
    return_events = list(return_events)
    last_values=[]
    while True:
        event, values = window.read()
        if event ==sg.WIN_CLOSED:
            window.close()
            values= None
            break
        elif event in return_events:
            window.close()
            break
    if event_return == True:
        return event
    return values  
      
  ```
  **Purpose:**
  Reads events from the given window and handles them based on the provided conditions.

  **Arguments:**
  * window: The window to read events from.
  * return_events (list or str): Events that would lead to the window being closed and a value returned.
  * exit_events (list or str): Events that would lead to the window being closed without returning a value.
  * event_return (bool): If True, returns the event. If False, returns the values.

  **Returns:**
  * event or values: Depending on the event_return flag.

---
* `verify_args`
  ```python
  def verify_args(args:dict=None, layout:list=None, title:str=None, event_function:str=None,exit_events:(list or str)=None):
    """
    Verifies and/or sets default values for window arguments.
    
    Args:
        args (dict, optional): Dictionary containing window arguments.
        layout (list, optional): The layout for the window.
        title (str, optional): The title of the window.
        event_function (str, optional): The function to be executed when an event occurs.
        exit_events (list or str, optional): List of events that would close the window.
        
    Returns:
        dict: The verified/updated window arguments.
    """
    args = args or {}
    layout = layout or [[]]
    title = title or 'window'
    exit_events = exit_events or ["exit", "Exit", "EXIT"]
    args.setdefault("title", title)
    args.setdefault("layout", ensure_nested_list(layout))
    args.setdefault("event_function", event_function)
    args.setdefault("exit_events", list(exit_events))
    return args
  ```
  **Purpose:**
  Verifies and/or sets default values for window arguments.

  **Arguments:**
  * args (dict, optional): Dictionary containing window arguments.
  * layout (list, optional): The layout for the window.
  * title (str, optional): The title of the window.
  * event_function (str, optional): The function to be executed when an event occurs.
  * exit_events (list or str, optional): List of events that would close the window.

  **Returns:**
  * dict: The verified/updated window arguments.

---
* `get_window`
  ```python
  def get_window(title=None, layout=None, args=None):
    """
    Get a PySimpleGUI window.

    Args:
        win_name (str, optional): The name of the window. If not provided, a unique name is generated.
        layout (list, optional): The layout of the window. If not provided, an empty layout is used.
        args (dict, optional): Additional arguments for the window.

    Returns:
        any: A PySimpleGUI window.
    """
    args = verify_args(args=args, layout=layout, title=title)
    return get_gui_fun('Window', {**args})
  ```
  **Purpose:**
  Get a PySimpleGUI window.

  **Arguments:**
  * win_name (str, optional): The name of the window. If not provided, a unique name is generated.
  * layout (list, optional): The layout of the window. If not provided, an empty layout is used.
  * args (dict, optional): Additional arguments for the window.

  **Returns:**
  * any: A PySimpleGUI window.

---
* `get_browser_layout`
  ```python
  def get_browser_layout(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path()):
    """
    Function to get a browser GUI based on the type specified.

    Parameters:
    type (str): The type of GUI window to display. Defaults to 'Folder'.
    title (str): The title of the GUI window. Defaults to 'Directory'.

    Returns:
    dict: Returns the results of single_call function on the created GUI window.
    """
    if type.lower() not in 'folderdirectory':
        type = 'File'
    else:
        type = 'Folder'
    if title is None:
        title = f'Please choose a {type.lower()}'
    layout = [
        [get_gui_fun('Text', {"text": title})],
        [get_gui_fun('Input',args={"default":initial_folder,"key":"output"}), get_gui_fun(f'{type}Browse', {**args, "initial_folder": initial_folder})],
        [get_gui_fun('OK'), get_gui_fun('Cancel')]
    ]
    return {"title": f'{type} Explorer', "layout": layout}
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* `get_yes_no_layout`
  ```python
  def get_yes_no_layout(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={}):
    """
    Creates a layout for a Yes/No window.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        args (dict, optional): Additional arguments for the window.
        
    Returns:
        dict: The layout dictionary.
    """
    layout = [
        [get_gui_fun('Text', {"text": text})],
        [sg.Button('Yes'), sg.Button('No')]
    ]
    return {"title":title, "layout": layout,**args}
  ```
  **Purpose:**
  Creates a layout for a Yes/No window.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * args (dict, optional): Additional arguments for the window.

  **Returns:**
  * dict: The layout dictionary.

---
* `get_input_layout`
  ```python
  def get_input_layout(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={}):
    """
    Function to get a browser GUI based on the type specified.

    Parameters:
    type (str): The type of GUI window to display. Defaults to 'Folder'.
    title (str): The title of the GUI window. Defaults to 'Directory'.

    Returns:
    dict: Returns the results of single_call function on the created GUI window.
    """
    if type.lower() not in 'folderdirectory':
        type = 'File'
    else:
        type = 'Folder'
    if title is None:
        title = f'Please choose a {type.lower()}'
    if "default" not in args:
        args["default"]=default
    if "key" not in args:
        args["key"]=key
    if "text" in args:
        text = args["text"]
    layout = [
        [get_gui_fun('Text', {"text": text})],
        [get_gui_fun('Input',args=args)],
        [get_gui_fun('OK'), get_gui_fun('Cancel')]
    ]
    return {"title":title, "layout": layout}
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* `get_yes_no`
  ```python
  def get_yes_no(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={},exit_events:(str or list)=[],return_events:(str or list)=["Yes","No"],event_return=True):
    """
    Creates and displays a Yes/No window, then captures the user response.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        args (dict, optional): Additional arguments for the window.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to a response being returned.
        event_return (bool, optional): If True, returns the event. If False, returns the values.
        
    Returns:
        event or values: Depending on the event_return flag.
    """
    window = get_window(args=get_yes_no_layout(title=title,text=text))
    return while_quick(window=window,exit_events=exit_events,return_events=return_events,event_return=event_return)
  ```
  **Purpose:**
  Creates and displays a Yes/No window, then captures the user response.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * args (dict, optional): Additional arguments for the window.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to a response being returned.
  * event_return (bool, optional): If True, returns the event. If False, returns the values.

  **Returns:**
  * event or values: Depending on the event_return flag.

---
* `get_input`
  ```python
  def get_input(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={},exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK']):
    """
    Creates and displays an input window, then captures the user input.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        default (str, optional): The default input value.
        args (dict, optional): Additional arguments for the window.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to an input being returned.
        
    Returns:
        values: The captured user input.
    """
    window = get_window(args=get_input_layout(title=title,text=text,args=args,default=default,initial_folder=initial_folder))
    return while_quick(window=window,exit_events=exit_events,return_events=return_events)
    
  ```
  **Purpose:**
  Creates and displays an input window, then captures the user input.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * default (str, optional): The default input value.
  * args (dict, optional): Additional arguments for the window.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to an input being returned.

  **Returns:**
  * values: The captured user input.

---
* `get_browser`
  ```python
  def get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path(),exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK']):
    """
    Creates and displays a browser window, then captures the user-selected path.
    
    Args:
        title (str, optional): The title of the window.
        type (str, optional): The type of browser (e.g., 'Folder').
        args (dict, optional): Additional arguments for the window.
        initial_folder (str, optional): The folder to start browsing from.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to a path being returned.
        
    Returns:
        results: The selected path or default path if none is selected.
    """
    window = get_window(args=get_browser_layout(title=title,type=type,args=args,initial_folder=initial_folder))
    results = while_quick(window=window,exit_events=exit_events,return_events=return_events)
    if isinstance(results, dict):
        if results['output']=='':
            results['output'] = initial_folder
    if results == None:
        results={'output':initial_folder}
    return results['output']
  ```
  **Purpose:**
  Creates and displays a browser window, then captures the user-selected path.

  **Arguments:**
  * title (str, optional): The title of the window.
  * type (str, optional): The type of browser (e.g., 'Folder').
  * args (dict, optional): Additional arguments for the window.
  * initial_folder (str, optional): The folder to start browsing from.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to a path being returned.

  **Returns:**
  * results: The selected path or default path if none is selected.

---
* `get_gui_fun`
  ```python
  def get_gui_fun(name: str = '', args: dict = {}):
    """
    Returns a callable object for a specific PySimpleGUI function with the provided arguments.

    Args:
        name (str): The name of the PySimpleGUI function.
        args (dict): The arguments to pass to the PySimpleGUI function.

    Returns:
        callable: A callable object that invokes the PySimpleGUI function with the specified arguments when called.
    """
    return get_fun({"instance": sg, "name": name, "args": args})
  ```
  **Purpose:**
  Returns a callable object for a specific PySimpleGUI function with the provided arguments.

  **Arguments:**
  * name (str): The name of the PySimpleGUI function.
  * args (dict): The arguments to pass to the PySimpleGUI function.

  **Returns:**
  * callable: A callable object that invokes the PySimpleGUI function with the specified arguments when called.

---
* `create_window_manager`
  ```python
  def create_window_manager(script_name='default_script_name',global_var=globals()):
    """
    Initializes a window manager for a given script.
    
    Args:
        script_name (str, optional): The name of the script.
        global_var (dict, optional): The global variables associated with the script.
        
    Returns:
        tuple: A tuple containing the WindowManager, bridge, and script name.
    """
    bridge = WindowGlobalBridge()
    script_name = bridge.create_script_name(script_name)
    global_var[script_name] = script_name
    js_bridge = bridge.retrieve_global_variables(script_name, global_var)
    return WindowManager(script_name, bridge),bridge,script_name

  ```
  **Purpose:**
  Initializes a window manager for a given script.

  **Arguments:**
  * script_name (str, optional): The name of the script.
  * global_var (dict, optional): The global variables associated with the script.

  **Returns:**
  * tuple: A tuple containing the WindowManager, bridge, and script name.

---

## Example Usage

```python
# Import the module
import abstract_gui

# Create a global bridge instance
global_bridge = abstract_gui.WindowGlobalBridge()

# Create a window manager instance for a script named "example_script"; interacts with the global bridge for modular event handling for script specific functions
window_manager = abstract_gui.WindowManager("example_script", global_bridge)

#or use the window_manager initialization function
window_mgr,bridge,script_name = abstract_gui.create_window_manager(script_name="example_script",global_var=globals())

#Create components for a layout
#input args, a dictionary with window parameters for any and all parameter inputs. an incompatible parameter will not be applied, error free component utilization
layout = abstract_gui.get_gui_fun('Text', args={"text": "Hello, PySimpleGUI!"})

#make component expandable (it will not error out if arguments are incompatible); with customizable legacy inputs
#Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.
expand = abstract_gui.expandable()

# Create a new PySimpleGUI window using the window manager, add the stringified function name as event_function for binded event handling
#get_new_window(self, title=None, layout=None, args=None, event_function=None, exit_events:list=["exit", "Exit", "EXIT"])
window = window_manager.get_new_window(title="Example Window", args={"layout":[[layout]],**expand})

# Run the event loop for the window
window_manager.while_basic(window)

# Retrieve all registered windows and their details
all_windows = window_manager.get_all_windows()
```

```python
import PySimpleGUI as sg
# ... [Other necessary imports and your provided functions and class]

# Initialize the window manager
window_manager, _, script_name = create_window_manager(script_name="MyScript")

layout = [
    [sg.Text("Hello from PySimpleGUI!")],
    [sg.Button("Exit")]
]

window = sg.Window("My Window", layout, **expandable())

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

window.close()
```
Please refer to the source code for the complete list of classes and functions provided by the module, as well as their detailed documentation.

## Contributing

Contributions are welcome! Please fork this repository and open a pull request to add snippets, make grammar tweaks, etc.

## Contact

If you have any questions, feel free to reach out to us at partners@abstractendeavors.com.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

* putkoff - main developer


For detailed usage, parameter information, and return types, please refer to the individual method documentation.

## Bug Reports & Contact
For any bugs or issues, please report on the [Github page](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_gui). For direct queries, you can email the team at [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com).

---
