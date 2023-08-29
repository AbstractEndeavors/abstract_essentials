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

* **create_row(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Elements to be placed in the row layout.
      * **Returns:**
        * `list`: A row layout containing the provided elements.
        * **create_column(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Elements to be placed in the column layout.
      * **Returns:**
        * `list`: A column layout containing the provided elements.
        * **concatenate_rows(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Row layouts to be concatenated.
      * **Returns:**
        * `list`: A row layout containing concatenated elements from input row layouts.
        * **concatenate_layouts(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Layouts to be concatenated.
      * **Returns:**
        * `list`: A layout containing concatenated elements from input layouts.
        * **create_row_of_buttons(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Arguments for creating buttons.
      * **Returns:**
        * `list`: A row layout containing buttons created from the provided arguments.
        * **get_buttons(*args)**
      * **Purpose:** ...
      * **Arguments:** 
        * `*args`: Arguments specifying button elements.
      * **Returns:**
        * `list`: Button elements generated from the provided arguments.
        * **if_not_window_make_window(window)**
      * **Purpose:** ...
      * **Arguments:** 
        * `window`: The object to be checked. If not a window, it's expected to be a dictionary with layout information.
      * **Returns:**
        * `window`: The valid window object.
        * **while_quick(window,return_events:(list or str)=[],exit_events:(list or str)=[sg.WIN_CLOSED],event_return=False)**
      * **Purpose:** ...
      * **Arguments:** 
        * `window`: The window to read events from.
        * `return_events (list or str)`: Events that would lead to the window being closed and a value returned.
        * `exit_events (list or str)`: Events that would lead to the window being closed without returning a value.
        * `event_return (bool)`: If True, returns the event. If False, returns the values.
      * **Returns:**
        * `event or values`: Depending on the event_return flag.
        * **verify_args(args:dict=None, layout:list=None, title:str=None, event_function:str=None,exit_events:(list or str)=None)**
      * **Purpose:** ...
      * **Arguments:** 
        * `args (dict, optional)`: Dictionary containing window arguments.
        * `layout (list, optional)`: The layout for the window.
        * `title (str, optional)`: The title of the window.
        * `event_function (str, optional)`: The function to be executed when an event occurs.
        * `exit_events (list or str, optional)`: List of events that would close the window.
      * **Returns:**
        * `dict`: The verified/updated window arguments.
        * **get_window(title=None, layout=None, args=None)**
      * **Purpose:** ...
      * **Arguments:** 
        * `win_name (str, optional)`: The name of the window. If not provided, a unique name is generated.
        * `layout (list, optional)`: The layout of the window. If not provided, an empty layout is used.
        * `args (dict, optional)`: Additional arguments for the window.
      * **Returns:**
        * `any`: A PySimpleGUI window.
  * **get_browser_layout(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path())**
      * **Purpose:** ...
      * **Arguments:** 
      * **Returns:**
        * **get_yes_no_layout(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={})**
      * **Purpose:** ...
      * **Arguments:** 
        * `title (str, optional)`: The title of the window.
        * `text (str, optional)`: The prompt text.
        * `args (dict, optional)`: Additional arguments for the window.
      * **Returns:**
        * `dict`: The layout dictionary.
        * **get_input_layout(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={})**
      * **Purpose:** ...
      * **Arguments:** 
        
      * **Returns:**
        
        * **get_yes_no(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={},exit_events:(str or list)=[],return_events:(str or list)=["Yes","No"],event_return=True)**
      * **Purpose:** ...
      * **Arguments:** 
        * `title (str, optional)`: The title of the window.
        * `text (str, optional)`: The prompt text.
        * `args (dict, optional)`: Additional arguments for the window.
        * `exit_events (str or list, optional)`: List of events that would close the window.
        * `return_events (str or list, optional)`: List of events that would lead to a response being returned.
        * `event_return (bool, optional)`: If True, returns the event. If False, returns the values.
      * **Returns:**
        * `event or values`: Depending on the event_return flag.
        * **get_input(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={},exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK'])**
      * **Purpose:** ...
      * **Arguments:** 
        * `title (str, optional)`: The title of the window.
        * `text (str, optional)`: The prompt text.
        * `default (str, optional)`: The default input value.
        * `args (dict, optional)`: Additional arguments for the window.
        * `exit_events (str or list, optional)`: List of events that would close the window.
        * `return_events (str or list, optional)`: List of events that would lead to an input being returned.
      * **Returns:**
        * `values`: The captured user input.
        * **get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path(),exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK'])**
      * **Purpose:** ...
      * **Arguments:** 
        * `title (str, optional)`: The title of the window.
        * `type (str, optional)`: The type of browser (e.g., 'Folder').
        * `args (dict, optional)`: Additional arguments for the window.
        * `initial_folder (str, optional)`: The folder to start browsing from.
        * `exit_events (str or list, optional)`: List of events that would close the window.
        * `return_events (str or list, optional)`: List of events that would lead to a path being returned.
      * **Returns:**
        * `results`: The selected path or default path if none is selected.
        * **get_gui_fun(name: str = '', args: dict = {})**
      * **Purpose:** ...
      * **Arguments:** 
        * `name (str)`: The name of the PySimpleGUI function.
        * `args (dict)`: The arguments to pass to the PySimpleGUI function.
      * **Returns:**
        * `callable`: A callable object that invokes the PySimpleGUI function with the specified arguments when called.
        * **create_window_manager(script_name='default_script_name',global_var=globals())**
      * **Purpose:** ...
      * **Arguments:** 
        * `script_name (str, optional)`: The name of the script.
        * `global_var (dict, optional)`: The global variables associated with the script.
      * **Returns:**
        * `tuple`: A tuple containing the WindowManager, bridge, and script name.
     
###### Classes

* **Class Name 1**
  * **Attributes**
    * `attribute_name1`: Description of the attribute.
    * ...
  * **Methods**
    * **Method Name 1**
      * **Purpose:** Description of method's purpose.
      * **Arguments:** 
        * `arg1`: Description of argument 1.
        * ...
      * **Returns:** Description of what the method returns.

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

