---

# Abstract Essentials Python Package

Abstract Essentials is a comprehensive suite of modules designed to streamline various tasks, from managing environment variables to web utilities.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Modules](#modules)
  - [Abstract Security](#abstract-security)
  - [Abstract Audio](#abstract-audio)
  - [Abstract Modules](#abstract-modules)
  - [Abstract AI](#abstract-ai)
  - [Abstract Gui](#abstract-gui)
  - [Abstract Images](#abstract-images)
  - [Abstract Utilities](#abstract-utilities)
  - [Abstract Webtools](#abstract-webtools)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

## Introduction

[Short introduction or overview about the package.]

## Installation

[Instructions on how to install the package, perhaps with pip or another package manager.]

```
pip install abstract_essentials
```

## Modules
---

### Abstract Security
Manages and accesses environment variables in `.env` files, with a unique search capability across multiple directories.
- **Features**:
  - [Brief description of notable features.]
  - ...

**Description:**  
Abstract Security simplifies the management and access of environment variables stored in `.env` files. Its key feature is the ability to search multiple directories for these files, ensuring you always fetch the right environment variables with minimal hassle.

- **Dependencies**:
 - `os`
 - `dotenv`
 - Various utilities from `abstract_utilities`

- **Functions**:

### 1. `find_and_read_env_file`
- **Purpose**: Search for an environment file and read a specific key from it.
- **Arguments**:
  - `file_name`: Name of the `.env` file to be searched. Defaults to `.env`.
  - `key`: Key to be retrieved from the `.env` file. Defaults to 'MY_PASSWORD'.
  - `start_path`: Directory path to start the search from. Defaults to the current directory.
- **Returns**: The value corresponding to the key if found, otherwise None.

### 2. `search_for_env_key`
- **Purpose**: Search for a specific key in a `.env` file.
- **Arguments**:
  - `path`: The path to the `.env` file.
  - `key`: The key to search for.
- **Returns**: The value of the key if found, otherwise None.

### 3. `check_env_file`
- **Purpose**: Check if the environment file exists in a specified path.
- **Arguments**:
  - `path`: The path to check for the `.env` file.
  - `file_name`: The name of the `.env` file. Defaults to '.env'.
- **Returns**: The path of the `.env` file if it exists, otherwise False.

### 4. `safe_env_load`
- **Purpose**: Safely load the `.env` file if it exists at a specified path.
- **Arguments**:
  - `path`: The path to load the `.env` file from.
- **Returns**: True if the `.env` file is successfully loaded, otherwise False.

### 5. `get_env_value`
- **Purpose**: Retrieves the value of the specified environment variable.
- **Arguments**:
  - `start_path`: The path to the environment file.
  - `file_name`: The name of the environment file. Defaults to '.env'.
  - `key`: The key to search for. Defaults to 'MY_PASSWORD'.
- **Returns**: The value of the environment variable if found, otherwise None.

**Author**: putkoff
**Part of**: abstract_audio
**Date**: 05/31/2023
**Version**: 0.0.1.0


## Speech to Text

**Description:**  
The Speech to Text module enables the capture and manipulation of audio input from a microphone, converting it into text and saving it into a file. This module employs an abstract graphical user interface (GUI) to display the audio recording and playback status.

**Dependencies**:
- `os`
- `speech_recognition` (as `sr`)
- `abstract_utilities` (specifically, functions from `read_write_utils`, `cmd_utils`, and `thread_utils`)
- `abstract_gui`

**Functions**:

### 1. `change_glob`
- **Purpose**: Update a global variable with a given value.
- **Arguments**:
  - `x`: Name of the global variable to be updated.
  - `y`: Value to be set for the global variable.
- **Returns**: Updated value of the global variable.

### 2. `mic_switch`
- **Purpose**: Toggle the microphone state.
- **Returns**: Output of the 'amixer set Capture toggle' command.

### 3. `parse_mic_state`
- **Purpose**: Parse the microphone state from the 'amixer' command output.
- **Arguments**:
  - `st`: Output of the 'amixer' command.
- **Returns**: Parsed microphone state.

### 4. `get_mic_state`
- **Purpose**: Retrieve the current microphone state.
- **Returns**: Current microphone state.

### 5. `win_update`
- **Purpose**: Update the GUI window with new values for a given key.
- **Arguments**:
  - `win`: The GUI window object to update.
  - `st`: The key to update in the window values dictionary.
  - `data`: The data to set for the specified key.

### 6. `get_values`
- **Purpose**: Retrieve a value from the GUI window's stored values using the given key.
- **Arguments**:
  - `st`: The key to retrieve from the window values dictionary.
- **Returns**: Value associated with the given key.

### 7. `save_voice`
- **Purpose**: Save the voice recording to a file and update the GUI window.
- **Arguments**:
  - `voice`: The voice recording data to save.

### 8. `playback`
- **Purpose**: Start the speech recognition process and update the GUI window with recognized text.

### 9. `ambient_noise`
- **Purpose**: Adjust for ambient noise before starting the actual audio recording.

### 10. `listen_audio`
- **Purpose**: Listen for audio input and store it in the global variable 'audio'.

### 11. `recognzer`
- **Purpose**: Perform speech recognition on the recorded audio and update the 'voice_value' global variable.

### 12. `start_recording`
- **Purpose**: Start the audio recording process and handle exceptions for KeyboardInterrupt.

### 13. `record_hit`
- **Purpose**: Toggle the microphone state based on the specified boolean value.
- **Arguments**:
  - `bool_it`: Boolean value specifying the microphone state.

### 14. `stop_record`
- **Purpose**: Stop the audio recording process and update the GUI elements accordingly.
- **Arguments**:
  - `window`: The GUI window object to update.

### 15. `recording_true`
- **Purpose**: Set the recording flag to True.

### 16. `record_button`
- **Purpose**: Update GUI elements to indicate that recording is in progress.
- **Arguments**:
  - `window`: The GUI window object to update.

### 17. `get_gui_layout`
- **Purpose**: Define the layout for the PySimpleGUI GUI window.
- **Returns**: Layout of the GUI.

### 18. `voice_record_function`
- **Purpose**: Handle different events triggered by the GUI window and perform corresponding actions.
- **Arguments**:
  - `event`: Name of the event triggered in the GUI.

### 19. `speech_to_text_gui`
- **Purpose**: Initialize the GUI window, set global variables, and start the main GUI event loop.

### 20. `speech_to_text_main`
- **Purpose**: Main function to setup global variables, initialize the SpeechRecognizer and Microphone objects, and start the GUI.
- **Returns**: Result from the GUI initialization and loop.

---

**Author**: putkoff
**Part of**: abstract_audio
**Date**: 05/31/2023
**Version**: 0.0.1.0

To use this script, execute it as a Python program. It will open a GUI window with a 'record' button. Clicking on the 'record' button will initiate audio recording, and the GUI screen will turn green to indicate recording. Once you stop speaking, the recorded audio will be processed using the Google Web Speech API, and the recognized text will be displayed in the GUI window.

Note: Ensure that the required libraries are installed, including `abstract_utilities`, `abstract_gui`, and `speech_recognition`.


## Abstract Modules

This package provides a set of utilities to make Python module management easier, with a particular focus on the creation, packaging, and distribution of modules. Its key features include the upload of Python modules to PyPI and the management of the module's version number.

Abstract Modules is composed of three components: upload_utils.py, module_utils.py, and create_module_folder.py

### Upload Utils

**Description:**  
Upload Utils provides a utility script to easily upload a Python module to the Python Package Index (PyPI) using Twine. It also handles the versioning and installation requirements of the module.

#### Functions:

##### `get_parent_directory(directory: str) -> str`
- **Purpose**: Opens a file browser to allow the user to pick a module directory and returns the chosen directory. If no directory is chosen, it keeps prompting until a selection is made.
- **Arguments**:
  - `directory`: The initial directory to open the file browser. Defaults to the current working directory.
- **Returns**: The path of the selected directory.

##### `get_output_text(parent_directory: str) -> str`
- **Purpose**: Generate the path for the output text file based on the provided directory.
- **Arguments**:
  - `parent_directory`: Base directory.
- **Returns**: Path to the output text file.

##### `install_setup() -> str`
- **Purpose**: Return the command to install setup.
- **Returns**: Command string.

##### `install_twine() -> str`
- **Purpose**: Return the command to install twine.
- **Returns**: Command string.

##### `build_module(dist_dir: str) -> str`
- **Purpose**: If the 'dist' directory doesn't exist, create it. Return the command to build the module.
- **Arguments**:
  - `dist_dir`: Directory to build the module in.
- **Returns**: Command string.

##### `module_upload_cmd() -> str`
- **Purpose**: Return the command to upload the module.
- **Returns**: Command string.

##### `upload_module(output_text: str) -> str`
- **Purpose**: Execute the module upload command and handle the required child runs.
- **Arguments**:
  - `output_text`: Path to the output text.
- **Returns**: Response from the command execution.

The process of uploading a module involves also functions to handle editing the setup file, changing the version number of the module, and installing the module. For a full summary of functions and their usage, please refer to the code comments of the upload_utils.py file.

**Usage**:

```bash
python3 upload_utils.py
```

### Scan Folder Utils

**Description:**  
Scan Folder Utils provides utilities for scanning folders and Python scripts, which can be used to analyze the dependencies of a Python project. It also gathers documentation from the Python files in a selected folder. 

File: `module_utils.py`

**Dependencies**:
- `os`
- `ast`
- `re`
- `importlib`
- `inspect`
- `abstract_gui`
- `pkg_resources`

**Functions**:

##### `scan_folder_for_required_modules(folder_path: str = None, exclude: Union[str, list] = []) -> list`
- **Purpose**: Scan the specified folder for Python files and create a list of necessary Python modules according to the import statements in the Python scripts.
- **Arguments**:
  - `folder_path`: The path of the folder to scan. If None, a folder will be picked using a GUI window.
  - `exclude`: A list of module names that will be excluded from the output. Defaults to an empty list.
- **Returns**: A list of required Python modules based on all Python files found in the folder.

##### `get_installed_versions(install_requires: list) -> list`
- **Purpose**: Get the version numbers of the installed Python modules listed in 'install_requires'.
- **Arguments**:
  - `install_requires`: A list of Python module names with optional version constraints.
- **Returns**: A list of module names with their version numbers appended.

##### `is_valid_package_name(package_name: str) -> bool`
- **Purpose**: Check if a given package name is a valid Python package name.
- **Arguments**:
  - `package_name`: Package name to be validated.
- **Returns**: True if the package name is valid, False otherwise.

##### `gather_header_docs(folder_path: str) -> str`
- **Purpose**: Gather header documentation from Python modules within a specified folder.
- **Arguments**:
  - `folder_path`: Path to the folder containing Python modules.
- **Returns**: Concatenated header documentation for classes with docstrings.

**Usage**:

```python
# Scan a folder for required modules
required_modules = scan_folder_for_required_modules('/path/to/project')

# Get installed versions of required modules
installed_versions = get_installed_versions(required_modules)

# Check if a package name is valid
is_valid = is_valid_package_name('package_name')

# Gather header documentation from Python modules
docs = gather_header_docs('/path/to/project')
```
## Create Module Folder

**Description:**  
Create Module Folder is a utility script providing an interactive process to facilitate the setup of a Python module. This script helps building the module's structure, and automatically generates required files such as README.md, setup.cfg, pyproject.toml, main.py and a license file. 

The output of the process is the path of the created module folder, which can then be further developed or uploaded to a package index like PyPI.

File: `create_module_folder.py`

**Dependencies**:
- `abstract_utilities.string_clean`
- `abstract_utilities.path_utils`
- `abstract_utilities.read_write_utils`
- `abstract_gui`

**Usage**:

This function can be used from Python directly as follows:

```python
from create_module_folder import create_module_folder

module_folder_path = create_module_folder()
print("New module folder created at:", module_folder_path)
```

Or can be called from shell:

```bash
python3 create_module_folder.py
```

### Functions:

#### `create_module_folder() -> str`
- **Purpose**: Generate a new module folder with required files based on user input through an interactive process.
- **Returns**: Path of the created module folder.

For grasp of the flow and details of the generation process, explore the other functions in the code such as `create_setup_cfg()`, `create_toml()` and `licenses()`. The functions range from creating different configuration files, to retrieving and formatting details like the system date and time. User input and form handling are managed through a number of functions like `get_readme()`, `check_paths()` and `value_function()`.

The script also provides flexibility by letting the user choose specific configuration options for the module. For instance, they specify the type of license the project will be using, and whether certain files need to be created. For a full rundown of functions and their usage, please refer to the code comments of the create_module_folder.py file.


### Abstract AI
Enhances AI interactions with utilities for API handling, requests, tokenization, and more.
- **Developed By**: putkoff
- **Features**:
  - [Brief description of notable features.]
  - ...

Certainly! Here's the provided content reformatted for consistency with the previous structure:

---

## Abstract GUI Module

The `abstract_gui` module provides classes and functions to manage PySimpleGUI windows and events in a more abstract manner. It includes a class called `WindowGlobalBridge` to manage global variables shared between different scripts and a class called `WindowManager` to manage PySimpleGUI windows and their events.

### Installation

You can install the `abstract_gui` module using `pip`:

```
pip install abstract_gui
```
### Features

* Feature 1
* Feature 2
* ... 

Certainly! Here's the "Dependencies" section formatted similarly to the previous sections:

### **Dependencies**:

- #### `import PySimpleGUI as sg`
    - **Purpose**: PySimpleGUI offers a simpler way to create desktop applications.

- #### `from abstract_utilities.thread_utils import thread_alive`
    - **Purpose**: Imports the `thread_alive` function from the `thread_utils` module of the `abstract_utilities` package. This function is likely used to check if a particular thread is still running.

- #### `from abstract_utilities.class_utils import get_fun`
    - **Purpose**: Imports the `get_fun` function from the `class_utils` module of the `abstract_utilities` package. The function might retrieve a specific function or method from a class or module.

- #### `from abstract_utilities.path_utils import get_current_path`
    - **Purpose**: Imports the `get_current_path` function from the `path_utils` module of the `abstract_utilities` package. This function is probably used to retrieve the current working directory or path.

### Components


#### abstract_gui.py
##### Functions
##### Class Functions
##### WindowGlobalBridge
* **Attributes**
  * `global_vars (dict)`:  A dictionary to store global variables for each script.
* **Methods**
  * `__init__`
    ```python
    def __init__(self):
    """
    Initializes the WindowGlobalBridge with an empty dictionary for global_vars.
    """
    self.global_vars = {}
    ```
    **Purpose:**
    Initializes the WindowGlobalBridge with an empty dictionary for global_vars.

  * `retrieve_global_variables`
    ```python
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

    ```
    **Purpose:**
    Stores the global variables of a script in the global_vars dictionary.

    **Arguments:**
    * script_name (str): The name of the script.
    * global_variables (dict): The global variables to store for the script.
    * tag_script_name (bool, optional): If True, the script_name will be stored in the global_variables dictionary. Defaults to False.

  * `return_global_variables`
    ```python
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

    ```
    **Purpose:**
    Returns the global variables of a script.

    **Arguments:**
    * script_name (str, optional): The name of the script. If None, all global variables will be returned.

    **Returns:**
    * dict: The global variables of the script. If no global variables are found, it returns an empty dictionary.

  * `change_globals`
    ```python
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
    ```
    **Purpose:**
    Modifies a global variable value for a specified script.

    **Arguments:**
    * variable (str): The name of the global variable to modify.
    * value (any): The new value to assign to the global variable.
    * script_name (str, optional): The name of the script. If None, the global variable in the base context will be modified.

  * `search_globals_values`
    ```python
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
    ```
    **Purpose:**
    Searches for a specific value in the global variables of a script.

    **Arguments:**
    * value (any): The value to search for in the global variables.
    * script_name (str, optional): The name of the script. If None, the search will be performed in the base context.

    **Returns:**
    * str or False: The name of the first global variable containing the given value, or False if not found.

##### WindowManager
* **Attributes**
  * `all_windows (dict)`:  A dictionary to store registered windows along with their details.
  * `last_window (str)`:  The name of the last accessed window.
  * `script_name (str)`:  The name of the script that is using the WindowManager.
  * `global_bridge`:  The global bridge to access shared variables between different scripts.
  * `global_vars (dict)`:  A dictionary to store global variables for this script.
* **Methods**
  * `__init__`
    ```python
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
    ```
    **Purpose:**
    Initialize a WindowManager instance.

    **Arguments:**
    * script_name (str): The name of the script that is using the WindowManager.
    * global_bridge (GlobalBridge): An instance of GlobalBridge to access shared variables between different scripts.

  * `get_all_windows`
    ```python
    def get_all_windows(self):
    """
    Get all registered windows.

    Returns:
        dict: A dictionary containing all registered windows and their details.
    """
    return self.all_windows
    ```
    **Purpose:**
    Get all registered windows.

  * `get_window_names`
    ```python
    def get_window_names(self):
    """
    Get the names of all registered windows.

    Returns:
        list: A list of names of all registered windows.
    """
    return self.delete_from_list(list(self.get_all_windows().keys()), 'last_window')
    ```
    **Purpose:**
    Get the names of all registered windows.

  * `register_window`
    ```python
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
    ```
    **Purpose:**
    Register a window.

    **Arguments:**
    * obj (any, optional): The window to register. If not provided, a new window is created.

    **Returns:**
    * str: The name of the registered window.

  * `get_new_window`
    ```python
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

  * `search_global_windows`
    ```python
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
    ```
    **Purpose:**
    Search for a window in the global variables.

    **Arguments:**
    * window (any): The window to search for.

    **Returns:**
    * any: The name of the window if found, False otherwise.

  * `verify_window`
    ```python
    def verify_window(self, window=None) -> bool:
    """
    Verifies if the given object is a valid PySimpleGUI window.

    Args:
        win (any): The object to verify.

    Returns:
        bool: True if the object is a valid window, False otherwise.
    """
    return self.search_global_windows(window=window) != False
    ```
    **Purpose:**
    Verifies if the given object is a valid PySimpleGUI window.

    **Arguments:**
    * win (any): The object to verify.

    **Returns:**
    * bool: True if the object is a valid window, False otherwise.

  * `update_last_window`
    ```python
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
    ```
    **Purpose:**
    Update the last accessed window.

    **Arguments:**
    * window (any): The window to set as the last accessed window.

  * `send_to_bridge`
    ```python
    def send_to_bridge(self):
    """
    Update the global bridge with the current state of the windows.
    """
    self.global_vars["all_windows"] = self.all_windows
    self.global_bridge.retrieve_global_variables(self.script_name, self.global_vars)
    ```
    **Purpose:**
    Update the global bridge with the current state of the windows.

  * `close_window`
    ```python
    def close_window(self, window=None):
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
    ```
    **Purpose:**
    Closes the given PySimpleGUI window.

    **Arguments:**
    * win (any): The window to close.

  * `read_window`
    ```python
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
    ```
    **Purpose:**
    Read the event and values from a window and update the WindowManager's state.

    **Arguments:**
    * window (any): The window to read from.

  * `get_last_window_info`
    ```python
    def get_last_window_info(self):
    """
    Retrieve the details of the last accessed window.

    Returns:
        dict: Dictionary containing information about the last accessed window or None if there's no such window.
    """
    last_window = self.all_windows['last_window']
    if last_window != None:
        return self.all_windows[last_window]
    ```
    **Purpose:**
    Retrieve the details of the last accessed window.

  * `get_last_window_method`
    ```python
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

    ```
    **Purpose:**
    Get the method associated with the last accessed window.

  * `update_values`
    ```python
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
    ```
    **Purpose:**
    Update the values associated with a given window.

    **Arguments:**
    * window (any, optional): The window to update values for. Defaults to the last accessed window.
    * key (str, optional): The key to be updated in the window.
    * value (any, optional): The value to set for the given key.
    * values (any, optional): Multiple values to set.
    * args (dict, optional): Additional arguments to update the window with.

  * `get_event`
    ```python
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

    ```
    **Purpose:**
    Get the last event from a window.

    **Arguments:**
    * win (any, optional): The window to get the event from. If not provided, the last accessed window is used.

    **Returns:**
    * any: The last event from the window.

  * `get_values`
    ```python
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

    ```
    **Purpose:**
    Get the values from a window.

    **Arguments:**
    * win (any, optional): The window to get the values from. If not provided, the last accessed window is used.

    **Returns:**
    * dict: The values from the window.

  * `while_basic`
    ```python
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
    ```
    **Purpose:**
    Run an event loop for a window.

    **Arguments:**
    * window (any, optional): The window to run the event loop for. If not provided, the last accessed window is used.

  * `get_window_name`
    ```python
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
    ```
    **Purpose:**
    Get the names of all registered windows.

  * `win_closed`
    ```python
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
    ```
    **Purpose:**
    Check if a window event calls to close the window.

    **Arguments:**
    * event (str): The event to check.

    **Returns:**
    * bool: True if the window is closed, False otherwise.

#### Stand Alone Functions
* `create_row`
  ```python
  def create_row(*args):
    """
    Create a row layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the row layout.

    Returns:
        list: A row layout containing the provided elements.
    """
    return [arg for arg in args]
  ```
  **Purpose:**
  Create a row layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the row layout.

  **Returns:**
  * list: A row layout containing the provided elements.

---
* `create_column`
  ```python
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
  ```
  **Purpose:**
  Create a column layout containing the provided arguments.

  **Arguments:**
  * *args: Elements to be placed in the column layout.

  **Returns:**
  * list: A column layout containing the provided elements.

---
* `concatenate_rows`
  ```python
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
  ```
  **Purpose:**
  Concatenate multiple row layouts into a single row layout.

  **Arguments:**
  * *args: Row layouts to be concatenated.

  **Returns:**
  * list: A row layout containing concatenated elements from input row layouts.

---
* `concatenate_layouts`
  ```python
  def concatenate_layouts(*args):
    """
    Concatenate multiple layouts into a single layout.

    Args:
        *args: Layouts to be concatenated.

    Returns:
        list: A layout containing concatenated elements from input layouts.
    """
    return concatenate_lists(args)
  ```
  **Purpose:**
  Concatenate multiple layouts into a single layout.

  **Arguments:**
  * *args: Layouts to be concatenated.

  **Returns:**
  * list: A layout containing concatenated elements from input layouts.

---
* `create_row_of_buttons`
  ```python
  def create_row_of_buttons(*args):
    """
    Create a row layout containing buttons generated from the provided arguments.

    Args:
        *args: Arguments for creating buttons.

    Returns:
        list: A row layout containing buttons created from the provided arguments.
    """
    return [button for arg in args for button in get_buttons(arg)]

  ```
  **Purpose:**
  Create a row layout containing buttons generated from the provided arguments.

  **Arguments:**
  * *args: Arguments for creating buttons.

  **Returns:**
  * list: A row layout containing buttons created from the provided arguments.

---
* `get_buttons`
  ```python
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

  ```
  **Purpose:**
  Generate button elements based on the provided arguments.

  **Arguments:**
  * *args: Arguments specifying button elements.

  **Returns:**
  * list: Button elements generated from the provided arguments.

---
* `if_not_window_make_window`
  ```python
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
  ```
  **Purpose:**
  Checks if the provided object is a window and creates a new window if it isn't.

  **Arguments:**
  * window: The object to be checked. If not a window, it's expected to be a dictionary with layout information.

  **Returns:**
  * window: The valid window object.

---
* `while_quick`
  ```python
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
      
  ```
  **Purpose:**
  Reads events from the given window and handles them based on the provided conditions.

  **Arguments:**
  * window: The window to read events from.
  * return_events (list or str): Events that would lead to the window being closed and a value returned.
  * exit_events (list or str): Events that would lead to the window being closed without returning a value.
  * event_return (bool): If True, returns the event. If False, returns the values.

  **Returns:**
  * event or values: Depending on the event_return flag.

---
* `verify_args`
  ```python
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
  ```
  **Purpose:**
  Verifies and/or sets default values for window arguments.

  **Arguments:**
  * args (dict, optional): Dictionary containing window arguments.
  * layout (list, optional): The layout for the window.
  * title (str, optional): The title of the window.
  * event_function (str, optional): The function to be executed when an event occurs.
  * exit_events (list or str, optional): List of events that would close the window.

  **Returns:**
  * dict: The verified/updated window arguments.

---
* `get_window`
  ```python
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
    args = verify_args(args=args, layout=layout, title=title)
    return get_gui_fun('Window', {**args})
  ```
  **Purpose:**
  Get a PySimpleGUI window.

  **Arguments:**
  * win_name (str, optional): The name of the window. If not provided, a unique name is generated.
  * layout (list, optional): The layout of the window. If not provided, an empty layout is used.
  * args (dict, optional): Additional arguments for the window.

  **Returns:**
  * any: A PySimpleGUI window.

---
* `get_browser_layout`
  ```python
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
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* `get_yes_no_layout`
  ```python
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
  ```
  **Purpose:**
  Creates a layout for a Yes/No window.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * args (dict, optional): Additional arguments for the window.

  **Returns:**
  * dict: The layout dictionary.

---
* `get_input_layout`
  ```python
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
  ```
  **Purpose:**
  Function to get a browser GUI based on the type specified.
Parameters:
type (str): The type of GUI window to display. Defaults to 'Folder'.
title (str): The title of the GUI window. Defaults to 'Directory'.

---
* `get_yes_no`
  ```python
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
  ```
  **Purpose:**
  Creates and displays a Yes/No window, then captures the user response.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * args (dict, optional): Additional arguments for the window.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to a response being returned.
  * event_return (bool, optional): If True, returns the event. If False, returns the values.

  **Returns:**
  * event or values: Depending on the event_return flag.

---
* `get_input`
  ```python
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
    
  ```
  **Purpose:**
  Creates and displays an input window, then captures the user input.

  **Arguments:**
  * title (str, optional): The title of the window.
  * text (str, optional): The prompt text.
  * default (str, optional): The default input value.
  * args (dict, optional): Additional arguments for the window.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to an input being returned.

  **Returns:**
  * values: The captured user input.

---
* `get_browser`
  ```python
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
  ```
  **Purpose:**
  Creates and displays a browser window, then captures the user-selected path.

  **Arguments:**
  * title (str, optional): The title of the window.
  * type (str, optional): The type of browser (e.g., 'Folder').
  * args (dict, optional): Additional arguments for the window.
  * initial_folder (str, optional): The folder to start browsing from.
  * exit_events (str or list, optional): List of events that would close the window.
  * return_events (str or list, optional): List of events that would lead to a path being returned.

  **Returns:**
  * results: The selected path or default path if none is selected.

---
* `get_gui_fun`
  ```python
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
  ```
  **Purpose:**
  Returns a callable object for a specific PySimpleGUI function with the provided arguments.

  **Arguments:**
  * name (str): The name of the PySimpleGUI function.
  * args (dict): The arguments to pass to the PySimpleGUI function.

  **Returns:**
  * callable: A callable object that invokes the PySimpleGUI function with the specified arguments when called.

---
* `create_window_manager`
  ```python
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
    js_bridge = bridge.retrieve_global_variables(script_name, global_var)
    return WindowManager(script_name, bridge),bridge,script_name

  ```
  **Purpose:**
  Initializes a window manager for a given script.

  **Arguments:**
  * script_name (str, optional): The name of the script.
  * global_var (dict, optional): The global variables associated with the script.

  **Returns:**
  * tuple: A tuple containing the WindowManager, bridge, and script name.

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
#### Module Information
- **Author**: putkoff
- **Author Email**: partners@abstractendeavors.com
- **Github**: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_gui
- **PYPI**: https://pypi.org/project/abstract-gui
- **Part of**: abstract_essentials
- **Date**: 08/29/2023
- **Version**: 0.0.56.7
- 
---

### Abstract Images
Offers tools for image and PDF tasks.
- **Features**:
  - [Brief description of notable features.]
  - ...

### Abstract Utilities
A comprehensive suite for various tasks.
- **Features**:
  - [Brief description of notable features.]
  - ...

---
## Abstract WebTools
Provides utilities for inspecting and parsing web content, including React components and URL utilities, with enhanced capabilities for managing HTTP requests and TLS configurations.

- **Features**:
  - URL Validation: Ensures URL correctness and attempts different URL variations.
  - HTTP Request Manager: Custom HTTP request handling, including tailored user agents and improved TLS security through a custom adapter.
  - Source Code Acquisition: Retrieves the source code of specified websites.
  - React Component Parsing: Extracts JavaScript and JSX source code from web pages.
  - Comprehensive Link Extraction: Collects all internal links from a specified website.
  - Web Content Analysis: Extracts and categorizes various web content components such as HTML elements, attribute values, attribute names, and class names.

### abstract_webtools.py
**Description:**  
Abstract WebTools offers a suite of utilities designed for web content inspection and parsing. One of its standout features is its ability to analyze URLs, ensuring their validity and automatically attempting different URL variations to obtain correct website access. It boasts a custom HTTP request management system that tailors user-agent strings and employs a specialized TLS adapter for heightened security. The toolkit also provides robust capabilities for extracting source code, including detecting React components on web pages. Additionally, it offers functionalities for extracting all internal website links and performing in-depth web content analysis. This makes Abstract WebTools an indispensable tool for web developers, cybersecurity professionals, and digital analysts.

- **Dependencies**:
  - `requests`
  - `ssl`
  - `HTTPAdapter` from `requests.adapters`
  - `PoolManager` from `urllib3.poolmanager`
  - `ssl_` from `urllib3.util`
  - `urlparse`, `urljoin` from `urllib.parse`
  - `BeautifulSoup` from `bs4`

#### **Functions**:
##### **Classes**:

- ###### `TLSAdapter(HTTPAdapter: int)`
    - **Description**: A custom HTTPAdapter class that sets TLS/SSL options and ciphers.
    - **Attributes**:
      - `ssl_options (int)`: The TLS/SSL options to use when creating the SSL context.
    - **Methods**:
        - `ssl_options(self) -> int`
            - **Purpose**: Returns the SSL options to be used when creating the SSL context.
            - **Returns**: The SSL options.
        - `__init__(self, ssl_options:int=0, *args, **kwargs) -> None`
            - **Purpose**: Initializes the TLSAdapter with the specified SSL options.
            - **Arguments**:
                - `ssl_options (int, optional)`: The TLS/SSL options to use when creating the SSL context. Defaults to 0.
        - `add_string_list(self, ls: (list or str), delim: str = '', string: str = '') -> str`
            - **Purpose**: Concatenates the elements of a list into a single string with the given delimiter.
            - **Arguments**:
                - `ls (list or str)`: The list of elements or a comma-separated string.
                - `delim (str, optional)`: The delimiter to use when concatenating elements. Defaults to an empty string.
                - `string (str, optional)`: The initial string to append elements. Defaults to an empty string.
            - **Returns**: The concatenated string.
        - `get_ciphers(self) -> list`
            - **Purpose**: Returns a list of preferred TLS/SSL ciphers.
            - **Returns**: A list of TLS/SSL ciphers.
        - `create_ciphers_string(self, ls: list = None) -> str`
            - **Purpose**: Creates a colon-separated string of TLS/SSL ciphers from a list of ciphers.
            - **Arguments**:
                - `ls (list, optional)`: The list of TLS/SSL ciphers to use. Defaults to None, in which case it uses the default list.
            - **Returns**: The colon-separated string of TLS/SSL ciphers.
        - `init_poolmanager(self, *args, **kwargs) -> None`
            - **Purpose**: Initializes the pool manager with the custom SSL context and ciphers.
            - **Description**: This method leverages the given TLS/SSL ciphers and options to set up the pool manager with an appropriate SSL context.

- ##### `get_status(url:str) -> int`
    - **Purpose**: Gets the HTTP status code of the given URL.
    - **Arguments**:
- `url`: The URL to check the status of.
    - **Returns**: The HTTP status code of the URL, or None if the request fails.

- ##### `clean_url(url:str) -> list`
    - **Purpose**: Cleans the given URL and returns a list of possible variations.
    - **Arguments**:
        - `url`: The URL to clean.
    - **Returns**: A list of possible URL variations, including 'http://' and 'https://' prefixes.

- ##### `get_correct_url(url: str, session: type(requests.Session) = requests) -> (str or bool)`
    - **Purpose**: Gets the correct URL from the possible variations by trying each one with an HTTP request.
    - **Arguments**:
      - `url`: The URL to find the correct version of.
      - `session`: The requests session to use for making HTTP requests. Defaults to requests.
    - **Returns**: The correct version of the URL if found, or None if none of the variations are valid.

- ##### `try_request(url: str, session: type(requests.Session) = requests) -> (str or bool)`
    - **Purpose**: Tries to make an HTTP request to the given URL using the provided session.
    - **Arguments**:
      - `url`: The URL to make the request to.
      - `session`: The requests session to use for making HTTP requests. Defaults to requests.
    - **Returns**: The response object if the request is successful, or None if the request fails.

- ##### `is_valid(url:str) -> bool`
    - **Purpose**: Checks whether `url` is a valid URL.
    - **Arguments**:
      - `url`: The URL to check.
    - **Returns**: True if the URL is valid, False otherwise.

- ##### `desktop_user_agents() -> list`
    - **Purpose**: Returns a list of popular desktop user-agent strings for various browsers.
    - **Returns**: A list of desktop user-agent strings.

- ##### `get_user_agent(user_agent=desktop_user_agents()[0]) -> dict`
    - **Purpose**: Returns the user-agent header dictionary with the specified user-agent.
    - **Arguments**:
      - `user_agent`: The user-agent string to be used. Defaults to the first user-agent in the list.
    - **Returns**: A dictionary containing the 'user-agent' header.



- ##### `get_Source_code(url: str = 'https://www.example.com', user_agent= desktop_user_agents()[0]) -> str`
    - **Purpose**: Fetches the source code of the specified URL using a custom user-agent.
    - **Arguments**:
      - `url (str, optional)`: The URL to fetch the source code from. Defaults to 'https://www.example.com'.
      - `user_agent (str, optional)`: The user-agent to use for the request. Defaults to the first user-agent in the list.
    - **Returns**: The source code of the URL if the request is successful, or None if the request fails.

- ##### `parse_react_source(url:str) -> list`
    - **Purpose**: Fetches the source code of the specified URL and extracts JavaScript and JSX source code (React components).
    - **Arguments**:
      - `url (str)`: The URL to fetch the source code from.
    - **Returns**: A list of strings containing JavaScript and JSX source code found in <script> tags.

- ##### `get_all_website_links(url:str) -> list`
    - **Purpose**: Returns all URLs that are found on the specified URL and belong to the same website.
    - **Arguments**:
      - `url (str)`: The URL to search for links.
    - **Returns**: A list of URLs that belong to the same website as the specified URL.

- ##### `parse_all(url:str) -> dict`
    - **Purpose**: Parses the source code of the specified URL and extracts information about HTML elements, attribute values, attribute names, and class names.
    - **Arguments**:
      - `url (str)`: The URL to fetch the source code from.
    - **Returns**: A dict containing keys: [element_types, attribute_values, attribute_names, class_names] with values as lists for keys element types, attribute values, attribute names, and class names found in the source code.

- ##### `extract_elements(url:str=None, source_code:str=None, element_type=None, attribute_name=None, class_name=None) -> list`
    - **Purpose**: Extracts portions of the source code from the specified URL based on provided filters.
    - **Arguments**:
      - `url (str, optional)`: The URL to fetch the source code from.
      - `source_code (str, optional)`: The source code of the desired domain.
      - `element_type (str, optional)`: The HTML element type to filter by. Defaults to None.
      - `attribute_name (str, optional)`: The attribute name to filter by. Defaults to None.
      - `class_name (str, optional)`: The class name to filter by. Defaults to None.
    - **Returns**:  list: A list of strings containing portions of the source code that match the provided filters, or None if url and source_code are not provided.


#### Usage

##### Get Status Code

The `get_status` function fetches the status code of the URL.

```python
from abstract_webtools import clean_url

urls = clean_url('https://example.com')
print(urls)  # Output: ['https://example.com', 'http://example.com']
tps://example.com'
```

##### Try Request

The `try_request` function makes HTTP requests to a URL and returns the response if successful.

```python
from abstract_webtools import try_request

response = try_request('https://www.example.com')
print(response)  # Output: <Response [200]>
```

##### Is Valid URL

The `is_valid` function checks whether a given URL is valid.

```python
from abstract_webtools import is_valid

valid = is_valid('https://www.example.com')
print(valid)  # Output: True
```

##### Get Source Code

The `get_Source_code` function fetches the source code of a URL with a custom user-agent.

```python
from abstract_webtools import get_Source_code

source_code = get_Source_code('https://www.example.com')
print(source_code)  # Output: HTML source code of the URL
```

##### Parse React Source

The `parse_react_source` function fetches the source code of a URL and extracts JavaScript and JSX source code (React components).

```python
from abstract_webtools import parse_react_source

react_code = parse_react_source('https://www.example.com')
print(react_code)  # Output: List of JavaScript and JSX source code found in <script> tags
```

##### Get All Website Links

The `get_all_website_links` function returns all URLs found on a specified URL that belong to the same website.

```python
from abstract_webtools import get_all_website_links

links = get_all_website_links('https://www.example.com')
print(links)  # Output: List of URLs belonging to the same website as the specified URL
```

##### Parse All

The `parse_all` function fetches the source code of a URL and extracts information about HTML elements, attribute values, attribute names, and class names.

```python
from abstract_webtools import parse_all

HTML_components = parse_all('https://www.example.com')
print(HTML_components["element_types"])       # Output: List of HTML element types
print(HTML_components["attribute_values"])    # Output: List of attribute values
print(HTML_components["attribute_names"])     # Output: List of attribute names
print(HTML_components["class_names"])         # Output: List of class names
```

##### Extract Elements

The `extract_elements` function fetches the source code of a URL and extracts portions of the source code based on provided filters.

```python
from abstract_webtools import extract_elements

elements = extract_elements('https://www.example.com', element_type='div', attribute_name='class', class_name='container')
print(elements)  # Output: List of HTML elements that match the provided filters
```

#### Module Information
-**Author**: putkoff
-**Author Email**: partners@abstractendeavors.com
-**Github**: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_webtools
-**PYPI**: https://pypi.org/project/abstract-webtools
-**Part of**: abstract_essentials
-**Date**: 08/29/2023
-**Version**: 0.1.2
---

