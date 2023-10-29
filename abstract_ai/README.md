# Abstract AI

## Table of Contents
- [Introduction](#Introduction)
- [Installation](#Installation)
- [Getting Started](#Getting-Started)
- [Documentation](#Documentation)
- [Contact](#Contact)
- [License](#License)

## Introduction

`abstract_ai` is a Python module that provides a wide range of functionalities aimed at facilitating and enhancing interactions with AI. Developed by `putkoff`, it comprises several utility modules to help handle API responses, generate requests, manage tokenization, and deal with other related aspects.

The module is particularly focused on the OpenAI API and makes use of its functionalities, yet it is designed to be easily extended to other APIs as well.

![Screenshot from 2023-08-31 02-52-21](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/382ca375-3987-4c2b-b5a9-dde0f7102d15)


![image](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/1975b7f0-f4de-4a8c-8a41-f6a0fded55da)

---

## Installation of `abstract_ai`

To install `abstract_ai`, you can either use pip or manually set it up by cloning the repository:

### Using pip:

```sh
pip install abstract-ai
```

### Manual Installation:

1. Clone the specific `abstract_ai` directory from the repository:
    - Using the `svn` command:
      ```sh
      svn checkout https://github.com/AbstractEndeavors/abstract_essentials/trunk/abstract_ai
      ```
      (For Ubuntu users, install `svn` with: `sudo apt-get install subversion`)

    - OR using sparse checkout with git:
      ```sh
      git clone https://github.com/AbstractEndeavors/abstract_essentials.git
      cd abstract_essentials
      git config core.sparseCheckout true
      echo "abstract_ai/*" > .git/info/sparse-checkout
      git checkout main
      ```

    - OR use third-party tools like [DownGit](https://minhaskamal.github.io/DownGit/#/home) to download the directory.

    - OR manually navigate to each file in the directory via GitHub's web interface and click the "Download" button.

2. Navigate to the cloned/downloaded directory:
```sh
cd abstract_ai
```

3. Run the setup file:
```sh
python setup.py install
```

**Note**: `abstract_ai` requires Python 3.6 or later. Ensure you meet this requirement before proceeding with the installation.

---

## Getting Started

Here is a basic example of using `abstract_ai`:

```python
from abstract_ai.api_calls import PromptManager
request='''please write a python function that will chatgpt to build a python script from api responses.
1) the script needs to have features that allow the gpt module that is being queried to request the portion of code it needs to review
 - i.e. request a directory map
 - request a line of the function that it currently being created,
 - request a functon source_code
 - anything else that would be neccisary to complete this goal.
2) the script should inately allow for the module to edit the python script, meaning that it should maintain an api feedbackloop for the api to request and analyze a portions of the script.
3) the content for these requests need to be programatically attained from this code such that they can be sent back to the module in a subsequent prompt.
4) each eubsequent prompt to the module after a request has been made needs to contain the requested content AND enough context to have the module understand why it requested the content and what the goal is
5) the above has tenuously already started with this prompt
6) the script so far will accompany this prompt in "current data chunk"'''

prompt_data="""import openai
import os

openai.api_key = 'your-api-key'

def create_python_script(file_path, prompt):
    # Send initial prompt to GPT-3
    response = openai.Completion.create(engine='gpt-3', prompt=prompt, max_tokens=500)
    # Open the file for writing
    with open(file_path, 'w') as file:
        # Write GPT's response to file
        file.write(response.choices[0]['text'])

def request_directory_map(path):
        paths = {os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn}
        create_python_script('directory_map.py', f'Create a function that returns a map of a directory: {paths}')

def request_function_source_code(function_name):
        # Send the query to GPT-3
        response = openai.Completion.create(engine='gpt-3', prompt=f'Please write the source code for a function named {function_name}', max_tokens=500)
        # Save response as new Python script
        create_python_script(f'{function_name}.py', response.choices[0]['text'])
# Generate a script that maps a directory
request_directory_map('/path/to/directory')

# Generate a script for a specific function
request_function_source_code('my_custom_function')"""

output = PromptManager(request=request,prompt_data=prompt_data).send_query()

```

## Documentation

`abstract_ai` consists of the following Python files and their corresponding functionalities:

### 1. `response_handling.py`:

`response_handling.py` is a utility module designed to manage and process responses, typically in JSON format. The module allows users to save, aggregate, and retrieve conversations, generating unique titles if needed.  It also offers utility functions like generating unique titles, finding keys in nested dictionaries or lists, navigating complex nested JSON structures, and more.

- `save_response(js:dict, response:dict, title: str = str(get_time_stamp()))`: Saves the response JSON and generated text to a file.
- `find_keys(data, target_keys)`: Finds the values associated with the specified target keys in a nested dictionary or list.
- `print_it(string)`: Prints the input string and returns it.
- `aggregate_conversations(directory)`: Aggregates conversations from JSON files in the specified directory.
- `get_responses(path)`: Retrieves the aggregated conversations from JSON files.

### 2. `api_call.py`:

Sure, here's an exhaustive `readme.md` for the `api_calls.py` component of the `abstract_ai` module:

# `api_calls.py` - Abstract AI Module

`api_calls.py` is a component of the Abstract AI module, designed to facilitate API calls to OpenAI's GPT-3 model. This module is intended to simplify the interaction with the GPT-3 API and handle responses in a structured manner.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Classes and Functions](#classes-and-functions)
  - [PromptManager](#promptmanager-class)
  - [hard_request](#hard_request-function)
  - [quick_request](#quick_request-function)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

`api_calls.py` serves as a bridge between your application and the OpenAI GPT-3 API. It provides a convenient interface to send requests, manage responses, and control the behavior of the API calls. This module is highly customizable, allowing you to define prompts, instructions, and response handling logic.

## Installation

To use the `api_calls.py` module, you need to install the required dependencies and set up your OpenAI API key.

1. Install the required Python packages:

   ```bash
   pip install openai
   ```

2. Set your OpenAI API key as an environment variable. By default, the module looks for an environment variable named `OPENAI_API_KEY` to authenticate API calls.

## Usage

Based on the provided notes, here's a README for the `abstract_ai` module:

---

# abstract_ai Module

The `abstract_ai` module is a sophisticated class management system designed to interact with the GPT model seamlessly. This module incorporates a variety of sub-modules and components to make the process of querying, interpreting, and managing responses from the GPT model streamlined.

## Main Components

- **GptManager**: Serves as the heart of the system and manages the interactions and flow between various components.
- **ApiManager**: Oversees the OpenAI API keys and headers.
- **ModelManager**: In charge of model selection and querying.
- **PromptManager**: Dedicated to generating and managing prompts.
- **InstructionManager**: Manages instructions for the GPT model.
- **ResponseManager**: Handles responses from the model.

## Dependencies

- **abstract_webtools**: Offers tools for handling web-related tasks.
- **abstract_gui**: Contains GUI-related tools and components.
- **abstract_utilities**: Encompasses utility functions and classes for general operations.
- **abstract_ai_gui_layout**: Provides the layout for the AI GUI.

## Usage

1. Begin by initializing the `GptManager` class.
2. Utilize the update methods to set or modify configurations.
3. Call `get_query()` to query the GPT model and obtain a response.

---

### Detailed Components Documentation

#### ModelManager

Class used for managing the models by the communication system.

- **Attributes**:
  - `all_models`: A list of all available models with their attributes.
  - `all_model_names`: Names of the available models.
  - `all_endpoints`: Endpoints of the available models.
  - `default_model_info`: Default model info used if no specific model is chosen.
  - `models_get_info_endpoint`: The API endpoint for retrieving model information.
  - `selected_model_name`: The name of the chosen model.
  - `selected_endpoint`: Endpoint of the chosen model.
  - `selected_max_tokens`: Maximum number of tokens usable by the chosen model.

#### InstructionManager

Manages instructions for communication with the ChatGPT model.

- **Methods**:
  - `__init__()`: Initializes the InstructionManager with parameters guiding the interaction.
  - `get_additional_responses()`: Interprets the 'additional_responses' value.
  - `get_generate_title()`: Determines the 'generate_title' value.
  - ... [Other methods as per the provided details]

#### PromptManager

Manages prompts and their processing. 

- **Description**: Contains functionality for constructing prompts based on chunk type, model manager, etc. It calculates token distribution among prompts, completions, and chunks.

- **Methods**:
  - `calculate_token_distribution()`: Determines token distribution between prompts, completions, and chunks.
  - `count_tokens()`: Counts the number of tokens in a given text.
  - ... [Other methods as per the provided details]

---

### Additional Information

- **Author**: putkoff
- **Date**: 05/31/2023
- **Version**: 1.0.0

---

This README gives an overview of the `abstract_ai` module and breaks down its main components, dependencies, and usage. The "Detailed Components Documentation" section provides a deeper dive into some of the main classes and their functionalities.
## Contact

Should you have any issues, suggestions or contributions, please feel free to create a new issue on our [Github repository](https://github.com/AbstractEndeavors/abstract_essentials/abstract_ai).

## License

`abstract_ai` is released under the [MIT License](https://opensource.org/licenses/MIT).


