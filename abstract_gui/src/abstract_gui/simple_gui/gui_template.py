from abstract_utilities.json_utils import get_keys
from abstract_utilities.thread_utils import thread_alive
from abstract_utilities.class_utils import call_functions, process_args, get_fun
from abstract_utilities.type_utils import is_number
from .__init__ import *
globals()['registry_name'] = 'simple_gui_windows_manager'
global_registry(name=registry_name,glob=globals())
def expandable(size: tuple = (None, None)):
    """Returns a dictionary with window parameters for creating an expandable PySimpleGUI window."""
    return {"size": size, "resizable": True, "scrollable": True, "auto_size_text": True, "expand_x": True, "expand_y": True}
update_registry(var='all_windows', val={'last_window': {'name': '', 'values': {}, 'event': ''}},name=registry_name)
def get_all_windows():
    glob = get_global_from_registry(registry_name)
    return glob['all_windows']
def get_window_from_global(obj:str):
    glob = get_global_from_registry(registry_name)
    if obj in glob:
        return glob[obj]
def update_window_to_registry(win,win_name:str ='default_window'):
    windows =get_all_windows()
    if win_name in windows:
        win_name = create_win_name(win_name=win_name)
    windows[win_name]={'name': win_name, 'values': {}, 'event': ''}
    update_registry(var='all_windows',val=windows,name=registry_name)
def get_window(title: str = 'basic window', layout: list = [[]]):
    """
    Returns a callable object for creating a PySimpleGUI window with the specified title and layout.

    Args:
        title (str): The title of the window.
        layout (list): The layout of the window.

    Returns:
        callable: A callable object that creates the PySimpleGUI window when called.
    """
    return get_gui_fun(name='Window', args={"title": title, "layout": layout})

def verify_window(win: any = None) -> bool:
    """
    Verifies if the given object is a valid PySimpleGUI window.

    Args:
        win (any): The object to verify.

    Returns:
        bool: True if the object is a valid window, False otherwise.
    """
    if type(win) == str:
        win = get_window_from_global(obj=win)
    if type(win) == type(get_window()):
        return True
    return False

def close_window(win: any = None):
    """
    Closes the given PySimpleGUI window.

    Args:
        win (any): The window to close.
    """
    if verify_window(win):
        win.close()

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

def win_closed(event: str = ''):
    """
    Checks if the event corresponds to a closed window.

    Args:
        event (str): The event to check.

    Returns:
        bool: True if the event corresponds to a closed window, False otherwise.
    """
    return T_or_F_obj_eq(event=event, obj=sg.WIN_CLOSED)

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

def create_win_name(win_name:str='default_window'):
    """
    Generates a unique window name based on the existing window names.

    Returns:
        str: The generated unique window name.
    """
    all_windows = get_all_windows()
    keys = get_keys(all_windows)
    curr_try,i = win_name, 0
    if '_' in win_name:
        num = win_name.split('_')[-1]
        if is_number(num):
          i=int(num)
          win_name= win_name[:-len(in_name.split('_')[-1]+1)]
    while curr_try in keys:
        curr_try = f'{win_name}_{i}'
        i += 1
    return curr_try

def update_read(curr_win: type(get_window()), win_name: str = create_win_name()):
    """
    Updates the current window's event and values based on the latest user input.

    Args:
        curr_win (type(get_window())): The current window to update.
        win_name (str): The name of the current window.
    """
    all_windows = get_all_windows()
    event, values = curr_win.read()
    if win_name not in all_windows:
        all_windows[win_name] = {'event': '', 'values': {}}
        change_glob(var=win_name, val=curr_win)
        update_registry(var=win_name, val=curr_win,name=registry_name)
    all_windows[win_name]['event'] = event
    all_windows[win_name]['values'] = values
    all_windows['last_window']['name'] = win_name
    all_windows['last_window']['event'] = event
    all_windows['last_window']['values'] = values
    update_registry(var='all_windows', val=all_windows,name=registry_name)

def get_js_st(js: dict, st: str):
    """
    Retrieves a value from a dictionary based on the specified key.

    Args:
        js (dict): The dictionary to retrieve the value from.
        st (str): The key to retrieve the value for.

    Returns:
        any: The retrieved value or None if the key doesn't exist.
    """
    if st in js:
        return js[st]

