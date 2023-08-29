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

### Abstract Gui
Advanced management for PySimpleGUI windows and events. 
- **Key Classes**: `WindowGlobalBridge`, `WindowManager`
- **Features**:
  - [Brief description of notable features.]
  - ...

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

#### **Classes**:

- ##### `TLSAdapter(HTTPAdapter: int)`
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
**Author**: putkoff
**Author Email**: partners@abstractendeavors.com
**Github**: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_webtools
**PYPI**: https://pypi.org/project/abstract-webtools
**Part of**: abstract_essentials
**Date**: 08/29/2023
**Version**: 0.1.2
---

