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
# abstract_essentials Package Overview

Welcome to the `abstract_essentials` package! This package is an amalgamation of modules that provides you with a wide range of utilities to streamline your Python development tasks. Whether it's handling environment variables, converting speech to text, or managing Python modules, `abstract_essentials` has got you covered. Below is a concise overview of each module included in the package:

## Modules:

### 1. **Abstract Security**

- A streamlined solution for managing and accessing environment variables within .env files. Its primary feature is the ability to search through multiple directories, ensuring the efficient retrieval of environment variables.

### 2. **Abstract Audio**

- A Speech to Text module that captures and transforms audio input from a microphone into text, subsequently saving it to a file. It showcases an abstract GUI to visualize audio recording and playback statuses.

### 3. **Abstract Modules**

- A utility set focusing on simplifying Python module management. This includes creating, packaging, and distributing modules. Notably, it offers functionalities to upload Python modules to PyPI and manage the module's version number.

### 4. **Abstract Ai**

- Serving as an interface between your Python code and the OpenAI API, this module streamlines the process of sending requests and handling responses. It's built to remove the intricacies of the interaction, letting developers concentrate on meaningful queries and the relevant results.

### 5. **Abstract GUI**

- Aimed at simplifying the management of global variables and windows in PySimpleGUI applications, `abstract_gui.py` offers utility classes and functions that ease the creation and manipulation of PySimpleGUI windows.

### 6. **Abstract Images**

- A segment of the `abstract_essentials` package dedicated to image and PDF utilities. It comes packed with functions to load/save images, extract text from images, take screenshots, process PDFs, and more.

### 7. **Abstract Utilities**

- A collection of diverse utility modules designed to assist in various tasks. This encompasses data comparison, list manipulation, JSON operations, string tasks, mathematical calculations, and time operations. Each module is extensively documented to ensure clarity and ease of use.

### 8. **Abstract WebTools**

- A robust toolkit built for web content parsing and inspection. It boasts enhanced features like React component detection and URL utilities, making it indispensable for developers, analysts, and cybersecurity experts alike.

---

Thank you for exploring the `abstract_essentials` package. Dive into each module's documentation to fully grasp its capabilities and understand its applications. Your journey towards efficient Python programming starts here!

## Installation

[Instructions on how to install the package, perhaps with pip or another package manager.]

```
pip install abstract_essentials
```

## Modules
---
### Abstract Security

Abstract Security offers a streamlined solution to managing and accessing environment variables within `.env` files. Its standout feature is the unparalleled ability to search through multiple directories, ensuring accurate and efficient retrieval of environment variables.

- **Key Features**:
  - Simplified access and management of environment variables from `.env` files.
  - Unique search capability across multiple directories to locate and fetch the right environment variables.
### Abstract Security
Manages and accesses environment variables in `.env` files, with a unique search capability across multiple directories.
- **Features**:
  - [Brief description of notable features.]
  - ...

**Description:**  
Abstract Security simplifies the management and access of environment variables stored in `.env` files. Its key feature is the ability to search multiple directories for these files, ensuring you always fetch the right environment variables with minimal hassle.

## Installation

for now, please install the individual modules seperately.

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
---

### Abstract Audio

**Description:**  
The Speech to Text module enables the capture and manipulation of audio input from a microphone, converting it into text and saving it into a file. This module employs an abstract graphical user interface (GUI) to display the audio recording and playback status.


## Installation

```
pip install abstract_audio
```

**Dependencies**:
- `os`
- `speech_recognition` (as `sr`)
- `abstract_utilities` (specifically, functions from `read_write_utils`, `cmd_utils`, and `thread_utils`)
- `abstract_gui`

### Features

- **Audio Conversion**: Seamlessly converts live audio input from a microphone into text, enhancing user accessibility and usability.
- **Integrated GUI**: Provides an intuitive abstract graphical user interface that displays audio recording and playback status, enabling effortless user interaction.
- **Microphone Management**: Comprehensive features to toggle, parse, and retrieve the current state of the microphone, ensuring optimal voice capture.
- **Real-time GUI Updates**: Dynamically updates the GUI window based on recording status, parsed text, and other key events, ensuring immediate feedback to the user.
- **Speech Recognition**: Employs sophisticated mechanisms such as adjusting for ambient noise and utilizes the Google Web Speech API for efficient and accurate voice-to-text conversion.
- **Customizable GUI Layout**: Offers the ability to define the layout of the PySimpleGUI window, catering to diverse user interface preferences.
- **Event-Driven Actions**: Effectively handles multiple GUI window events, performing corresponding actions and ensuring smooth user experience.
- **Easy Execution**: Simple script execution opens up a GUI window with clear indicators and buttons, allowing users to quickly start and view audio recordings.


