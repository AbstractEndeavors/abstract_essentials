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

### def 
```python
__init__(self, script_name, global_bridge)
```
**Purpose:**
"""
Initialize a WindowManager instance.
**Returns:**
* script_name (str): The name of the script that is using the WindowManager.
* global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.
---
### def 
```python
get_all_windows(self)
```
**Purpose:**
"""
Get all registered windows.
---
### def 
```python
get_window_names(self)
```
**Purpose:**
"""
Get the names of all registered windows.
---
### def 
```python
register_window(self, window=None)
```
**Purpose:**
"""
Register a window.
**Arguments:**
  * str: The name of the registered window.
**Returns:**
  * obj (any, optional): The window to register. If not provided, a new window is created.
---
### def 
```python
get_new_window(self, title:str=None, layout:list=None, args:dict=None, event_function:str=None,exit_events:(list or str)=None)
```
**Purpose:**
"""
Create a new window.
**Arguments:**
  * any: A new PySimpleGUI window.
**Returns:**
  * title (str, optional): The title of the window. If not provided, 'window' is used.
  * layout (list, optional): The layout of the window. If not provided, an empty layout is used.
  * args (dict, optional): Additional arguments for the window.
  * event_function (str, optional): The event function for the window.
---
### def 
```python
search_global_windows(self, window)
```
**Purpose:**
"""
Search for a window in the global variables.
**Arguments:**
  * any: The name of the window if found, False otherwise.
**Returns:**
  * window (any): The window to search for.
---
### def 
```python
verify_window(self, window=None) -> bool
```
**Purpose:**
"""
Verifies if the given object is a valid PySimpleGUI window.
**Arguments:**
  * bool: True if the object is a valid window, False otherwise.
**Returns:**
  * win (any): The object to verify.
---
### def 
```python
update_last_window(self, window)
```
**Purpose:**
"""
Update the last accessed window.
**Returns:**
* window (any): The window to set as the last accessed window.
---
### def 
```python
read_window(self, window)
```
**Purpose:**
"""
Read the event and values from a window and update the WindowManager's state.
**Returns:**
* window (any): The window to read from.
---
### def 
```python
get_last_window_info(self)
```
**Purpose:**
"""
Retrieve the details of the last accessed window.
---
### def 
```python
get_last_window_method(self)
```
**Purpose:**
"""
Get the method associated with the last accessed window.
---
### def 
```python
update_values(self, window=None, key:str=None, value:any=None, values:any=None, args:dict=None)
```
**Purpose:**
"""
Update the values associated with a given window.
**Returns:**
* window (any, optional): The window to update values for. Defaults to the last accessed window.
* key (str, optional): The key to be updated in the window.
* value (any, optional): The value to set for the given key.
* values (any, optional): Multiple values to set.
* args (dict, optional): Additional arguments to update the window with.
---
### def 
```python
get_event(self, window=None)
```
**Purpose:**
"""
Get the last event from a window.
**Arguments:**
  * any: The last event from the window.
**Returns:**
  * win (any, optional): The window to get the event from. If not provided, the last accessed window is used.
---
### def 
```python
get_values(self, window=None)
```
**Purpose:**
"""
Get the values from a window.
**Arguments:**
  * dict: The values from the window.
**Returns:**
  * win (any, optional): The window to get the values from. If not provided, the last accessed window is used.
---
### def 
```python
while_basic(self, window=None)
```
**Purpose:**
"""
Run an event loop for a window.
**Returns:**
* window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.
---
### def 
```python
get_window_name(self, obj=None)
```
**Purpose:**
"""
Get the names of all registered windows.
---
### def 
```python
win_closed(self, window)
```
**Purpose:**
"""
Check if a window event calls to close the window.
**Arguments:**
  * bool: True if the window is closed, False otherwise.
**Returns:**
  * event (str): The event to check.
---
### def 
```python
delete_from_list(self, _list, var)
```
**Purpose:**
"""
Remove a specific variable from a list.
**Arguments:**
  * list: A list with the specified variable removed.
**Returns:**
  * _list (list): The list to remove the variable from.
  * var (any): The variable to remove from the list.
---
### def 
```python
is_window_object(self, obj)
```
**Purpose:**
"""
Check if an object is a PySimpleGUI window object.
**Arguments:**
  * bool: True if the object is a window object, False otherwise.
**Returns:**
  * obj (any): The object to check.
---
### def 
```python
create_window_name(self)
```
**Purpose:**
"""
Create a unique name for a window.
---
### def 
```python
close_window_element(self)
```
**Purpose:**
"""
Get the constant representing a closed window event in PySimpleGUI.
---
### def 
```python
unregister_window(self, window)
```
**Purpose:**
"""
Unregister a window from the WindowManager.
**Returns:**
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

