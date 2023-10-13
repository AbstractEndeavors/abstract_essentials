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

Here's how you can use the `api_calls.py` module in your Python application:

1. Import the necessary classes and functions:

   ```python
   from abstract_ai.api_calls import PromptManager, hard_request, quick_request
   ```

2. Create an instance of `PromptManager` to manage your API calls:

   ```python
   prompt_manager = PromptManager(
       prompt_data=None,
       request=None,
       instructions=None,
       model=None,
       # ... other configuration options
   )
   ```

3. Customize the `PromptManager` instance according to your requirements, including prompts, instructions, and response handling logic.

4. Use the `send_query` method to send API requests and handle responses:

   ```python
   responses = prompt_manager.send_query()
   ```

5. Optionally, you can use the `hard_request` and `quick_request` functions for direct API calls with simpler configurations.

## Classes and Functions

### PromptManager Class

The `PromptManager` class is the core of the `api_calls.py` module. It provides a flexible way to configure and manage API requests. Here are some of its important attributes and methods:

- `send_query`: Sends API requests based on the configured settings.
- `get_openai_key`: Retrieves the OpenAI API key from environment variables.
- `initialize`: Initializes the `PromptManager` instance.
- `get_instructions`: Retrieves instructions for API requests.
- `get_additional_response`: Determines additional responses based on input.
- `get_title`: Retrieves a title based on input.
- `get_notation`: Retrieves notation based on input.
- `get_suggestions`: Retrieves suggestions based on input.
- `get_abort`: Retrieves an abort signal based on input.
- `get_header`: Generates request headers for API calls.
- `load_openai_key`: Loads the OpenAI API key for authentication.
- `create_prompt_guide`: Creates a formatted communication for the current data chunk.
- `create_prompt`: Creates a prompt dictionary with specified values.

### hard_request Function

The `hard_request` function sends a hard request to the OpenAI API with the provided parameters. It is a simplified way to make API calls.

### quick_request Function

The `quick_request` function sends a quick request to the OpenAI API with simple configurations and prints the result. It is a convenient shortcut for quick API interactions.

## Examples

For detailed examples and usage scenarios, refer to the `examples` directory in this repository. You'll find practical code samples demonstrating how to use the `api_calls.py` module for various tasks.

## Contributing

If you'd like to contribute to the development of the `abstract_ai` module or report issues, please refer to the [Contributing Guidelines](CONTRIBUTING.md).

## License

This module is licensed under the [MIT License](LICENSE), which means you are free to use and modify it as per the terms of the license. Make sure to review the license file for complete details.

Feel free to use `api_calls.py` to enhance your interactions with OpenAI's GPT-3 model in your projects.
### 3. `endpoints.py`:

`endpoints.py` is a crucial utility module within the `abstract_ai` package. Its primary function is to manage and offer comprehensive information regarding tokens, models, and the associated endpoints of various AI utilities.

- `get_model_info()`: Extracts the inversed JSON dictionary for model data. The dictionary maps model names (as keys) to their respective token counts, helping users gauge the complexity and capacity of each model.
- `get_endpoint_info()`: Offers a concise JSON dictionary where each endpoint is linked to its affiliated model(s), streamlining the process of selecting the correct endpoint for a given model.
- `get_token_info()`: Procures an inverted JSON dictionary concerning token information. In this dictionary, the token counts serve as the keys, while the associated model names are the values, providing a reverse lookup mechanism for understanding model capacities.
- `get_token_js()`: Fetches a JSON dictionary detailing token and endpoint relations for multiple AI models, making it easier to understand the linkage between models and their respective tokens
- `default_endpoint()`: Determines and provides the default endpoint. This choice is based on the preset 'endpoint_selection' configuration within the module.
- `default_model()`: Supplies the default AI model as configured in the 'model_selection' setting. Useful for users who frequently rely on a specific model.
- `default_tokens()`: Offers the default token count setting, derived from the 'token_selection' configuration, ensuring consistent token allocations in the absence of specific instructions.
- `get_defaults()`: Gathers and presents a comprehensive dictionary outlining default settings for endpoints, models, and tokens. This function also provides flexibility by allowing users to input their preferences for endpoints, models, and tokens.
- `get_endpoint_defaults()`: Returns a dictionary detailing default configurations for endpoints. It encapsulates details for various functionalities, including audio transcriptions, translations, chat completions, embeddings, image operations, moderations, and in-depth model particulars.
### 4. `tokenization.py`

 view entire revision history to see all changes.Manages tokenization and related operations.

- `count_tokens(text:str)`: Counts the number of tokens in the given text.
- `tokens_to_characters(token_count:int, model:str=default_model())`: Converts token count into characters for the specified model.
- `characters_to_tokens(character_count:int, model:str=default_model())`: Converts character count into tokens for the specified model.
- `print_tokens(text:str, model:str=default_model())`: Prints the token count for the given text and the specified model.
- `tokens_fit(text:str, max_tokens:int=default_tokens(), model:str=default_model())`: Checks if the token count of the text fits within the specified maximum tokens for the given model.
- `fit_text_to_tokens(text:str, max_tokens:int=default_tokens(), model:str=default_model())`: Truncates the text to fit within the specified maximum tokens for the given model.

## Contact

Should you have any issues, suggestions or contributions, please feel free to create a new issue on our [Github repository](https://github.com/AbstractEndeavors/abstract_essentials/abstract_ai).

## License

`abstract_ai` is released under the [MIT License](https://opensource.org/licenses/MIT).


