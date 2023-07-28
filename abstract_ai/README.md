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
from abstract_ai.response_handling import save_response, find_keys
from abstract_ai.api_call import hard_request, load_openai_key

load_openai_key()
prompt = "Translate the following English text to French: '{}'"
response = hard_request(prompt.format("Hello World"))
save_response({"prompt": prompt}, response)
```

## Documentation

`abstract_ai` consists of the following Python files and their corresponding functionalities:

### 1. `response_handling.py`:

Handles API responses and provides additional functionalities.

- `save_response(js:dict, response:dict, title: str = str(get_time_stamp()))`: Saves the response JSON and generated text to a file.
- `find_keys(data, target_keys)`: Finds the values associated with the specified target keys in a nested dictionary or list.
- `print_it(string)`: Prints the input string and returns it.
- `aggregate_conversations(directory)`: Aggregates conversations from JSON files in the specified directory.
- `get_responses(path)`: Retrieves the aggregated conversations from JSON files.

### 2. `api_call.py`:

Facilitates API calls to OpenAI.

- `get_openai_key(key:str='OPENAI_API_KEY')`: Retrieves the OpenAI API key from the environment variables.
- `load_openai_key()`: Loads the OpenAI API key for authentication.
- `headers(content_type:str='application/json',api_key:str=get_openai_key())`: Returns the headers for the API request.
- `post_request()`: Sends a POST request to the OpenAI API.
- `hard_request()`: Sends a hard request to the OpenAI API.
- `quick_request()`: Sends a quick request to the OpenAI API.
- `raw_data()`: Sends a raw data request to the specified endpoint with the provided parameters.

### 3. `endpoints.py`:

Manages endpoints and associated information.

- `get_model_info()`: Retrieves the inverted JSON dictionary of model information.
- `get_endpoint_info()`: Retrieves the JSON dictionary containing endpoint information.
- `get_token_info()`: Retrieves the inverted JSON dictionary of token information.
- `default_endpoint()`: Returns the default endpoint.
- `default_model()`: Returns the default model.
- `default_tokens()`: Returns the default number of tokens.
- `get_defaults()`: Returns a dictionary containing the default values for endpoint, model, and tokens.

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

