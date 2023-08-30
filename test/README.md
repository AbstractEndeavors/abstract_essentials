# Abstract Essentials

## Description

### Use
* Explanation of how to use the package.


## Abstract GUI
### Description
* Brief description of the module.

### Features
* Feature 1
* Feature 2
* ... 

### Dependencies

#### Dependency Name 1


### abstract_gui.py
#### Functions
##### Class Functions
###### WindowGlobalBridge
* **Attributes**
  * `global_vars (dict)`:  A dictionary to store global variables for each script.
* **Methods**
  * **__init__**
    ```python
    __init__(self)
  ```
    **Purpose:**
    Initializes the WindowGlobalBridge with an empty dictionary for global_vars.

  * **retrieve_global_variables**
    ```python
    retrieve_global_variables(self, script_name:str, global_variables:dict, tag_script_name:bool=False)
  ```
    **Purpose:**
    Stores the global variables of a script in the global_vars dictionary.

    **Arguments:**
    * script_name (str): The name of the script.
    * global_variables (dict): The global variables to store for the script.
    * tag_script_name (bool, optional): If True, the script_name will be stored in the global_variables dictionary. Defaults to False.

  * **return_global_variables**
    ```python
    return_global_variables(self, script_name=None)
  ```
    **Purpose:**
    Returns the global variables of a script.

    **Arguments:**
    * script_name (str, optional): The name of the script. If None, all global variables will be returned.

    **Returns:**
    * dict: The global variables of the script. If no global variables are found, it returns an empty dictionary.

  * **change_globals**
    ```python
    change_globals(self, variable:str, value:any, script_name:str=None)
  ```
    **Purpose:**
    Modifies a global variable value for a specified script.

    **Arguments:**
    * variable (str): The name of the global variable to modify.
    * value (any): The new value to assign to the global variable.
    * script_name (str, optional): The name of the script. If None, the global variable in the base context will be modified.

  * **search_globals_values**
    ```python
    search_globals_values(self, value:any, script_name:str=None)
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
  * **__init__**
    ```python
    __init__(self, script_name, global_bridge)
  ```
    **Purpose:**
    Initialize a WindowManager instance.

    **Arguments:**
    * script_name (str): The name of the script that is using the WindowManager.
    * global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.

  * **get_all_windows**
    ```python
    get_all_windows(self)
  ```
    **Purpose:**
    Get all registered windows.

  * **get_window_names**
    ```python
    get_window_names(self)
  ```
    **Purpose:**
    Get the names of all registered windows.

  * **register_window**
    ```python
    register_window(self, window=None)
  ```
    **Purpose:**
    Register a window.

    **Arguments:**
    * obj (any, optional): The window to register. If not provided, a new window is created.

    **Returns:**
    * str: The name of the registered window.

  * **get_new_window**
    ```python
    get_new_window(self, title:str=None, layout:list=None, args:dict=None, event_function:str=None,exit_events:(list or str)=None)
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

  * **search_global_windows**
    ```python
    search_global_windows(self, window)
  ```
    **Purpose:**
    Search for a window in the global variables.

    **Arguments:**
    * window (any): The window to search for.

    **Returns:**
    * any: The name of the window if found, False otherwise.

  * **verify_window**
    ```python
    verify_window(self, window=None) -> bool
  ```
    **Purpose:**
    Verifies if the given object is a valid PySimpleGUI window.

    **Arguments:**
    * win (any): The object to verify.

    **Returns:**
    * bool: True if the object is a valid window, False otherwise.

  * **update_last_window**
    ```python
    update_last_window(self, window)
  ```
    **Purpose:**
    Update the last accessed window.

    **Arguments:**
    * window (any): The window to set as the last accessed window.

  * **send_to_bridge**
    ```python
    send_to_bridge(self)
  ```
    **Purpose:**
    Update the global bridge with the current state of the windows.

  * **close_window**
    ```python
    close_window(self, window=None)
  ```
    **Purpose:**
    Closes the given PySimpleGUI window.

    **Arguments:**
    * win (any): The window to close.

  * **read_window**
    ```python
    read_window(self, window)
  ```
    **Purpose:**
    Read the event and values from a window and update the WindowManager's state.

    **Arguments:**
    * window (any): The window to read from.

  * **get_last_window_info**
    ```python
    get_last_window_info(self)
  ```
    **Purpose:**
    Retrieve the details of the last accessed window.

  * **get_last_window_method**
    ```python
    get_last_window_method(self)
  ```
    **Purpose:**
    Get the method associated with the last accessed window.

  * **update_values**
    ```python
    update_values(self, window=None, key:str=None, value:any=None, values:any=None, args:dict=None)
  ```
    **Purpose:**
    Update the values associated with a given window.

    **Arguments:**
    * window (any, optional): The window to update values for. Defaults to the last accessed window.
    * key (str, optional): The key to be updated in the window.
    * value (any, optional): The value to set for the given key.
    * values (any, optional): Multiple values to set.
    * args (dict, optional): Additional arguments to update the window with.

  * **get_event**
    ```python
    get_event(self, window=None)
  ```
    **Purpose:**
    Get the last event from a window.

    **Arguments:**
    * win (any, optional): The window to get the event from. If not provided, the last accessed window is used.

    **Returns:**
    * any: The last event from the window.

  * **get_values**
    ```python
    get_values(self, window=None)
  ```
    **Purpose:**
    Get the values from a window.

    **Arguments:**
    * win (any, optional): The window to get the values from. If not provided, the last accessed window is used.

    **Returns:**
    * dict: The values from the window.

  * **while_basic**
    ```python
    while_basic(self, window=None)
  ```
    **Purpose:**
    Run an event loop for a window.

    **Arguments:**
    * window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.

  * **get_window_name**
    ```python
    get_window_name(self, obj=None)
  ```
    **Purpose:**
    Get the names of all registered windows.

  * **win_closed**
    ```python
    win_closed(self, window)
  ```
    **Purpose:**
    Check if a window event calls to close the window.

    **Arguments:**
    * event (str): The event to check.

    **Returns:**
    * bool: True if the window is closed, False otherwise.

  * **delete_from_list**
    ```python
    delete_from_list(self, _list, var)
  ```
    **Purpose:**
    Remove a specific variable from a list.

    **Arguments:**
    * _list (list): The list to remove the variable from.
    * var (any): The variable to remove from the list.

    **Returns:**
    * list: A list with the specified variable removed.

  * **is_window_object**
    ```python
    is_window_object(self, obj)
  ```
    **Purpose:**
    Check if an object is a PySimpleGUI window object.

    **Arguments:**
    * obj (any): The object to check.

    **Returns:**
    * bool: True if the object is a window object, False otherwise.

  * **create_window_name**
    ```python
    create_window_name(self)
  ```
    **Purpose:**
    Create a unique name for a window.

  * **close_window_element**
    ```python
    close_window_element(self)
  ```
    **Purpose:**
    Get the constant representing a closed window event in PySimpleGUI.

  * **unregister_window**
    ```python
    unregister_window(self, window)
  ```
    **Purpose:**
    Unregister a window from the WindowManager.

    **Arguments:**
    * window (any): The window to unregister.