### **Functions**:

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

To use this script, execute it as a Python program. It will open a GUI window with a 'record' button. Clicking on the 'record' button will initiate audio recording, and the GUI screen will turn green to indicate recording. Once you stop speaking, the recorded audio will be processed using the Google Web Speech API, and the recognized text will be displayed in the GUI window.

Note: Ensure that the required libraries are installed, including `abstract_utilities`, `abstract_gui`, and `speech_recognition`.
hical user interface (GUI) to display the audio recording and playback status.


---

## Abstract Modules

This package provides a set of utilities to make Python module management easier, with a particular focus on the creation, packaging, and distribution of modules. Its key features include the upload of Python modules to PyPI and the management of the module's version number.

Abstract Modules is composed of three components: upload_utils.py, module_utils.py, and create_module_folder.py



## Installation

```
pip install abstract-modules
```


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


## Abstract Ai

The `abstract_ai` module is a key component of the `abstract_ai` submodule within the larger `abstract_essentials` package. Designed to streamline the process of making API calls to OpenAI, handling responses, and managing communication intricacies, this module offers a suite of functions that empower developers to interact with the OpenAI API efficiently and effectively.

### Description

The module serves as a bridge between your Python code and the OpenAI API, providing a structured interface for sending requests, managing responses, and handling various scenarios that might arise during the interaction. It abstracts away many of the technical complexities, enabling developers to focus on crafting meaningful requests and interpreting the corresponding responses.

## Installation

To install abstract_ai, use pip:

```
pip install abstract-ai
```

### Key Features

## Features

- **API Key Management**: The module includes functions to fetch and load the OpenAI API key from environment variables, ensuring secure authentication for API interactions.
- **Flexible Request Handling**: The `post_request()` function allows sending POST requests to a specified endpoint with customizable headers and prompt data, offering flexibility in crafting API requests.
- **Structured Communication**: The module facilitates chunked data communication with the OpenAI API, enabling structured exchanges for complex tasks by breaking down data into manageable chunks.
- **Response Handling**: The module provides functions to process and handle API responses, converting them into Python dictionaries for easier interpretation and manipulation.
- **Safety Checks**: The `safe_send()` function offers a safe method to send API requests, adhering to token limitations and handling scenarios where responses may exceed token allowances.
- **Convenient Prompt Creation**: Functions like `create_prompt_js()` allow for the creation of well-formatted prompt JSON objects, simplifying the construction of requests and improving readability.
- **User-Friendly GUI**: The module integrates with a graphical user interface (GUI) to handle aborted requests, ensuring a smooth user experience and providing a clear interface for handling unexpected scenarios.
- **Customizable Response Template**: The `default_instructions()` function generates a standardized response format template in JSON, allowing users to easily structure their responses with notes, suggestions, and more.
- **Documentation and Source Link**: The module provides information about the version, author, and source code location. A link to the GitHub repository offers comprehensive documentation and source code for reference.
- **Integration with Dependencies**: The module collaborates seamlessly with dependent modules such as `abstract_utilities`, `abstract_gui`, and others, streamlining the development process and enhancing functionality.

These key features empower users to interact with the OpenAI API efficiently, handle diverse response scenarios, and manage complex communication processes through a well-structured and organized interface.

### Dependencies

To leverage the capabilities of the `abstract_ai` module, ensure that the required dependencies are installed. 
- `requests` library for making HTTP requests
- `openai` library for interacting with OpenAI's API
- `abstract_utilities` for submodule integration
- `abstract_gui` for additional utilities and GUI handling.

Incorporating this module into your codebase can significantly simplify the process of interacting with the OpenAI API, allowing you to focus on the creative aspects of your project while the module takes care of the technical details.


### Example Use

The module's functions can be utilized for various tasks, such as sending different types of requests, handling complex queries, and managing responses. A typical use case might involve fetching data from an external source using the OpenAI API, processing the response, and presenting the results to the user.

Here's an example of how you can use the functions provided by the `api_calls.py` module to interact with the OpenAI API and handle responses effectively:

