from abstract_gui.simple_gui.gui_template import sg,get_gui_fun
class WindowManager:
    def __init__(self, script_name, global_bridge):
        self.all_windows = {}
        self.last_window = None
        self.script_name = script_name
        self.global_bridge = global_bridge

        # Load global variables for this script from the global bridge
        self.global_vars = self.global_bridge.return_global_variables(self.script_name)

    def win_closed(self, event=''):
        obj_ls = ["Exit", sg.WIN_CLOSED]
        for each in obj_ls:
            bool_it = self.t_or_f_obj_eq(event=event, obj=each)
            if bool_it:
                return bool_it
        return bool_it

    def t_or_f_obj_eq(self, event=None, obj=None):
        return event == obj
    def verify_window(self, win: any = None) -> bool:
        """
        Verifies if the given object is a valid PySimpleGUI window.

        Args:
            win (any): The object to verify.

        Returns:
            bool: True if the object is a valid window, False otherwise.
        """
        verify = self.search_global_windows(window=win)
        if verify != False:
            return True
        return False
    def close_window(self, win: any = None):
        """
        Closes the given PySimpleGUI window.

        Args:
            win (any): The window to close.
        """
        if self.verify_window(win):
            win.close()
    def update_last_window(self, window):
        name = window
        if self.is_window_object(window):
            name = self.search_global_windows(window)
            if name is False:
                name = self.register_window(window)
        if name in self.get_window_names():
            self.all_windows['last_window'] = name

    def read_window(self, window):
        name = self.create_window_name()
        if self.is_window_object(window):
            name = self.search_global_windows(window)
            if name is False:
                name = self.register_window(window)
        if name not in self.get_window_names():
            return False
        window = self.global_vars[name]
        event, values = window.read()
        self.all_windows[name]["last_event"] = event
        self.all_windows[name]["values"] = values
        print(event)
        self.update_last_window(window)

    def get_event(self, win=None):
        if win is None:
            return self.all_windows[self.all_windows['last_window']]['last_event']
        name = self.search_global_windows(win)
        if name is not False:
            return self.all_windows[self.search_global_windows(win)]['last_event']

    def get_values(self, win=None):
        if win is None:
            return self.all_windows[self.all_windows['last_window']]['values']
        name = self.search_global_windows(win)
        if name is not False:
            return self.all_windows[name]['values']

    def while_basic(self, window=None):
        values = []
        self.global_vars = self.global_bridge.return_global_variables(self.script_name)
        while self.verify_window(window):
            self.read_window(window)
            if self.win_closed(self.get_event(window)):
                break
            event_function = self.all_windows[self.search_global_windows(window)]["event_function"]
            if event_function is not None:
                self.global_vars[event_function](self.get_event(window))

        self.close_window(window)
        # Update the global variables in the global bridge
        self.global_bridge.retrieve_global_variables(self.script_name,self.global_vars)

    def delete_from_list(self, _list, var):
        n_list = []
        for each in _list:
            if each != var:
                n_list.append(each)
        return n_list

    def get_all_windows(self):
        return self.all_windows

    def get_window_names(self):
        return self.delete_from_list(self.get_all_windows().keys(), 'last_window')

    def is_window_object(self, obj):
        if isinstance(obj, type(self.get_window())):
            return True

    def create_window_name(self):
        window_names = self.get_window_names()
        i = 0
        while 'win_' + str(i) in window_names:
            i += 1
        return 'win_' + str(i)

    def get_window(self, win_name='', layout=None, args=None):
        if args is None:
            args = {}
        if layout is None:
            layout = [[]]
        if "title" not in args:
            args["title"] = win_name
        if "layout" not in args:
            args["layout"] = layout
        return get_gui_fun('Window', {**args})

    def register_window(self, obj=None):
        if self.is_window_object(obj):
            name = self.search_global_windows(obj)
            if name is False:
                name = self.create_window_name()
                self.all_windows[name] = {"name": name, "last_event": '', "values": {}, "event_function": None}
                self.global_vars[name] = obj
            return name
        elif obj is None:
            name = self.create_window_name()
            self.all_windows[name] = {"name": name, "last_event": '', "values": {}, "event_function": None}
            self.global_vars[name] = None

        return name

    def search_global_windows(self, window):
        window_names = self.get_window_names()
        if self.is_window_object(window):
            for name in window_names:
                if self.global_vars[name] == window:
                    return name
        elif window in window_names:
            return self.global_vars[window]
        return False

    def unregister_window(self, window):
        win = self.search_global_windows(window)
        if win in self.get_window_names():
            del self.global_vars[win]
            del self.all_windows[win]
        elif self.is_window_object(win):
            del self.global_vars[window]
            del self.all_windows[window]

    def get_new_window(self, title="window", layout=None, args=None, event_function=None):
        if args is None:
            args = {}
        if layout is None:
            layout = [[]]
        if "title" not in args:
            args["title"] = title
        if "layout" not in args:
            args["layout"] = layout
        if "event_function" not in args:
            args["event_function"] = event_function
        name = self.register_window()
        self.global_vars[name] = self.get_window(args=args)
        self.all_windows[name]["event_function"] = args["event_function"]
        return self.global_vars[name]
