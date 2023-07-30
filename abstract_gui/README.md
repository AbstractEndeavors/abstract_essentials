# abstract_gui

This is a Python module for creating abstract GUI windows and interacting with them. It uses the PySimpleGUI library and provides additional utilities for simplifying the creation and handling of PySimpleGUI windows.

This module can be found in the `abstract_essentials` project at `github.io/abstract_endeavors/abstract_essentials/abstract_gui/`.

## Installation

You can install the `abstract_gui` module via pip:

```sh
pip install abstract_gui
```

You can also install it directly from the source:

```sh
git clone https://github.io/abstract_endeavors/abstract_essentials/abstract_gui/
cd abstract_gui
python setup.py install# abstract_gui

This is a Python module for creating abstract GUI windows and interacting with them. It uses the PySimpleGUI library and provides additional utilities for simplifying the creation and handling of PySimpleGUI windows.

This module can be found in the `abstract_essentials` project at `github.io/abstract_endeavors/abstract_essentials/abstract_gui/`.

## Installation

You can install the `abstract_gui` module via pip:

```sh
pip install abstract_gui
```

You can also install it directly from the source:

```sh
git clone https://github.io/abstract_endeavors/abstract_essentials/abstract_gui/
cd abstract_gui
python setup.py install
```

## Usage

Here's an example of how to use the `abstract_gui` module:

```python
from abstract_gui import get_window, while_basic

window = get_window(title="Hello World!", layout=[[sg.Text("Hello, world!")]])
while_basic(window)
```

This will create a simple window with a single "Hello, world!" text element, and handle its events until it's closed.

##Components

# Window Manager - [WindowManager Utility](#abstract_gui---windowmanager-utility)


## Documentation

The `abstract_gui` module provides the following classes and functions:

### `expandable(size: tuple = (None, None))`

Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.

### `get_glob(obj: str = '', glob=globals())`

Retrieves a global object by name from the global namespace.

### `get_window(title: str = 'basic window', layout: list = [[]])`

Returns a callable object for creating a PySimpleGUI window with the specified title and layout.

### `verify_window(win: any = None) -> bool`

Verifies if the given object is a valid PySimpleGUI window.

### `close_window(win: any = None)`

Closes the given PySimpleGUI window.

### `get_gui_fun(name: str = '', args: dict = {})`

Returns a callable object for a specific PySimpleGUI function with the provided arguments.

### `win_closed(event: str = '')`

Checks if the event corresponds to a closed window.

### `T_or_F_obj_eq(event: any = '', obj: any = '')`

Compares two objects and returns True if they are equal, False otherwise.

### `det_bool_T(obj: (tuple or list or bool) = False)`

Determines if the given object is a boolean True value.

### `det_bool_F(obj: (tuple or list or bool) = False)`

Determines if the given object is a boolean False value.

### `out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1)`

Checks if the given object is out of the specified upper and lower bounds.

... and many more!

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

```

## Usage

Here's an example of how to use the `abstract_gui` module:

```python
from abstract_gui import get_window, while_basic

window = get_window(title="Hello World!", layout=[[sg.Text("Hello, world!")]])
while_basic(window)
```

This will create a simple window with a single "Hello, world!" text element, and handle its events until it's closed.

# abstract_gui - `WindowManager` Utility

## Overview

The `WindowManager` utility is part of the `abstract_gui` module, specifically in the `simple_gui` package. It provides a class to manage PySimpleGUI windows and their events in a convenient manner. The utility is designed to work in combination with the `WindowGlobalBridge` class, which manages global variables shared between different scripts.

## Installation

Ensure that you have the `abstract_gui` module installed. You can install it using pip:

```bash
pip install abstract_gui
```

## Usage

To use the `WindowManager` utility, follow these steps:

1. Import the necessary classes:

```python
from abstract_gui.simple_gui import window_manager, global_bridge
```

2. Initialize the global bridge and create an instance of the `WindowManager` class:

```python
# Initialize the global bridge
bridge = global_bridge.WindowGlobalBridge()

# Store the global variables in the bridge (Replace globals() with your actual global variables)
script_name = "main_script"
bridge.retrieve_global_variables(script_name, globals())

# Create an instance of the WindowManager class
window_manager = window_manager.WindowManager(script_name, bridge)
```

3. Define your GUI layout and event functions:

```python
def main_window_layout():
    return [
        [sg.Text("Enter the amount of CBD (mg):"), sg.Input(key="-CBD-", enable_events=True)],
        [sg.Text("Enter the amount of THC (mg):"), sg.Input(key="-THC-", enable_events=True)],
        [sg.Button("Calculate"), sg.Button("Exit")]
    ]

def percent_functions(event):
    if event == "Calculate":
        try:
            cbd_mg = float(window_manager.get_values()["-CBD-"])
            thc_mg = float(window_manager.get_values()["-THC-"])
            calculate_and_show_result(cbd_mg, thc_mg)
        except ValueError:
            sg.popup_error("Please enter valid numbers for CBD and THC.")
```

4. Define your windows and event loops:

```python
def main_window():
    return window_manager.get_new_window(
        title="CBD and THC Percentage Calculator",
        layout=main_window_layout(),
        event_function="percent_functions"
    )

def calculate_and_show_result(cbd_mg, thc_mg):
    tincture_volume_ml = 30  # Assuming the volume is 30 ml for the tincture
    cbd_weight_percentage, thc_weight_percentage = calculate_cbd_thc_weight_percentage(cbd_mg, thc_mg, tincture_volume_ml)
    result_window = show_result_window(cbd_weight_percentage, thc_weight_percentage)
    window_manager.while_basic(result_window)
```

5. Run the main event loop:

```python
if __name__ == "__main__":
    main_win = main_window()
    window_manager.while_basic(window=main_win)
```

## Conclusion

The `WindowManager` utility in the `abstract_gui` module provides a user-friendly approach to manage PySimpleGUI windows and events. By using the `WindowGlobalBridge` class, it facilitates the sharing of global variables between different scripts. Feel free to customize and extend the provided code to suit your specific GUI application requirements. Happy coding!


## Documentation

The `abstract_gui` module provides the following classes and functions:

### `expandable(size: tuple = (None, None))`

Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.

### `get_glob(obj: str = '', glob=globals())`

Retrieves a global object by name from the global namespace.

### `get_window(title: str = 'basic window', layout: list = [[]])`

Returns a callable object for creating a PySimpleGUI window with the specified title and layout.

### `verify_window(win: any = None) -> bool`

Verifies if the given object is a valid PySimpleGUI window.

### `close_window(win: any = None)`

Closes the given PySimpleGUI window.

### `get_gui_fun(name: str = '', args: dict = {})`

Returns a callable object for a specific PySimpleGUI function with the provided arguments.

### `win_closed(event: str = '')`

Checks if the event corresponds to a closed window.

### `T_or_F_obj_eq(event: any = '', obj: any = '')`

Compares two objects and returns True if they are equal, False otherwise.

### `det_bool_T(obj: (tuple or list or bool) = False)`

Determines if the given object is a boolean True value.

### `det_bool_F(obj: (tuple or list or bool) = False)`

Determines if the given object is a boolean False value.

### `out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1)`

Checks if the given object is out of the specified upper and lower bounds.

... and many more!

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
