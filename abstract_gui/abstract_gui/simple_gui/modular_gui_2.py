from function_registry import FunctionRegistry
import threading
import PySimpleGUI as sg
import inspect
import os

registrygui = FunctionRegistry()
@event_trigger('get', 'update', st='-RESPONSE-', obj={'value': 'heyayayaya'})
def my_function():
    # Function logic goes here
    pass

# Register the function in the function registry
registrygui.register_function('my_function', my_function)
# Example usage: retrieve the function and its event trigger information
function_info = registrygui.get_function('my_function')
event_type = function_info.event_type  # 'get'
event_obj = function_info.event_obj  # 'update'
event_args = function_info.event_args  # {'st': '-RESPONSE-', 'obj': {'value': 'heyayayaya'}}
class UpdateHandler:
    def __init__(self, window):
        self.window = window

    def update_progress(self, st, progress):
        self.window[st].update_bar(progress)

    def update_element(self, st, obj):
        self.window.Element(st).Update(**obj)

    def update_button_visibility(self, button_name, visible):
        self.window[button_name].update(visible=visible)

    def update_table(self, table_name, data):
        self.window.FindElement(table_name).Update(values=data, num_rows=len(data))

    def close_window(self, window):
        window.Close()

    def handle_update(self, update):
        update_type = update.get('type')
        if update_type:
            func_name = f'update_{update_type}'
            if hasattr(self, func_name):
                func = getattr(self, func_name)
                args = update.get('args', {})
                func(**args)

def expandable(size=(None, None)):
    return {"size": size, "resizable": True, "scrollable": True, "auto_size_text": True, "expand_x": True, "expand_y": True}

def match_window_with_number(window):
    for name, obj in globals().items():
        if name.startswith('win_') and id(obj) == id(window):
            return name
    return None

def get_gui_fun(name='', args={}):
    import PySimpleGUI as sg
    win = False
    if name == 'Window':
        win = True
    obj = get_fun({"instance": sg, "name": name, "args": args})
    if win:
        win_track['num'] += 1
        globals()[f'win_{win_track["num"]}'] = obj
    return obj

def win_closed(event=''):
    return T_or_F_obj_eq(event=event, obj=sg.WIN_CLOSED)

def T_or_F_obj_eq(event=None, obj=None):
    return True if event == obj else False

def det_bool_T(obj=False):
    if isinstance(obj, bool):
        return obj 
    return any(obj)

def det_bool_F(obj=False):
    if isinstance(obj, bool):
        return obj
    return all(obj)

def out_of_bounds(upper=100, lower=0, obj=-1):
    return det_bool_T(obj > 100 or obj < 0)

def create_win_name():
    all_windows = get_glob('all_windows')
    keys = list(all_windows.keys())
    i, curr_try = 'default_window', 0
    while curr_try in keys:
        curr_try = f'default_window_{i}'
        i += 1
    return curr_try

def update_read(curr_win=None, win_name=''):
    all_windows = get_glob('all_windows')
    event, values = curr_win.read()
    # Matching the window with its number
    window_number = match_window_with_number(curr_win)
    globals()['win_last'] = curr_win
    if win_name not in all_windows:
        all_windows[win_name] = {'event': '', 'values': {}}
        change_glob(win_name, curr_win)
    all_windows[win_name]['event'] = event
    all_windows[win_name]['values'] = values
    all_windows['last_window']['name'] = win_name
    all_windows['last_window']['event'] = event
    all_windows['last_window']['values'] = values
    change_glob('all_windows', all_windows)

def get_js_st(js, st):
    if st in js:
        return js[st]

def while_basic_events(event_win=None, win_name='', events={}):
    while verify_window(event_win):
        update_read(curr_win=event_win, win_name='event_win')
        if win_closed(get_event(event_win)):
            break
        keys = list(events.keys())
        for k in range(len(keys)):
            key = keys[k]
            if T_or_F_obj_eq(event=get_event(curr_win=win_name), obj=key):
                func_specs = events[key]
                args = process_args(func_specs['args'])
                call_functions(args=args, instance=get_js_st(func_specs, 'instance'), function_name=get_js_st(func_specs, 'name'), glob=globals())
    close_window(event_win)

def while_basic(win=None):
    if win is None:
        win = get_glob(obj='window')
    while verify_window(win):
        event, values = win.read()
        if win_closed(event):
            break
    close_window(win)

def get_last_window():
    return win_last

def while_progress(win=None, progress=0, step=5, thread=None):
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

def update(curr_win=None, st=None, obj={"value": ''}):
    if st is not None:
        curr_win[st].update(**obj)

def get_value(curr_win='last_window', st=''):
    all_windows = get_glob('all_windows')
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[curr_win]
    if st in curr_js['values']:
        return curr_js['values'][st]

def get_event(curr_win='last_window', st=''):
    all_windows = get_glob('all_windows')
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[win_name]
    return curr_js['event']

def get_thread(target=None, args=(), daemon=True):
    return threading.Thread(target=target, args=args, daemon=daemon)

def start_thread(thread=None):
    if verify_thread(thread):
        thread.start()

def verify_thread(thread=None):
    return T_or_F_obj_eq(type(thread), type(threading.Thread()))

def thread_alive(thread):
    if verify_thread(thread):
        return thread.is_alive()
    return False

def get_progress_bar(max_value=100, size=(30, 10), key='bar'):
    return get_gui_fun('ProgressBar', {"max_value": max_value, "size": size, "key": key})

def update_progress(win='progress_window', st='bar', progress=0):
    win[st].update_bar(progress)

def get_window(title='basic window', layout=[[]]):
    return sg.Window(title, layout)

def verify_window(win=None):
    if type(win) == str:
        win = get_glob(obj=win)
    if type(win) == type(get_window()):
        return True
    return False

def close_window(win=None):
    if verify_window(win):
        win.close()

globals()['win_track'] = {'num': 0}
change_glob(var='all_windows', val={'last_window': {'name': '', 'values': {}, 'event': ''}}, glob=globals())
registrygui = FunctionRegistry()
# Usage example
window = get_window()

# Create the UpdateHandler instance
update_handler = UpdateHandler(window)

# Example update
update_info = {
    'type': 'progress',
    'args': {
        'st': 'progress_bar',
        'progress': 50
    }
}

# Handle the update
update_handler.handle_update(update_info)
