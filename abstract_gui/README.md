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

### Additional Functionality
- Here are some non-class methods that add more capabilities to the module:

### `ensure_nested_list(obj)`
- Ensure that the input object is a nested list.

- **Parameters**:
  - `obj` (any): The object to ensure as a nested list.

- **Returns**:
  - `list`: A nested list containing the object or the original list if it's already nested.

### `create_row(*args)`
- Create a row layout containing the provided arguments.

- **Parameters**:
  - `*args`: Elements to be placed in the row layout.

- **Returns**:
  - `list`: A row layout containing the provided elements.

### `create_column(*args)`
- Create a column layout containing the provided arguments.

- **Parameters**:
  - `*args`: Elements to be placed in the column layout.

- **Returns**:
  - `list`: A column layout containing the provided elements.

### `concatenate_rows(*args)`
- Concatenate multiple row layouts into a single row layout.

- **Parameters**:
  - `*args`: Row layouts to be concatenated.

- **Returns**:
  - `list`: A row layout containing concatenated elements from input row layouts.

### `concatenate_layouts(*args)`
- Concatenate multiple layouts into a single layout.

- **Parameters**:
  - `*args`: Layouts to be concatenated.

- **Returns**:
  - `list`: A layout containing concatenated elements from input layouts.

### `create_row_of_buttons(*args)`
- Create a row layout containing buttons generated from the provided arguments.

- **Parameters**:
  - `*args`: Arguments for creating buttons.

- **Returns**:
  - `list`: A row layout containing buttons created from the provided arguments.

### `get_buttons(*args)`
Generate button elements based on the provided arguments.

- **Parameters**:
  - `*args`: Arguments specifying button elements.

- **Returns**:
  - `list`: Button elements generated from the provided arguments.

### `make_list_add(obj, values)`
- Add multiple values to a list and return the resulting list.

- **Parameters**:
  - `obj` (list): The original list.
  - `values` (iterable): Values to be added to the list.

- **Returns**:
  - `list`: The modified list containing the original elements and the added values.

### `if_not_window_make_window(window)`
- Checks if the provided object is a window and creates a new window if it isn't.

- **Parameters**:
  - `window`: The object to be checked. If not a window, it's expected to be a dictionary with layout information.

- **Returns**:
  - `window`: The valid window object.

### `while_quick(window, return_events=[], exit_events=[sg.WIN_CLOSED], event_return=False)`
- Reads events from the given window and handles them based on the provided conditions.

- **Parameters**:
  - `window`: The window to read events from.
  - `return_events` (list or str): Events that would lead to the window being closed and a value returned.
  - `exit_events` (list or str): Events that would lead to the window being closed without returning a value.
  - `event_return` (bool): If True, returns the event. If False, returns the values.

- **Returns**:
  - `event` or `values`: Depending on the `event_return` flag.

### `verify_args(args=None, layout=None, title=None, event_function=None, exit_events=None)`
- Verifies and/or sets default values for window arguments.

- **Parameters**:
  - `args` (dict, optional): Dictionary containing window arguments.
  - `layout` (list, optional): The layout for the window.
  - `title` (str, optional): The title of the window.
  - `event_function` (str, optional): The function to be executed when an event occurs.
  - `exit_events` (list or str, optional): List of events that would close the window.

- **Returns**:
  - `dict`: The verified/updated window arguments.

### `get_window(title=None, layout=None, args=None)`
- Get a PySimpleGUI window.

- **Parameters**:
  - `title` (str, optional): The name of the window.
  - `layout` (list, optional): The layout of the window.
  - `args` (dict, optional): Additional arguments for the window.

- **Returns**:
  - `any`: A PySimpleGUI window.

### `get_browser_layout(title=None, type='Folder', args={}, initial_folder=get_current_path())`
- Function to get a browser GUI based on the type specified.

**Parameters**:
- `title` (str): The title of the GUI window. Defaults to 'Directory'.
- `type` (str): The type of GUI window to display. Defaults to 'Folder'.
- `args` (dict): Additional arguments for the window.
- `initial_folder` (str): The starting folder for browsing.

**Returns**:
- `dict`: Returns the results of single_call function on the created GUI window.

### `get_yes_no_layout(title="Answer Window", text="would you like to proceed?", args={})`
Creates a layout for a Yes/No window.

**Parameters**:
- `title` (str, optional): The title of the window.
- `text` (str, optional): The prompt text.
- `args` (dict, optional): Additional arguments for the window.

**Returns**:
- `dict`: The layout dictionary.

### `get_input_layout(title="Input Window", text="please enter your input", default=None, args={})`
Function to get an input GUI window layout.

**Parameters**:
- `title` (str, optional): The title of the window.
- `text` (str, optional): The prompt text.
- `default` (str, optional): The default input value.
- `args` (dict, optional): Additional arguments for the window.

**Returns**:
- `dict`: The layout dictionary.

Please let me know if you need the rest of the function descriptions to be formatted in Markdown as well.

**T_or_F_obj_eq(event, obj)**
- Compares two objects and returns `True` if they are equal, `False` otherwise.
- **Parameters**:
  - `event` (any): The first object to compare.
  - `obj` (any): The second object to compare.
- **Returns**: `True` if the objects are equal, `False` otherwise.

**get_gui_fun(name, args)**
- Returns a callable object for a specific PySimpleGUI function with the provided arguments.
- **Parameters**:
  - `name` (str): The name of the PySimpleGUI function.
  - `args` (dict): The arguments to pass to the PySimpleGUI function.
- **Returns**: A callable object that invokes the PySimpleGUI function with the specified arguments when called.

**expandable(size, resizable, scrollable, auto_size_text, expand_x, expand_y)**
- Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.
- **Parameters**:
  - `size` (tuple, default=(None, None)): The desired size of the window.
  - `resizable` (bool, default=True): Whether the window is resizable or not.
  - `scrollable` (bool, default=True): Whether the window content is scrollable.
  - `auto_size_text` (bool, default=True): Whether to automatically adjust text size.
  - `expand_x` (bool, default=True): Allow horizontal expansion.
  - `expand_y` (bool, default=True): Allow vertical expansion.
- **Returns**: A dictionary with parameters suitable for a PySimpleGUI window.

**create_window_manager(script_name, global_var)**
- Initializes a window manager for a given script.
- **Parameters**:
  - `script_name` (str, default='default_script_name'): The name of the script.
  - `global_var` (dict, default=globals()): The global variables associated with the script.
- **Returns**: A tuple containing the `WindowManager`, bridge, and script name.

---


For detailed usage, parameter information, and return types, please refer to the individual method documentation.

## Bug Reports & Contact
For any bugs or issues, please report on the [Github page](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_gui). For direct queries, you can email the team at [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com).

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
