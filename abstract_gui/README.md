# Abstract GUI Module

The `abstract_gui` module provides classes and functions to manage PySimpleGUI windows and events in a more abstract manner. It includes a class called `WindowGlobalBridge` to manage global variables shared between different scripts and a class called `WindowManager` to manage PySimpleGUI windows and their events.

## Installation

You can install the `abstract_gui` module using `pip`:

```
pip install abstract_gui
```

## `WindowGlobalBridge` Class

A class to manage the global variables shared between different scripts.

### Attributes:

- `global_vars` (dict): A dictionary to store global variables for each script.

### Methods:

#### `__init__(self)`

Initializes the `WindowGlobalBridge` with an empty dictionary for `global_vars`.

#### `retrieve_global_variables(self, script_name, global_variables)`

Stores the global variables of a script in the `global_vars` dictionary.

- Args:
  - `script_name` (str): The name of the script.
  - `global_variables` (dict): The global variables to store for the script.

#### `return_global_variables(self, script_name)`

Returns the global variables of a script.

- Args:
  - `script_name` (str): The name of the script.

- Returns:
  - `dict`: The global variables of the script. If no global variables are found, it returns an empty dictionary.

## `WindowManager` Class

A class to manage PySimpleGUI windows and their events.

### Attributes:

- `all_windows` (dict): A dictionary to store registered windows along with their details.
- `last_window` (str): The name of the last accessed window.
- `script_name` (str): The name of the script that is using the `WindowManager`.
- `global_bridge`: The global bridge to access shared variables between different scripts.
- `global_vars` (dict): A dictionary to store global variables for this script.

### Methods:

#### `__init__(self, script_name, global_bridge)`

Initialize a `WindowManager` instance.

- Args:
  - `script_name` (str): The name of the script that is using the `WindowManager`.
  - `global_bridge` (`WindowGlobalBridge`): An instance of `WindowGlobalBridge` to access shared variables between different scripts.

#### `get_all_windows(self)`

Get all registered windows.

- Returns:
  - `dict`: A dictionary containing all registered windows and their details.

#### `get_window_names(self)`

Get the names of all registered windows.

- Returns:
  - `list`: A list of names of all registered windows.

#### `register_window(self, window=None)`

Register a window.

- Args:
  - `window` (any, optional): The window to register. If not provided, a new window is created.

- Returns:
  - `str`: The name of the registered window.

#### `get_new_window(self, title=None, layout=None, args=None, event_function=None)`

Create a new window.

- Args:
  - `title` (str, optional): The title of the window. If not provided, 'window' is used.
  - `layout` (list, optional): The layout of the window. If not provided, an empty layout is used.
  - `args` (dict, optional): Additional arguments for the window.
  - `event_function` (str, optional): The event function for the window.

- Returns:
  - `any`: A new PySimpleGUI window.

#### `search_global_windows(self, window)`

Search for a window in the global variables.

- Args:
  - `window` (any): The window to search for.

- Returns:
  - `any`: The name of the window if found, False otherwise.

#### `verify_window(self, window=None)`

Verifies if the given object is a valid PySimpleGUI window.

- Args:
  - `window` (any): The object to verify.

- Returns:
  - `bool`: True if the object is a valid window, False otherwise.

#### `update_last_window(self, window)`

Update the last accessed window.

- Args:
  - `window` (any): The window to set as the last accessed window.

#### `send_to_bridge(self)`

Update the global bridge with the current `all_windows` dictionary.

#### `close_window(self, window=None)`

Closes the given PySimpleGUI window.

- Args:
  - `window` (any): The window to close.

#### `read_window(self, window)`

Read the event and values from a window and update the `WindowManager`'s state.

- Args:
  - `window` (any): The window to read from.

#### `get_event(self, window=None)`

Get the last event from a window.

- Args:
  - `window` (any, optional): The window to get the event from. If not provided, the last accessed window is used.

- Returns:
  - `any`: The last event from the window.

#### `get_values(self, window=None)`

Get the values from a window.

- Args:
  - `window` (any, optional): The window to get the values from. If not provided, the last accessed window is used.

- Returns:
  - `dict`: The values from the window.

#### `while_basic(self, window=None)`

Run an event loop for a window.

- Args:
  - `window` (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.

- Returns:
  - `dict`: The stored data instead of `all_windows`.

#### `get_window_name(self, obj=None)`

Get the names of all registered windows.

- Returns:
  - `list`: A list of names of all registered windows.

#### `win_closed(self, event='')`

Check if a window event calls to close the window.

- Args:
  - `event` (str): The event to check.

- Returns:
  - `bool`: True if the window is closed, False otherwise.

#### `delete_from_list(self, _list, var)`

Remove occurrences of a variable from a list and returns the new list.

- Args:
  - `_list` (list): The list to remove occurrences from.
  - `var`: The variable to remove from the list.

- Returns:
  - `list`: The new list without the occurrences of `var`.

#### `is_window_object(self, obj)`

Check if an object is a PySimpleGUI window object.

- Args:
  - `obj` (any): The object to check.

- Returns:
  - `bool`: True if the object is a window object, False otherwise.

#### `create_window_name(self)`

Create a unique name for a window.

- Returns:
  - `str`: A unique name for a window.

#### `unregister_window(self, window)`

Unregister a window.

- Args:
  - `window` (any): The window to unregister.

## Helper Functions

The module also includes several helper functions:

- `get_window(title=None, layout=None, args=None)`: Get a PySimpleGUI window.
- `out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -

1)`: Checks if the given object is out of the specified upper and lower bounds.
- `det_bool_F(obj: (tuple or list or bool) = False)`: Determines if the given object is a boolean False value.
- `det_bool_T(obj: (tuple or list or bool) = False)`: Determines if the given object is a boolean True value.
- `T_or_F_obj_eq(event: any = '', obj: any = '')`: Compares two objects and returns True if they are equal, False otherwise.
- `get_gui_fun(name: str = '', args: dict = {})`: Returns a callable object for a specific PySimpleGUI function with the provided arguments.
- `expandable(size: tuple = (None, None))`: Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.
- `get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path())`: Function to get a browser GUI based on the type specified.

## Example Usage

```python
# Import the module
import abstract_gui

# Create a global bridge instance
global_bridge = abstract_gui.WindowGlobalBridge()

# Create a window manager instance for a script named "example_script"
window_manager = abstract_gui.WindowManager("example_script", global_bridge)

# Create a new PySimpleGUI window using the window manager
window = window_manager.get_new_window(title="Example Window", layout=[[abstract_gui.get_gui_fun('Text', {"text": "Hello, PySimpleGUI!"})]])

# Run the event loop for the window
window_manager.while_basic(window)

# Close the window
window_manager.close_window(window)

# Retrieve all registered windows and their details
all_windows = window_manager.get_all_windows()
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

This README file was last updated on May 29, 2023.
