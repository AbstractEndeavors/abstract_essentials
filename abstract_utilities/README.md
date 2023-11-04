
 # Abstract Utilities

  Abstract Utilities is a comprehensive collection of utility modules assembled to assist a multitude of common tasks. The aim of this collection is to eliminate the need to perpetually rewrite trivial but essential functions that are frequently used across projects. With minimal dependencies, this suite is an amalgam of bare essential functions, ranging from data comparison, string manipulation, mathematical operations, time tracking to JSON handling and others.

  The module's ease of use and detailed implementation allow for practical and efficient usage across different programs.

## Contents
  - [Introduction](#abstract-utilities)
  - [Modules](#modules)
  - [Installation](#installation)
  - [License](#license)
   
## Installation

  The package can be installed via pip by entering the following command:

  ```
  pip install abstract_utilities
  ~~or~~
  pip3 install abstract_utilities
  ```
  Ensure that you're using Python 3.11 or later, and the following dependencies are installed: 'pathlib>=1.0.1', 'abstract_security>=0.0.1', 'yt_dlp>=2023.10.13', 'pexpect>=4.8.0'.

  After you've installed the module, you can import any utility into your scripts using:
  ```
  from abstract_utilities import module_name
  ```

## Modules

  The repository contains several utility files, each dealing with a specific theme or operation. For example, `compare_utils.py` handles string and object comparison, `list_utils.py` helps with list manipulation, `json_utils.py` deals with JSON handling, and so on.

  In-depth analysis and explanation of each utility will be provided in the upcoming sections. On a high level, utilities covered are:
  - Class utilities
  - Command line utilities
  - Collator utilities
  - Comparison utilities
  - Global utilities
  - History utilities
  - JSON utilities
  - List utilities
  - Math utilities
  - Path utilities
  - Read-Write utilities
  - String utilities
  - Thread utilities
  - Time utilities
  - Type utilities

## License 

Abstract Utilities is licensed under the MIT License.

##### (Remainder of README coming soon. Each specific utility will be documented in the upcoming sections.)
## Class Utilities [class_utils.py](#modules)

This module includes helper methods tailored for manipulating and handling classes, objects, and modules. Some of the operations accomplished in the class utilities module include:

- Fetching and verifying object types.
- Manipulating global variables.
- Checking an object's membership status in a module.
- Inspecting function signatures and their arguments within a module.
- Executing functions with supplied arguments.
- Converting layout definitions into components.
- Accessing attributes and methods of a module.

### Key Functions:

1. **get_type_list:** This function helps to procure a list of common Python types.
2. **remove_key:** This function is used to remove a specific key from a provided dictionary.
3. **get_module_obj:** This function facilitates the retrieval of an object from a specified module.
4. **spec_type_mod:** This function checks whether an object matches a specific type.
5. **get_type_mod:** This function retrieves the type of a given object.
6. **is_module_obj:** This function checks if a provided object is part of a module.
7. **inspect_signature:** This function fetches the signature of a specified function within a module.
8. **get_parameter_defaults:** This method helps in fetching the default parameter values for a provided function in a module.
9. **convert_layout_to_components:** This utility converts a layout definition to its component representation.
10. **get_dir:** This function aids in listing all attributes and methods of a specified module.
11. **get_proper_args:** This function calls a function using either positional or keyword arguments based on the args type.
12. **get_fun:** This method parses a dictionary to retrieve a function and call it.
13. **if_none_change:** This function replaces a None object with a default value.
14. **call_functions:** Executes a specified function or method using provided arguments.
15. **process_args:** Evaluates and processes nested function calls in arguments.
16. **has_attribute:** Checks if a function exists in a module.
17. **get_all_functions_for_instance:** Retrieves all callable methods/functions of an object instance.

### Dependencies:

This utility module depends on two other Python modules: 'inspect' and 'json'. Each utility method in the module has its own docstring, offering a more in-depth explanation of its purpose, expected inputs, and outputs.
## Command Utilities

The `command_utils.py` houses a collection of utilities for executing commands with various functionalities, including handling of sudo, logging outputs, and interacting with commands that expect input.

### Functions 

1. **get_all_params(instance, function_name)**: This function retrieves information about the parameters of a callable method/function of an instance.

2. **mk_fun(module,function)**: This function checks if a function exists in a given module and prints a statement indicating whether the function exists or not.

3. **get_output_text(parent_dir)**: Provides the path to an 'output.txt' file in a given directory.

4. **get_env_value(key, env_path)**: Fetches the environment value associated with a provided key from a specific .env file path.

5. **print_cmd(input, output)**:Prints the executed command alongside its corresponding output.

6. **get_sudo_password(key)**: Retrieves the sudo password stored in an environment file.

7. **cmd_run_sudo(cmd, password, key, output_text)**: Executes a command with sudo privileges, either using a given password or retrieving it from an environment file.

8. **cmd_run(cmd, output_text)**: Executes a command and captures its output in a specified file.

9. **pexpect_cmd_with_args(command, child_runs, output_text)**: Interacts with a command's expected input using the pexpect library and logs the command's output.

10. **get_output(p)**: This function retrieves the output generated by a subprocess command execution.

11. **get_cmd_out(st)**: This function executes a shell command and retrieves the output generated by the command's execution.

### Dependencies
- os
- time
- pexpect
- subprocess
- abstract_security.envy_it: find_and_read_env_file, get_env_value
- abstract_utilities.time_utils: get_sleep 

### Notes
- Ensure the necessary dependencies are installed.
- Make sure you have appropriate permissions to execute commands, especially sudo-based ones.
- Always keep environment files secure and away from public access to ensure sensitive information like passwords remains confidential.
## Command Line Utilities

CommandLine utilities provide functions to interface with command line and appropriately handle its output and prompts. The utility includes methods for executing shell commands (including sudo commands), handling command prompts, and retrieving environment values.

Below are descriptions for some of the key functions available in the command line utilities section:

- `cmd_input(st: str) -> subprocess.Popen`
    - This function executes a shell command using subprocess module. It takes a command string as an argument and returns a subprocess.Popen object for communication.

- `get_output_text(parent_dir: str = os.getcwd()) -> str`
    - This function fetches the path to the 'output.txt' file in the provided directory. If no directory is provided it takes the current working directory.

- `get_env_value(key: str = None, env_path: str = None) -> str`
   - This function retrieves an environment value based on a key from a specified .env file. 

- `print_cmd(input: str, output: str) -> None`
    - This function prints the input command along with its corresponding output.

- `cmd_run_sudo(cmd: str, password: str = None, key: str = None, output_text: str = None) -> None`
    - This function executes a command with sudo privileges.

- `cmd_run(cmd: str, output_text: str = None) -> None`
    - This function executes a command and logs its output in a specified file.

- `pexpect_cmd_with_args(command: str, child_runs: list, output_text: str = os.getcwd()) -> int`
    - This function executes a command using pexpect and handles its prompts with specified responses. 

## Collator Utilities

Collator utilities offer functions related to operations with alphabets and numbers. It includes generating lists of alphabetic characters and numbers, finding an index of a character in a list, and more.

Key functions available in the collator utilities section are:

- `get_alpha_list() -> list`
    - This function generates a list containing all lowercase alphabets. 

- `get_num_list() -> list`
    - This function generates a list of numbers in string format. 

- `find_it_alph(ls: list, y: any) -> int`
   - This function finds the index of an element in a list. 

- `get_alpha(k: Union[int,float]) -> str`
    - This function retrieves the alphabetic character corresponding to the given index. 

## Compare Utilities

Compare Utilities offer functions for comparing strings and objects. These include methods for calculating string similarity and comparing the lengths of objects.
## Comparison Utilities

This section provides information about different functions present in the `compare_utils.py` module. These functions aid in various string comparison operations, counting specific characters in a string, safely getting length of the string etc.

Functions include:

- `get_comp(string:str, string_2:str)` : This function calculates the similarity between two strings based on overlapping sequences of characters.

- `get_lower(obj, obj2)` : This function compares the lengths of two objects or their string representations and returns the one with shorter length.

- `is_in_list(obj: any, ls: list = [])` : This function checks whether a given object is present in the list or not.

- `safe_len(obj: str = '')` : This function gets the length of the string representation of a given object in a manner that avoids exceptions.

- `line_contains(string: str = None, compare: str = None, start: int = 0, length: int = None)` : This function checks whether a substring is present in another string starting from a specific index.

- `count_slashes(url: str) -> int` : This function counts the number of slashes in a given URL.

- `get_letters() -> list` : This function returns a list of lowercase letters from 'a' to 'z'.

- `get_numbers() -> list` : This function returns a list of numeric digits from 0 to 9.

- `percent_integer_of_string(obj: str, object_compare: str = 'numbers') -> float` : This function calculates the percentage of characters in a string that are either letters or numbers.

- `return_obj_excluded(list_obj:str, exclude:str, substitute='*')` : This function replaces all occurrences of a specified substring with a substitute string in a given list_obj.

- `determine_closest(string_comp:str, list_obj:str)` : This function finds the closest consecutive substrings from comp in list_obj.

- `longest_consecutive(list_cons:list)` : This function calculates the length of the longest consecutive non-empty elements in a list of strings.

- `combined_list_len(list_cons:list)` : This function calculates the total length of a list of strings by summing their individual lengths.

- `percent_obj(list_cons:list, list_obj:str)` : This function calculates the percentage of the combined length of a list of strings relative to the length of a target string.

- `get_closest_match_from_list(comp_str:str, total_list:list, case_sensative:bool=True)` : This function finds the closest match from a list of strings based on various criteria such as longest consecutive substring, combined length of consecutive substrings, and percentage of combined length relative to the length of the target string.

- `untuple(obj)` : This function returns the first element of a tuple if the provided input is a tuple.
## Comparison Utilities

The `compare_utils.py` module provides functions that help compare and identify patterns or similarities between strings or group of strings.

`get_closest_match_from_list(comp_str:str, total_list:list,case_sensative:bool=True)`

This function finds the closest match from a list of strings to a target string based on various criteria such as longest consecutive substring, combined length of consecutive substrings, and percentage of combined length relative to the length of the target string. It returns the string from the list that best matches the target, or None if no match is found.

`make_list(obj)`

Converts an object into a list. Valid for set and tuple types.

`create_new_name(name=None, names_list=None, default=True, match_true=False, num=0)`

Creates a new name that does not exist in provided list of names. It can be used to avoid name collision when generating file names, variable names, etc. The function generates a unique name by appending an incrementing number at the end. The base name and the list of existing names can be provided as arguments. If not provided, it uses 'Default_name' as the base name.

`get_last_comp_list(string, compare_list)`

Finds and returns the last string in the 'compare_list' that contains the target 'string'. Returns None if no match is found.



## Global Utilities 

In `global_utils.py`, it provides functions to manage and manipulate global variables.

`global_registry(name:str,glob:dict)` 

It records the name and the dictionary of a global variable to a global registry. If the name is not in the registry, it adds it and the provided dictionary. It returns the index of the name in the registry.

`get_registry_number(name:str)` 

It returns the index of a name in the registry.

`update_registry(var:str, val:any, name:str)` 

It updates a global variable with a new value.

`get_global_from_registry(name:str)` 

It gets a dictionary of a global variable recorded in the registry using the name as reference.

`return_globals() -> dict` 

It returns the global variables dictionary.

`change_glob(var: str, val: any, glob: dict = return_globals()) -> any`

It changes the value of a global variable and returns the new value.

`get_globes(string:str='', glob:dict=return_globals())`

It gets a specified global variable.

`if_none_default(string:str, default:any, glob:dict=return_globals())`

It checks if a global variable is `None`, if it is, it assigns it a default value and updates the global variable.



## History Utilities 

The `history_utils.py` module comprises the `HistoryManager` class which allows to handle the history of objects, states or actions for undo/redo features.

`HistoryManager()`

This is the constructor for the `HistoryManager` class. It initializes a 'history_names' dictionary to store the history of different objects.

`add_history_name(self, name, initial_data='')`

This method adds a new object to the history with an initial state.

`transfer_state(self, primary_data, secondary_data)`

This method transfers the latest state from primary_data to secondary_data and returns the modified primary and secondary data.

`add_to_history(self, name, data)`

This method adds a new state to the history of an object.

`redo(self, name)`

This method reverts the object to the next state in the redo history. If no redo history exists, the object remains unchanged.
### JSON Utilities

'json_utils' is a utility module that allows you to work with JSON data. Its functionalities include:
1. Converting JSON strings to dictionaries and vice versa.
2. Merging, adding to, updating, and removing keys from dictionaries.
3. Retrieving keys, values, specific items, and key-value pairs from dictionaries.
4. Recursively displaying values of nested JSON data structures with indentation.
5. Loading from and saving dictionaries to JSON files.
6. Validating and cleaning up JSON strings.
7. Searching and modifying nested JSON structures based on specific keys, values, or paths.
8. Inverting JSON data structures.
9. Creating and reading from JSON files.

The module contains functions like 'json_key_or_default', 'all_try_json_loads', 'safe_dump_to_file', etc. Each function comes with elaborate Python docstrings that provide detailed usage instructions.

The utility, for instance, provides a function named 'create_and_read_json' that allows you to create a JSON file if it does not exist, and then read from it. It also offers functions like 'is_valid_json' which checks whether a given string is a valid JSON string.

Take this function 'safe_write_to_json', it safely writes data to a JSON file. If an error occurs during writing, the data is written to a temporary file first, and then the temporary file is replaced with the original one.

Other functions like 'safe_read_from_json', 'find_keys', 'all_try', 'safe_json_loads', 'try_json_loads', and 'unified_json_loader' provide ways to work with JSON data and make handling JSON in Python easier and more efficient.
[]
## path_utils.py

This module contains utility functions for processing file paths, directories, and files. This includes operations such as getting the home directory, checking if a path is a file, updating global variables, listing directory contents, and working with file sizes and directory sizes. The implemented functions are:

- `get_home_folder()`: This function returns the path to the home directory of the current user.

- `is_file(path: str) -> bool`: This function checks if the provided path is a file.

- `update_global_variable(name: str, value) -> None`: This function updates the global variable with the provided name and value.

- `list_directory_contents(path: str) -> list`: This function returns a list of directory contents or a list with a single file, if the path is a file.

- `trunc(a: float, x: int) -> float`: This function truncates a float number to a specific number of decimal places.

- `mkGb(k) -> float`: This function converts a value to Gigabytes (GB).

- `mkGbTrunk(k) -> float`: This function converts a value to GB and truncates the result to five decimal places.

- `mkGbTrunFroPathTot(k) -> float`: This function fetches the file size from a path, converts it to GB, and truncates the result to five decimal places.

- `get_abs_name_of_this() -> Path`: This function returns the absolute name of the current module.

- `createFolds(ls: list) -> None`: This function creates multiple directories from a list of paths.

- `mkdirs(path: str) -> str`: This function creates a directory and any necessary intermediate directories.

- `file_exists(file_path: str) -> bool`: This function checks if a file exists at the specified path.

- `dir_exists(path: str) -> bool`: This function checks if a directory exists at the specified path.

- `file_size(path:str)`: This function returns the size of a file in bytes, if the path is a file, else it returns 0.

- `get_size(path: str) -> int`: This function calculates the size of a file or a directory in bytes.

- `get_total_size(folder_path: str) -> int`: This function calculates the total size of a directory and its subdirectories in bytes.

- `get_files(directory)`: This function returns a list of all files in a directory including the ones in its subdirectories.


For detailed information about each function, please refer to their respective documentation in the module.
## Read-Write Utilities

The `read_write_utils.py` module contains a variety of utility functions to assist with file I/O operations. If you need to perform read or write operations to files in your software, this utility can ease the process and shorten your codebase. Notably, it enables you to quickly write contents to a file, read contents from a file, or check if a string includes a file extension. 

Here are the primary functions:

1. **Write content to a file**
```python
read_write_utils.write_to_file(file_path: str, contents: any)
```
This function writes the provided contents to a file at the specified path. If the file doesn't exist, it will be created.

2. **Read content from a file**
```python
read_write_utils.read_from_file(file_path: str)
```
This function reads and returns the contents of a file at the specified file path.

3. **Check if a string has a file extension**
```python
read_write_utils.is_file_extension(obj: str)
```
This function checks whether a provided string includes a file extension and returns a boolean value accordingly.

4. **Read from or write to a file depending on the number of arguments**
```python
read_write_utils.determine_path_and_content(*args,**kwargs)
```
This function determines the file path and the contents based on the provided arguments. It can be used when you want to infer the operation (read/write) based on the kind and count of arguments.

5. **Create a file if it does not exist, then read from it**
```python
read_write_utils.create_and_read_file(file_path: str, contents: str)
```
This function attempts to open a file from its path. If the file doesn't exist, it creates the file, writes the provided contents to it, and then reads the file content back.

All the utility functions are designed to be easily incorporated into your code and have detailed docstrings explaining their usage. 

**Note**: All file paths need to be absolute paths, and the file operations are conducted with 'UTF-8' encoding. If a function is called with incorrect arguments, it will alert the user with an 'Too many arguments' or 'Missing file path or contents.' message.

Please refer to the `read_write_utils.py` source code for more details and to understand the inner workings of these utilities for optimal usage.
[]
## Thread Utilities

- **all_alive**: This method returns a dictionary indicating whether each thread is alive or not. The keys are the thread names, and the values are boolean.
- **all_thread_names**: This method returns the keys (names) of all threads in the dictionary.
- **get_last_result**: In the absence of a specific thread name, this method returns the result of the last thread in `thread_name_list`. If a thread name is specified, it first checks the validity of the name using `check_name` and then returns the result.
- **check_name**: This method checks if the provided thread name is present in existing threads.

## Time Utilities
- **get_time_stamp**: Returns the current timestamp in seconds.
- **get_milisecond_time_stamp**: Returns the current timestamp in milliseconds.
- **get_day**: Returns the current day of the week.
- **get_date**: Returns the current date in YYYY-MM-DD format.
- **save_last_time**: Saves the last timestamp to a file named 'last.txt'.
- **get_day_seconds**: Returns the number of seconds in a day.
- **get_week_seconds**: Returns the number of seconds in a week.
- **get_hour_seconds**: Returns the number of seconds in an hour.
- **get_minute_seconds**: Returns the number of seconds in a minute.
- **get_24_hr_start**: Returns the timestamp for the start of the current day.
- **create_timestamp**: Accepts a date string and military time string to create a timestamp.
## Time Utilities

`time_utils` is a module in `abstract_utilities` that provides functions to work with time stamps, get the current date and time, and manage chronological operations. 

Here is an example of a function provided in this module:

- `get_second()`: This function returns the value of one second as a float.

Additional functions in time utilities include:
- `get_time_stamp()`
- `get_milisecond_time_stamp()`
- `get_day()`
- `get_time()`
- `get_date()`
- `save_last_time()`
- `get_day_seconds()`
- `get_week_seconds()`
- `get_hour_seconds()`
- `get_minute_seconds()`
- `get_24_hr_start()`

Each function in the `time_utils` module provides a unique operation relating to time management in your programs.

## Type Utilities

`type_utils` is another utility module that provides type checking and conversion functionality. This module incorporates features such as determining the type of an object, checking if an object is of a certain type, and facilitating type conversion. This simplifies data handling across different data types and ensures consistent behavior.

Some mainstay functions within this module include:
- `is_iterable(obj: any) -> bool`
- `is_number(obj: any) -> bool`
- `is_str(obj: any) -> bool`
- `is_int(obj: any) -> bool`
- `is_float(obj: any) -> bool`
- `is_bool(obj: any) -> bool`
- `is_list(obj: any) -> bool`
- `is_tuple(obj: any) -> bool`
- `is_set(obj: any) -> bool`
- `is_dict(obj: any) -> bool`
- `is_frozenset(obj: any) -> bool`
- `is_bytearray(obj: any) -> bool`
- `is_bytes(obj: any) -> bool`
- `is_memoryview(obj: any) -> bool`
- `is_range(obj: any) -> bool`
- `is_enumerate(obj: any) -> bool`
- `is_zip(obj: any) -> bool`
- `is_filter(obj: any) -> bool`
- `is_map(obj: any) -> bool`
- `is_property(obj: any) -> bool`
- `is_slice(obj: any) -> bool`
- `is_super(obj: any) -> bool`
- `is_type(obj: any) -> bool`
- `is_Exception(obj: any) -> bool`
- `is_none(obj: any) -> bool`
- `is_str_convertible_dict(obj: any) -> bool`
- `is_dict_or_convertable(obj: any) -> bool`
- `dict_check_conversion(obj: any) -> Union[dict, any]`

These functions and more form the `type_utils` module, playing an integral part in ensuring type compatibility and facilitating data conversion.


## Type Utilities

The `type_utils.py` module encompasses numerous functions that help in identifying the type of data structures, converting strings to their appropriate data types, and checking if the data can be represented in a specific format. Here is a description of the functions available in this module.

##### is_iterable():
Determines whether the given object is iterable or not.

##### get_type(obj):
Determines the type of the given object and updates it accordingly.

##### is_number(obj):
Checks whether the given object can be represented as a number.

##### is_object(obj):
Checks whether the given object is of type 'object'.

##### is_str(obj):
Checks whether the given object is of type 'str'.

##### is_int(obj):
Checks whether the given object is of type 'int'.

##### is_float(obj):
Checks whether the given object is of type 'float'.

##### is_bool(obj):
Checks whether the given object is of type 'bool'.

The following functions check if the object is of respective data types (list, tuple, dictionary, frozenset, bytearray etc.)
- is_list(obj)
- is_tuple(obj)
- is_set(obj)
- is_dict(obj)
- is_frozenset(obj)
- is_bytearray(obj)
- is_bytes(obj)
- is_memoryview(obj)
- is_range(obj)
- is_enumerate(obj)
- is_zip(obj)
- is_filter(obj)
- is_map(obj)
- is_property(obj)
- is_slice(obj)
- is_super(obj)
- is_type(obj)
- is_Exception(obj)
- is_none(obj)

##### dict_check_conversion(obj):
Converts the given object to a dictionary if possible, otherwise returns the original object.

##### make_list(obj):
Converts the given object to a list if it's not already a list.

##### make_list_lower(ls):
Converts all string elements in a list to lowercase.

Please note to replace `obj` and `ls` with the object and list you want to analyze or manipulate, respectively.


