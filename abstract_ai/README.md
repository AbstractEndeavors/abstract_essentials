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

## Installation

Installation of `abstract_ai` is easy and straightforward. You just need to clone the repository and run the setup file:

1. Clone the repository:
```sh
git clone https://github.com/AbstractEndeavors/abstract_essentials/abstract_ai
```
2. Navigate to the cloned directory:
```sh
cd abstract_ai
```
3. Run the setup file:
```sh
python setup.py install
```

Please note that `abstract_ai` requires Python 3.6 or later.

## Getting Started

Here is a basic example of using `abstract_ai`:

```python
import os
from abstract_ai.api_calls import safe_send
request = "please convert the prompt data to chinese"
prompt_data = "hi welcome to abstract ai"
output = safe_send(prompt_data=prompt_data,request=request,model="gpt-4",title="test_prompt",completion_percentage=40,additional_responses=False,directory=os.getcwd())
print(output[0]["response"])
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

`api_call.py` facilitates communication with the OpenAI API for various tasks. The script provides functions for sending requests, handling responses, and managing tokens for efficient usage. Here's an overview of the key components and functionalities:

- `get_openai_key(key:str='OPENAI_API_KEY')`: Retrieves the OpenAI API key from the environment variables.
- `load_openai_key()`: Loads the OpenAI API key into the application for authentication, ensuring calls to the OpenAI API are authorized.
- `headers(content_type:str='application/json',api_key:str=get_openai_key())`: Constructs and returns the necessary headers for an API request. The default content type is set to 'application/json'.
- `post_request()`: Sends a generic POST request to the OpenAI API, useful for tasks that don't fit the mold of the more specialized requests.
- `hard_request()`: Designed for sending more robust or specific requests to the OpenAI API, it provides more control over parameters and headers.
- `quick_request()`: A lightweight and faster method for sending requests to the OpenAI API. It simplifies the process for tasks that don't require detailed configurations.
- `raw_data()`: This function allows users to send raw data directly to the specified OpenAI endpoint, providing maximum control over the data being sent.

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