```python
# Import necessary functions and modules from abstract_ai
from abstract_ai.api_calls import safe_send, quick_request

# Define your OpenAI API key or ensure it's set in the environment variables; the abstract_security module required for this module will automatically search for the .env in the current directory, and home/envy_all diretory

# send a prompt to gpt-4
request = "please convert the prompt data to chinese"
prompt_data = "hi welcome to abstract ai"
model="gpt-4"
output = safe_send(prompt_data=prompt_data,request=request,model=model,title="test_prompt",completion_percentage=40)
print(output[0]["response"])

#example with no inputs at all
response = safe_send()
print("API Response:", response)
# query sent to the module: {'prompt': {'available': 0, 'used': 210, 'desired': 4916}, 'completion': {'available': 3276, 'used': 0, 'desired': 3276}, 'chunks': {'total': 1, 'length_per': 4706, 'data': ["I have not sent anything . How 's your day though?"]}}
#response= [{'abort': 'False', 'additional_response': 'False', 'suggestions': 'This is a conversational prompt instead of a task-based one. It might be useful to keep the conversation going or redirect the user to how you can assist them.', 'notation': 'The user has not made a request but initiated a conversation instead.', 'response': "I'm an AI and don't experience days, but thank you for asking! How can I assist you today?"}]

# Example API call using post_request function
endpoint_url = "https://api.openai.com/v1/your-endpoint"
prompt_data = "Translate the following English text to French: 'Hello, world!'"
response = post_request(endpoint=endpoint_url, prompt=prompt_data)
print("API Response:", response)

# Example of sending a quick request
quick_request(prompt="Sum the numbers: 5, 10, 15")
# This function will quickly send the request and print the API response

# Example of using safe_send function
complex_prompt = "Perform a sentiment analysis on the following paragraph: 'The product is great, but the customer service needs improvement.'"
response_list = safe_send(prompt_data=complex_prompt, max_tokens=50)
for idx, resp in enumerate(response_list, start=1):
    print(f"Response {idx}:", resp["response"])
```

In this example, you can see how to make API calls, handle responses, and utilize different functions provided by the `abstract_ai` module. You can adapt these functions to your specific use case, allowing you to interact with the OpenAI API efficiently and manage responses in a structured manner. Remember to replace placeholders like `your-endpoint` and actual API keys with appropriate values before executing the code.
---

# Abstract GUI

`abstract_gui.py` is a module designed to simplify the handling and management of global variables and windows in PySimpleGUI applications. It provides a suite of utility classes and functions that makes creating and interacting with PySimpleGUI windows a breeze.

## Features

- **Manage Global Variables**: Share and manage global variables across different scripts with the `WindowGlobalBridge` class.
- **Manage Windows**: Seamlessly create and manage multiple PySimpleGUI windows with the `WindowManager` class.
- **Layout Utilities**: Easily create and concatenate layouts with functions like `create_row`, `create_column`, `concatenate_rows`, and more.
- **Quick Window Generation**: Generate commonly used window layouts for browsers, Yes/No prompts, and input dialogs without the need for complex setup.
- **Expandability**: Create expandable PySimpleGUI windows with ease using the `expandable` function.
Sure, here's a "Description" section based on the docstrings you provided:

## Installation

To install abstract_gui, use pip:

```
pip install abstract-gui
```

## Description

### WindowGlobalBridge

The **WindowGlobalBridge** class serves as a centralized storage system for managing global variables that are shared across different scripts. This functionality ensures that there's a consistent state of variables even when shared between multiple scripts.

- **Attributes**:
  - `global_vars`: A dictionary where global variables for each script are stored.
- **Key Methods**:
  - `retrieve_global_variables`: Stores the global variables of a script in the global_vars dictionary.
  - `return_global_variables`: Fetches the global variables of a specific script.
  - `change_globals`: Alters a global variable value for a specified script.
  - `return_global_value`: Fetches the value of a particular global variable in a script.

### WindowManager

The **WindowManager** class acts as a comprehensive manager for PySimpleGUI windows, ensuring that the creation, handling, and destruction of GUI windows are streamlined and simplified.

- **Attributes**:
  - `all_windows`: Dictionary storing registered windows and their details.
  - `last_window`: Name of the last accessed window.
  - `script_name`: Name of the script currently utilizing the WindowManager.
  - `global_bridge`: Bridge for accessing shared variables across different scripts.
  - `global_vars`: Dictionary containing global variables specific to this script.
- **Key Methods**:
  - `win_closed`: Determines if a particular event corresponds to the closure of a window.
  - `verify_window`: Checks the validity of a PySimpleGUI window.
  - `read_window`: Extracts event and value data from a given window and updates the manager's state.
  - `get_all_windows`: Returns a dictionary of all registered windows.
  - `create_window_name`: Generates unique names for new windows.
  - `get_new_window`: Facilitates the creation of a new window with customizable features.

