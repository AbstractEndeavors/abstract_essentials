# Abstract Essentials

## Description

### Use
* Explanation of how to use the package.

## Module

### Description
* Brief description of the module.

### Features
* Feature 1
* Feature 2
* ... 

### Dependencies

#### Dependency Name 1

##### Module Component


###### Functions

### __init__
```python
__init__(self, script_name, global_bridge)
```

**Purpose:**
Initialize a WindowManager instance.

**Arguments:**
  * script_name (str): The name of the script that is using the WindowManager.
  * global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.
---
### get_all_windows
```python
get_all_windows(self)
```

**Purpose:**
Get all registered windows.
---
### get_window_names
```python
get_window_names(self)
```

**Purpose:**
Get the names of all registered windows.
---
### register_window
```python
register_window(self, window=None)
```

**Purpose:**
Register a window.

**Arguments:**
  * obj (any, optional): The window to register. If not provided, a new window is created.
**Returns:**
  * str: The name of the registered window.
---
### get_new_window
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
---
### search_global_windows
```python
search_global_windows(self, window)
```

**Purpose:**
Search for a window in the global variables.

**Arguments:**
  * window (any): The window to search for.
**Returns:**
  * any: The name of the window if found, False otherwise.
---
### verify_window
```python
verify_window(self, window=None) -> bool
```

**Purpose:**
Verifies if the given object is a valid PySimpleGUI window.

**Arguments:**
  * win (any): The object to verify.
**Returns:**
  * bool: True if the object is a valid window, False otherwise.
---
### update_last_window
```python
update_last_window(self, window)
```

**Purpose:**
Update the last accessed window.

**Arguments:**
  * window (any): The window to set as the last accessed window.
---
### read_window
```python
read_window(self, window)
```

**Purpose:**
Read the event and values from a window and update the WindowManager's state.

**Arguments:**
  * window (any): The window to read from.
---
### get_last_window_info
```python
get_last_window_info(self)
```

**Purpose:**
Retrieve the details of the last accessed window.
---
### get_last_window_method
```python
get_last_window_method(self)
```

**Purpose:**
Get the method associated with the last accessed window.
---
### update_values
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
---
### get_event
```python
get_event(self, window=None)
```

**Purpose:**
Get the last event from a window.

**Arguments:**
  * win (any, optional): The window to get the event from. If not provided, the last accessed window is used.
**Returns:**
  * any: The last event from the window.
---
### get_values
```python
get_values(self, window=None)
```

**Purpose:**
Get the values from a window.

**Arguments:**
  * win (any, optional): The window to get the values from. If not provided, the last accessed window is used.
**Returns:**
  * dict: The values from the window.
---
### while_basic
```python
while_basic(self, window=None)
```

**Purpose:**
Run an event loop for a window.

**Arguments:**
  * window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.
---
### get_window_name
```python
get_window_name(self, obj=None)
```

**Purpose:**
Get the names of all registered windows.
---
### win_closed
```python
win_closed(self, window)
```

**Purpose:**
Check if a window event calls to close the window.

**Arguments:**
  * event (str): The event to check.
**Returns:**
  * bool: True if the window is closed, False otherwise.
---
### delete_from_list
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
---
### is_window_object
```python
is_window_object(self, obj)
```

**Purpose:**
Check if an object is a PySimpleGUI window object.

**Arguments:**
  * obj (any): The object to check.
**Returns:**
  * bool: True if the object is a window object, False otherwise.
---
### create_window_name
```python
create_window_name(self)
```

**Purpose:**
Create a unique name for a window.
---
### close_window_element
```python
close_window_element(self)
```

**Purpose:**
Get the constant representing a closed window event in PySimpleGUI.
---
### unregister_window
```python
unregister_window(self, window)
```

**Purpose:**
Unregister a window from the WindowManager.

**Arguments:**
  * window (any): The window to unregister.
---




###### Usage

* **Use:** Explanation of how to use the function/class.

###### Module Information

* **Info:** Additional information or context about the module component.

### Usage

#### Use
* Explanation of how to use the module.

### Module Information

#### Info
* Additional information or context about the module.