##### Stand Alone Functions
* **create_row**
  ```python
  create_row(*args)
  ```
  **Purpose:**
  Create a row layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the row layout.

  **Returns:**
  * list: A row layout containing the provided elements.

---
* **create_column**
  ```python
  create_column(*args)
  ```
  **Purpose:**
  Create a column layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the column layout.

  **Returns:**
  * list: A column layout containing the provided elements.

---
* **concatenate_rows**
  ```python
  concatenate_rows(*args)
  ```
  **Purpose:**
  Concatenate multiple row layouts into a single row layout.

  **Arguments:**
  * *args: Row layouts to be concatenated.

  **Returns:**
  * list: A row layout containing concatenated elements from input row layouts.

---
* **concatenate_layouts**
  ```python
  concatenate_layouts(*args)
  ```
  **Purpose:**
  Concatenate multiple layouts into a single layout.

  **Arguments:**
  * *args: Layouts to be concatenated.

  **Returns:**
  * list: A layout containing concatenated elements from input layouts.

---
* **create_row_of_buttons**
  ```python
  create_row_of_buttons(*args)
  ```
  **Purpose:**
  Create a row layout containing buttons generated from the provided arguments.

  **Arguments:**
  * *args: Arguments for creating buttons.

  **Returns:**
  * list: A row layout containing buttons created from the provided arguments.

---
* **get_buttons**
  ```python
  get_buttons(*args)
  ```
  **Purpose:**
  Generate button elements based on the provided arguments.

  **Arguments:**
  * *args: Arguments specifying button elements.

  **Returns:**
  * list: Button elements generated from the provided arguments.

---
* **if_not_window_make_window**
  ```python
  if_not_window_make_window(window)
  ```
  **Purpose:**
  Checks if the provided object is a window and creates a new window if it isn't.

  **Arguments:**
  * window: The object to be checked. If not a window, it's expected to be a dictionary with layout information.

  **Returns:**
  * window: The valid window object.

---
* **while_quick**
  ```python
  while_quick(window,return_events:(list or str)=[],exit_events:(list or str)=[sg.WIN_CLOSED],event_return=False)
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
* **verify_args**
  ```python
  verify_args(args:dict=None, layout:list=None, title:str=None, event_function:str=None,exit_events:(list or str)=None)
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
* **get_window**
  ```python
  get_window(title=None, layout=None, args=None)
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
* **get_browser_layout**
  ```python
  get_browser_layout(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path())
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* **get_yes_no_layout**
  ```python
  get_yes_no_layout(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={})
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
* **get_input_layout**
  ```python
  get_input_layout(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={})
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* **get_yes_no**
  ```python
  get_yes_no(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={},exit_events:(str or list)=[],return_events:(str or list)=["Yes","No"],event_return=True)
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
* **get_input**
  ```python
  get_input(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={},exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK'])
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
* **get_browser**
  ```python
  get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path(),exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK'])
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
* **get_gui_fun**
  ```python
  get_gui_fun(name: str = '', args: dict = {})
  ```
  **Purpose:**
  Returns a callable object for a specific PySimpleGUI function with the provided arguments.

  **Arguments:**
  * name (str): The name of the PySimpleGUI function.
  * args (dict): The arguments to pass to the PySimpleGUI function.

  **Returns:**
  * callable: A callable object that invokes the PySimpleGUI function with the specified arguments when called.

---
* **create_window_manager**
  ```python
  create_window_manager(script_name='default_script_name',global_var=globals())
  ```
  **Purpose:**
  Initializes a window manager for a given script.

  **Arguments:**
  * script_name (str, optional): The name of the script.
  * global_var (dict, optional): The global variables associated with the script.

  **Returns:**
  * tuple: A tuple containing the WindowManager, bridge, and script name.

---
### Usage

* **Use:** Explanation of how to use the function/class.

### Module Information

* **Info:** Additional information or context about the module component.

### Usage

#### Use
* Explanation of how to use the module.

### Module Information

#### Info
* Additional information or context about the module.
