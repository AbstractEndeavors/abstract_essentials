import PySimpleGUI as sg
from abstract_utilities.thread_utils import thread_alive
from abstract_utilities.class_utils import get_fun
from abstract_utilities.path_utils import get_current_path
class WindowGlobalBridge:
    """
    A class to manage the global variables shared between different scripts.

    Attributes:
        global_vars (dict): A dictionary to store global variables for each script.

    Methods:
        __init__(self):
            Initializes the WindowGlobalBridge with an empty dictionary for global_vars.

        retrieve_global_variables(self, script_name, global_variables, tag_script_name=False):
            Stores the global variables of a script in the global_vars dictionary.

        return_global_variables(self, script_name=None):
            Returns the global variables of a script.

        change_globals(self, variable, value, script_name=None):
            Modifies a global variable value for a specified script.

        search_globals_values(self, value, script_name=None):
            Searches for a specific value in the global variables of a script.

        return_global_value(self, variable, script_name=None):
            Returns the value of a specific global variable in a script.
    """
    def __init__(self):
        """
        Initializes the WindowGlobalBridge with an empty dictionary for global_vars.
        """
        self.global_vars = {}
    def create_script_name(self,script_name:str='default_script_name'):
        if script_name in self.global_vars:
            script_name = script_name+'_0'
        while script_name in self.global_vars:
            script_number = int(script_name.split('_')[-1])
            scrript_name = script_name[:-len(str(script_number))]+str(script_number+1)
        return script_name
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
                    return each
        return False

    def return_global_value(self, variable:str, script_name:str=None):
        """
        Returns the value of a specific global variable in a script.

        Args:
            variable (str): The name of the global variable to retrieve.
            script_name (str, optional): The name of the script. If None, the global variable in the base context will be retrieved.

        Returns:
            any: The value of the specified global variable.
        """
        if script_name is not None and variable in self.global_vars[script_name]:
            return self.global_vars[script_name][variable]


class WindowManager:
    """
    A class to manage PySimpleGUI windows and their events.

    Attributes:
        all_windows (dict): A dictionary to store registered windows along with their details.
        last_window (str): The name of the last accessed window.
        script_name (str): The name of the script that is using the WindowManager.
        global_bridge: The global bridge to access shared variables between different scripts.
        global_vars (dict): A dictionary to store global variables for this script.

    Methods:
        __init__(self, script_name, global_bridge):
            Initializes the WindowManager with the script name and global bridge.

        win_closed(self, event=''):
            Checks if the given event corresponds to a window close event.

        t_or_f_obj_eq(self, event=None, obj=None):
            Compares two objects and returns True if they are equal, False otherwise.

        verify_window(self, win: any = None) -> bool:
            Verifies if the given object is a valid PySimpleGUI window.

        close_window(self, win: any = None):
            Closes the given PySimpleGUI window.

        update_last_window(self, window):
            Updates the last accessed window to the given window.

        read_window(self, window):
            Reads the event and values from the given window and updates the WindowManager's state.

        get_event(self, window=None) -> Union[str, None]:
            Returns the last event of the specified window or the last accessed window.

        get_values(self, window=None) -> Union[Dict, None]:
            Returns the values of the specified window or the last accessed window.

        while_basic(self, window=None):
            Executes an event loop for the specified window or the last accessed window.

        delete_from_list(self, _list: List, var) -> List:
            Removes occurrences of a variable from a list and returns the new list.

        get_all_windows(self) -> Dict:
            Returns a dictionary containing all registered windows and their details.

        get_window_names(self) -> List[str]:
            Returns a list of names of all registered windows.

        is_window_object(self, obj) -> bool:
            Checks if the given object is a valid PySimpleGUI window object.

        create_window_name(self) -> str:
            Generates a unique name for a new window.

        get_window(self, win_name='', layout=None, args=None) -> sg.Window:
            Creates and returns a new PySimpleGUI window.

        register_window(self, obj=None) -> str:
            Registers a window object or creates a new window if no object is provided.

        search_global_windows(self, window) -> Union[str, bool]:
            Searches for a window in the global_vars dictionary and returns its name or False if not found.

        unregister_window(self, window):
            Unregisters a window and removes it from the global_vars and all_windows dictionaries.

        get_new_window(self, title="window", layout=None, args=None, event_function=None) -> sg.Window:
            Creates a new window with the given title, layout, and event function.
    """
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
    def get_all_windows(self):
        """
        Get all registered windows.

        Returns:
            dict: A dictionary containing all registered windows and their details.
        """
        return self.all_windows
    def get_window_names(self):
        """
        Get the names of all registered windows.

        Returns:
            list: A list of names of all registered windows.
        """
        return self.delete_from_list(list(self.get_all_windows().keys()), 'last_window')
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
    def verify_window(self, window=None) -> bool:
        """
        Verifies if the given object is a valid PySimpleGUI window.

        Args:
            win (any): The object to verify.

        Returns:
            bool: True if the object is a valid window, False otherwise.
        """
        return self.search_global_windows(window=window) != False
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
     def send_to_bridge(self):
        """
        Update the global bridge with the current state of the windows.
        """
        self.global_vars["all_windows"] = self.all_windows
        self.global_bridge.retrieve_global_variables(self.script_name, self.global_vars)    def close_window(self, window=None):
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
    def get_last_window_info(self):
        """
        Retrieve the details of the last accessed window.

        Returns:
            dict: Dictionary containing information about the last accessed window or None if there's no such window.
        """
        last_window = self.all_windows['last_window']
        if last_window != None:
            return self.all_windows[last_window]
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
        if self.close_window_element() not in exit_events:
            exit_events.append(self.close_window_element())
        return any(event == obj for obj in exit_events)
    def delete_from_list(self, _list, var):
        """
        Remove a specific variable from a list.

        Args:
            _list (list): The list to remove the variable from.
            var (any): The variable to remove from the list.

        Returns:
            list: A list with the specified variable removed.
        """
        return [each for each in _list if each != var]
    def is_window_object(self, obj):
        """
        Check if an object is a PySimpleGUI window object.

        Args:
            obj (any): The object to check.

        Returns:
            bool: True if the object is a window object, False otherwise.
        """
        return isinstance(obj, type(get_window()))
    def create_window_name(self):
        """
        Create a unique name for a window.

        Returns:
            str: A unique name for a window.
        """
        window_names = self.get_window_names()
        i = 0
        while 'win_' + str(i) in window_names:
            i += 1
        return 'win_' + str(i)
    def close_window_element(self):
        """
        Get the constant representing a closed window event in PySimpleGUI.

        Returns:
            any: The PySimpleGUI constant representing a window close event.
        """
        return sg.WIN_CLOSED
    def unregister_window(self, window):
        """
        Unregister a window from the WindowManager.

        Args:
            window (any): The window to unregister.
        """
        win = self.search_global_windows(window)
        if win in self.get_window_names():
            del self.all_windows[win]
        elif self.is_window_object(win):
            del self.all_windows[window]