### Utility Functions

These utility functions are crafted to refine and simplify the process of establishing and overseeing PySimpleGUI windows and their layouts. Their primary aim is to allow for a more concise and readable codebase when setting up GUIs.

- **`ensure_nested_list`**: Verifies and converts an object into a nested list if necessary.
- **`create_row` & `create_column`**: Forms rows and columns from passed arguments respectively.
- **`concatenate_rows` & `concatenate_layouts`**: Joins lists together.
- **`get_buttons`**: Produces a list of button components based on varying input types.
- **`while_quick`**: A utility to streamline the window event loop.
- **`verify_args`**: Validates default values for various window arguments.
- **`get_window` & `get_browser_layout`**: Retrieves and prepares layouts for specific window types.
- **`out_of_bounds`**: Checks value boundaries.
- **`det_bool_F` & `det_bool_T`**: Determines boolean representation of an object.
- **`get_gui_fun`**: Fetches a PySimpleGUI function by its name and pre-configures it with given arguments.
- **`create_window_manager`**: Constructs a window manager for PySimpleGUI windows oversight.

These tools, combined, provide a robust framework for developing and managing GUIs, allowing developers to focus on their primary tasks without delving into the intricacies of window management.

## Dependencies

To ensure smooth functionality, the following modules and packages are required:

- **PySimpleGUI**: A simple way to create GUIs.
- **abstract_utilities**: A utility package containing various helpful modules:
  - **thread_utils**: 
    - `thread_alive`: Checks if a thread is alive.
  - **class_utils**: 
    - `get_fun`: Retrieves a specific function (or other callable) from a class.
  - **path_utils**: 
    - `get_current_path`: Obtains the current working directory or path of the script.
  - **list_utils**: 
    - `ensure_nested_list`: Ensures a list is nested.
    - `make_list_add`: Adds elements to a list.
  - **math_utils**: 
    - `out_of_bounds`: Checks if a value is out of specified bounds.

Make sure to have all these dependencies installed to avoid any runtime errors.

## Usage

Here's a simple example showcasing some of the functionalities:

```python
import abstract_gui

# Initialize the window manager and global bridge
window_mgr, bridge, script_name = abstract_gui.create_window_manager(script_name="example_script", global_var=globals())

# Create a simple layout using the utility function
layout = abstract_gui.get_gui_fun('Text', args={"text": "Hello, PySimpleGUI!"})

# Create an expandable PySimpleGUI window
expand = abstract_gui.expandable()
window = window_mgr.get_new_window(title="Example Window", args={"layout":[[layout]], **expand})

# Run the event loop for the window
window_mgr.while_basic(window)
```

For more detailed usage, including parameter information and return types, refer to the source code and individual method documentation.

Thank you for considering `abstract_gui` for your PySimpleGUI applications!
---
---
# Abstract Images

`abstract_images` is part of the abstract_essentials package, provides a collection of utility functions for working with images and PDFs, including loading and saving images, extracting text from images, capturing screenshots, processing PDFs, and more.


## Features
- Read and manipulate PDF files.
- Convert PDF pages to images.
- Extract text from images.
- Split PDF files into individual pages.
- Merge multiple PDF files into a single PDF.
- Get information about PDF files such as the number of pages.
- Open PDF files using the default associated program.


## Installation

To install abstract_modules, use pip:

```
pip install abstract-images
```

## Description

The "abstract_images" module provides a set of functions to work with PDF files, convert PDF pages to images, and extract text from images. It also offers functionalities to split PDF files into individual pages, merge multiple PDF files into a single PDF, and get information about PDF files. Additionally, the module includes an "image_utils.py" module that provides various utility functions for working with images, including resizing, format conversion, and pixel data extraction.

## Dependencies

The following dependencies are required for the proper functioning of `abstract_images`:

**Dependencies:**
- PyPDF2: A library for reading and manipulating PDF files.
- pdf2image: A library for converting PDF pages to images.
- OpenCV: A library for computer vision tasks.
- pytesseract: A library for optical character recognition.
- numpy: A library for numerical computations.
- Pillow (PIL): A library for image processing.
- pyscreenshot: A library for taking screenshots.
- abstract_webtools: A module for web-related utility functions.
- abstract_utilities: A library for basic tools needed in most any script.

Make sure to have all these dependencies installed to avoid any runtime errors.

**Example Usage:**