def while_basic_events(event_win: type(get_window()) = get_window(), win_name: str = create_win_name(), events: dict = {}):
    """
    Executes a while loop for handling basic events in a PySimpleGUI window.

    Args:
        event_win (type(get_window())): The window to handle events for.
        win_name (str): The name of the window.
        events (dict): The dictionary of events and their corresponding function specifications.
    """
    while verify_window(event_win):
        update_read(curr_win=event_win, win_name='event_win')
        if win_closed(get_event(event_win)):
            break
        keys = get_keys(events)
        for k in range(0, len(keys)):
            key = keys[k]
            if T_or_F_obj_eq(event=get_event(curr_win=win_name), obj=key):
                func_specs = events[key]
                if fun_specs:
                    args = process_args(func_specs['args'])
                call_functions(args=args, instance=get_js_st(func_specs, 'instance'), function_name=get_js_st(func_specs, 'name'), glob=globals())
    close_window(event_win)

def while_basic(win=None):
    """
    Executes a while loop for handling basic events in a PySimpleGUI window.

    Args:
        win: The window to handle events for. If not provided, it uses the 'window' global object.
    """
    values_all=[]
    if win is None:
        win = get_globes(string='window')
    while verify_window(win):
        event, values = win.read()
        if values != None:
            values_all = values
        if win_closed(event):
            return values_all
            break
    close_window(win)
    return values_all

def single_call(win):
    """
    Reads and closes a PySimpleGUI window, returning the captured values.

    Args:
        win: The window to read.

    Returns:
        dict: The captured values from the window.
    """
    event, values = win.read()
    win.close()
    return values

def get_last_window():
    """
    Returns the name of the last opened window.

    Returns:
        str: The name of the last opened window.
    """
    return get_window_from_global('all_windows')['last_window']['name']

def while_progress(win=None, progress: int = 0, step: int = 5, thread=None):
    """
    Executes a while loop with a progress bar in a PySimpleGUI window.

    Args:
        win: The window to display the progress bar. If not provided, it uses the last opened window.
        progress (int): The initial progress value.
        step (int): The step size for incrementing/decrementing the progress value.
        thread: The thread object to check for termination.
    """
    if win is None:
        win = get_last_window()
    while verify_window(win):
        event, values = win.read(timeout=100)
        if win_closed(event) or not thread_alive(thread):
            break
        win.read(timeout=100)
        update_progress(win=win, st='bar', progress=progress)
        progress += step
        if out_of_bounds(upper=100, lower=0, obj=progress):
            step *= -1
    close_window(win)

def update(curr_win: (str or type(get_window())) = 'last_window', st: str = '', obj: any = ''):
    """
    Updates the value of a specific element in the current window.

    Args:
        curr_win (str or type(get_window())): The current window to update. If not provided, it uses the last opened window.
        st (str): The element to update.
        obj (any): The value to assign to the element.
    """
    all_windows = get_all_windows()
    all_windows['last_window'][st].update(values=obj)
    if type(obj) is list:
        all_windows['last_window'][st].update(value=obj[0])
    update_registry(var='all_windows', val=all_windows,name=registry_name)

def get_value(curr_win: (str or type(get_window())) = 'last_window', st: str = ''):
    """
    Retrieves the value of a specific element in the current window.

    Args:
        curr_win (str or type(get_window())): The current window to retrieve the value from. If not provided, it uses the last opened window.
        st (str): The element to retrieve the value for.

    Returns:
        any: The retrieved value of the element.
    """
    all_windows = get_all_windows()
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[curr_win]
    if st in curr_js['values']:
        return curr_js['values'][st]

def get_event(curr_win: (str or type(get_window())) = 'last_window', st: str = ''):
    """
    Retrieves the event of the current window or the specified window.

    Args:
        curr_win (str or type(get_window())): The current window to retrieve the event from. If not provided, it uses the last opened window.
        st (str): Unused parameter for consistency with other functions.

    Returns:
        any: The retrieved event of the window.
    """
    all_windows = get_all_windows()
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[win_name]
    return curr_js['event']