"""
These functions are designed to simplify and streamline the process of creating and managing PySimpleGUI windows and their layouts. The utility functions allow for more concise code when setting up GUIs.
1. **ensure_nested_list(obj)**
   - This function checks if the passed `obj` is a list. If it's not, it wraps the `obj` in a list. If the `obj` is a list but contains at least one non-list element, it wraps the entire list in another list. 

2. **create_row(*args)**
   - Creates and returns a list out of the passed arguments.

3. **create_column(*args)**
   - Creates and returns a column (list of lists) from the passed arguments. If an argument is a list, it's expanded into individual rows.

4. **concatenate_rows(*args)**
   - Concatenates multiple lists into one.

5. **concatenate_layouts(*args)**
   - Essentially appends all arguments into one list.

6. **create_row_of_buttons(*args)**
   - Creates a row of button elements from the passed arguments.

7. **get_buttons(*args)**
   - This function is designed to return a list of button components. It accepts different argument types and interprets them differently to produce the required buttons.

8. **make_list_add(obj, values)**
   - Takes an object and values, converts both to lists (if they aren't already), and appends the values to the object.

9. **if_not_window_make_window(window)**
   - Ensures the given `window` is of the proper type, potentially creating a new window if not.

10. **while_quick(window, return_events, exit_events, event_return)**
    - A utility function to simplify the window event loop. Reads events from the given window until certain conditions are met.

11. **verify_args(args, layout, title, event_function, exit_events)**
    - Ensures default values for various window arguments.

12. **get_window(title, layout, args)**
    - Retrieves a PySimpleGUI window with specified or default properties.

13. **get_browser_layout(title, type, args, initial_folder)**
    - Prepares a layout for a file or folder browser window.

14. **get_yes_no_layout(title, text, args)**
    - Prepares a layout for a Yes/No window.

15. **get_input_layout(title, text, default, args)**
    - Prepares a layout for an input window.

16. **get_yes_no(title, text, args, exit_events, return_events, event_return)**
    - Displays a Yes/No window and returns the result.

17. **get_input(title, text, default, args, exit_events, return_events)**
    - Displays an input window and returns the result.

18. **get_browser(title, type, args, initial_folder, exit_events, return_events)**
    - Displays a browser window and returns the result.

19. **out_of_bounds(upper, lower, obj)**
    - Checks if the given value is out of specified bounds.

20. **det_bool_F(obj)**
    - Determines if the given object represents a `False` boolean.

21. **det_bool_T(obj)**
    - Determines if the given object represents a `True` boolean.

22. **T_or_F_obj_eq(event, obj)**
    - Compares two objects and returns True if they are equal, otherwise False.

23. **get_gui_fun(name, args)**
    - Retrieves a PySimpleGUI function by its name and prepares it with the given arguments.

24. **expandable(size, resizable, scrollable, auto_size_text, expand_x, expand_y)**
    - Returns a dictionary of parameters suitable for creating an expandable PySimpleGUI window.

25. **create_window_manager(script_name, global_var)**
    - Creates and returns a window manager for managing PySimpleGUI windows.

These functions are designed to simplify and streamline the process of creating and managing PySimpleGUI windows and their layouts. The utility functions allow for more concise code when setting up GUIs.
"""
def ensure_nested_list(obj):
    """
    Ensure that the input object is a nested list.

    Args:
        obj (any): The object to ensure as a nested list.

    Returns:
        list: A nested list containing the object or the original list if it's already nested.
    """
    # Check if the input object is a list
    if not isinstance(obj, list):
        # If it's not a list, create a new nested list containing the object
        return [obj]
    # If it is a list, check if any of its elements are non-list objects
    for element in obj:
        if not isinstance(element, list):
            # If at least one element is not a list, wrap the original list in a new list
            return [obj]
    # If all elements are lists, return the original list
    return obj