```python
from abstract_images import (
    split_pdf, pdf_to_img_list, img_to_txt_list, open_pdf_file,
    get_pdfs_in_directory, get_all_pdf_in_directory, collate_pdfs
)

# Split a PDF into separate pages
pdf_path = "input.pdf"
split_pdf(pdf_path, output_folder="output_folder")

# Convert PDF pages to images
pdf_list = ["page1.pdf", "page2.pdf"]
pdf_to_img_list(pdf_list, output_folder="output_images")

# Convert images to text
img_list = ["image1.png", "image2.png"]
img_to_txt_list(img_list, output_folder="output_texts")

# Open a PDF file using the default program
pdf_file_path = "document.pdf"
open_pdf_file(pdf_file_path)

# Get a list of PDF filenames in a directory
pdf_directory = "pdfs_directory"
pdf_filenames = get_pdfs_in_directory(pdf_directory)

# Get a list of complete paths to PDF files in a directory
pdf_paths = get_all_pdf_in_directory(pdf_directory)

# Merge multiple PDF files into a single PDF
pdfs_to_merge = ["file1.pdf", "file2.pdf"]
merged_pdf_path = "merged.pdf"
collate_pdfs(pdfs_to_merge, merged_pdf_path)

# Resizing images
image_path = "image.jpg"
resized_data = resize_image(image_path, max_width=100, max_height=150)
with open('resized_image.png', 'wb') as file:
    file.write(resized_data)

# Convert image to text using Tesseract OCR
text = image_to_text("image.png")
print(text)

# Save an image in different format
original_image = read_image("original.jpg")
save_image(original_image, "converted.png", format="PNG")
```

For more detailed usage, including parameter information and return types, refer to the source code and individual method documentation.

Thank you for considering `abstract_images` for your interest in Abstract Images!
---

# Abstract Utilities

## Introduction

This Python package is a collection of utility modules providing a variety of functions to aid in tasks such as data comparison, list manipulation, JSON handling, string manipulation, mathematical computations, and time operations. The package includes the following modules:

- compare_utils.py
- collator_utils.py
- class_utils.py
- type_utils.py
- list_utils.py
- string_clean.py
- json_utils.py
- read_write_utils.py
- math_utils.py
- time_utils.py
- main.py

Each module includes a suite of functions which are thoroughly documented within their docstrings, including purpose, input parameters, and return values.

## Modules Overview

### compare_utils.py

This module provides utility functions for comparing strings and objects. It offers functions for calculating string similarity and comparing object lengths.

### collator_utils.py

[TODO: Add brief module overview here]

### class_utils.py

This module contains utility functions for dealing with classes, objects, and modules. It offers functions to manipulate global variables, fetch and check object types and their membership in a module, inspect function signatures, call functions with supplied arguments, convert layouts to components, and retrieve directory of a module.

### type_utils.py

This module provides utility functions for working with data types. It includes a variety of type checking and conversion functions, from simple checks like `is_str` or `is_int`, to more specific ones like `is_frozenset` or `is_memoryview`.

### list_utils.py

This module contains utility functions for operating on lists. It includes functions like `get_sort`, which sorts a list in ascending order and returns the element at a given index, and `combineList`, which combines two lists into one.

### string_clean.py

This module provides functions for cleaning and manipulating strings. Functions include `quoteIt`, which quotes specific elements in a string, and `eatInner`, `eatOuter`, and `eatAll`, which remove characters from various parts of a string or list. 

### json_utils.py

This module provides functions for handling JSON data. It offers functionalities like converting JSON strings to dictionaries, merging dictionaries, updating and removing keys, loading and saving JSON files, retrieving keys, values, and specific items from dictionaries, and recursively displaying values of nested JSON data structures with indentation.

### read_write_utils.py

This module provides utility functions for reading and writing to files. Functions include write content to a file, read content from a file, check if a string has a file extension, read from or write to a file depending on the number of arguments, create a file if it does not exist, then read from it, create a json file if it does not exist, then read from it.

### math_utils.py

This module contains utility functions related to mathematical operations. 

### time_utils.py

This module provides utility functions for working with timestamps and time-related operations. It includes functions that return the current timestamp in seconds or milliseconds, the current day of the week, the current time, the current date, and functions to calculate the number of seconds in various time intervals.

## Installation

For local use, navigate to the root directory of the project where `setup.py` resides and install the package locally in editable mode with `pip` by running:

```bash
pip install -e .
```

## Usage

Import the modules and use the functions in your Python scripts:

```python
from abstract_utilities import type_utils

print(type_utils.is_str("hello"))
```

Please make sure to replace "abstract_utilities" and "type_utils" with the actual names of your package and module. Changes to the modules will be reflected the next time you import them, without needing to reinstall the package.
---

# Abstract WebTools

Abstract WebTools is a comprehensive utility toolkit designed for parsing and inspecting web content. With enhanced capabilities, such as React component detection and URL utilities, it's a must-have for developers, analysts, and cybersecurity professionals.

## Features

- **URL Validation**: Tackle issues with URL accuracy and automatically test multiple URL variations.
- **HTTP Request Manager**: Advanced handling of HTTP requests, tailored user-agent strings, and optimized TLS security with a specialized adapter.
- **Source Code Acquisition**: A simple way to access the source code of websites.
- **React Component Parsing**: Identify and extract JavaScript and JSX source code from websites.
- **Comprehensive Link Extraction**: Easily gather all internal links from a website.
- **Web Content Analysis**: In-depth content analysis, including HTML elements, attributes, and class names.

## Description

Abstract WebTools provides an all-in-one solution for web content analysis. Its URL analyzer ensures that URLs are valid and even attempts different variations to achieve correct website access. The toolkit's unique HTTP request system allows for specific user-agent customization and introduces heightened security with its dedicated TLS adapter. Beyond these, Abstract WebTools is equipped to extract a plethora of information, ranging from source code to React components. With the ability to also pull all internal links from a website and a suite of tools for content analysis, this toolkit is a valuable asset for many professionals in the digital realm.

## Dependencies

To run Abstract WebTools smoothly, you will need the following packages:

- `requests`
- `ssl`
- `HTTPAdapter` from `requests.adapters`
- `PoolManager` from `urllib3.poolmanager`
- `ssl_` from `urllib3.util`
- `urlparse`, `urljoin` from `urllib.parse`
- `BeautifulSoup` from `bs4`

## Usage

### Get Status Code

Fetch the status code of a given URL with `get_status`.

```python
from abstract_webtools import clean_url

urls = clean_url('https://example.com')
print(urls)  # Outputs: ['https://example.com', 'http://example.com']
```

### Try Request

Make HTTP requests using `try_request` and receive responses.

```python
from abstract_webtools import try_request

response = try_request('https://www.example.com')
print(response)  # Outputs: <Response [200]>
```

### Is Valid URL

Check the validity of a URL with `is_valid`.

```python
from abstract_webtools import is_valid

valid = is_valid('https://www.example.com')
print(valid)  # Outputs: True
```

### Get Source Code

Retrieve the source code of a given URL with `get_Source_code`.

```python
from abstract_webtools import get_Source_code

source_code = get_Source_code('https://www.example.com')
print(source_code)  # Outputs: HTML source code of the URL
```

### Parse React Source

Extract React components using `parse_react_source`.

```python
from abstract_webtools import parse_react_source

react_code = parse_react_source('https://www.example.com')
print(react_code)  # Outputs: List of JavaScript and JSX source code within <script> tags
```

### Get All Website Links

Gather all internal links from a website with `get_all_website_links`.

```python
from abstract_webtools import get_all_website_links

links = get_all_website_links('https://www.example.com')
print(links)  # Outputs: List of URLs on the same website as the given URL
```

### Parse All

For an in-depth content analysis, use `parse_all`.

```python
from abstract_webtools import parse_all

HTML_components = parse_all('https://www.example.com')
print(HTML_components["element_types"])       # Outputs: List of HTML element types
print(HTML_components["attribute_values"])    # Outputs: List of attribute values
print(HTML_components["attribute_names"])     # Outputs: List of attribute names
print(HTML_components["class_names"])         # Outputs: List of class names
```

### Extract Elements

Isolate specific HTML elements using `extract_elements`.

```python
from abstract_webtools import extract_elements

elements = extract_elements('https://www.example.com', element_type='div', attribute_name='class', class_name='container')
print(elements)  # Outputs: List of HTML elements fitting the filters
```

---

Harness the power of Abstract WebTools and streamline your web content analysis today!

#### Module Information
- **Author**: putkoff
- **Author Email**: partners@abstractendeavors.com
- **Github**: https://github.com/AbstractEndeavors/abstract_essentials
- **PYPI**: [https://pypi.org/user/putkoff/](https://pypi.org/user/putkoff/)
- **Part of**: abstract_essentials
- **Date**: 08/29/2023
- **Version**: 0.1.2
---