def create_row(*args):
    """
    Create a row layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the row layout.

    Returns:
        list: A row layout containing the provided elements.
    """
    return [arg for arg in args]
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
def concatenate_layouts(*args):
    """
    Concatenate multiple layouts into a single layout.

    Args:
        *args: Layouts to be concatenated.

    Returns:
        list: A layout containing concatenated elements from input layouts.
    """
    layout = []
    for arg in args:
        layout.append(arg)
    return layout
def create_row_of_buttons(*args):
    """
    Create a row layout containing buttons generated from the provided arguments.

    Args:
        *args: Arguments for creating buttons.

    Returns:
        list: A row layout containing buttons created from the provided arguments.
    """
    return [button for arg in args for button in get_buttons(arg)]
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
def make_list_add(obj,values):
    """
    Add multiple values to a list and return the resulting list.

    Args:
        obj (list): The original list.
        values (iterable): Values to be added to the list.

    Returns:
        list: The modified list containing the original elements and the added values.
    """
    obj = list(obj)
    for each in list(values):
        obj.append(each)
    return obj
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
        args = verify_args(args=args, layout=ensure_nested_list(layout), title=title)
        return get_gui_fun('Window', {**args})
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
def out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1):
    """
    Checks if the given object is out of the specified upper and lower bounds.

    Args:
        upper (int or float): The upper bound.
        lower (int or float): The lower bound.
        obj (int or float): The object to check.

        bool: True if the object is out of bounds, False otherwise.
    """
    return det_bool_T(obj > 100 or obj < 0)
def det_bool_F(obj: (tuple or list or bool) = False):
    """
    Determines if the given object is a boolean False value.

    Args:
        obj (tuple or list or bool): The object to determine the boolean False value.

    Returns:
        bool: True if the object is a boolean False value, False otherwise.
    """
    if isinstance(obj, bool):
        return obj
    return all(obj)
def det_bool_T(obj: (tuple or list or bool) = False):
    """
    Determines if the given object is a boolean True value.

    Args:
        obj (tuple or list or bool): The object to determine the boolean True value.

    Returns:
        bool: True if the object is a boolean True value, False otherwise.
    """
    if isinstance(obj, bool):
        return obj 
    return any(obj)
def T_or_F_obj_eq(event: any = '', obj: any = ''):
    """
    Compares two objects and returns True if they are equal, False otherwise.

    Args:
        event (any): The first object to compare.
        obj (any): The second object to compare.

    Returns:
        bool: True if the objects are equal, False otherwise.
    """
    return True if event == obj else False
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
def expandable(size: tuple = (None, None),resizable:bool=True,scrollable:bool=True,auto_size_text:bool=True,expand_x:bool=True,expand_y:bool=True):
    """Returns a dictionary with window parameters for creating an expandable PySimpleGUI window."""
    return {"size": size, "resizable": resizable, "scrollable": scrollable, "auto_size_text": auto_size_text, "expand_x": expand_x, "expand_y": expand_y}
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
    bridge.retrieve_global_variables(script_name, global_var)
    return WindowManager(script_name, bridge),bridge,script_name
