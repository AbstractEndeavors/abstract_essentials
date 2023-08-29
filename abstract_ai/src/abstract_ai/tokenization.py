"""
tokenization.py
=====================
This module is part of the `abstract_ai` module of the `abstract_essentials` package. It primarily handles the task of tokenization and chunking of text data. The utilities present in this module are essential for effectively managing the token constraints set by the OpenAI API and optimizing the request structure.

Functions:
----------

### `count_tokens(text: str) -> int`

- **Description**: Counts the number of tokens in the given text using word tokenization.
- **Arguments**:
  - `text` (str): The input text.
- **Returns**: The number of tokens in the text.

### `convert_to_percentage(number: float) -> float`

- **Description**: Converts a number to its percentage if greater than one; otherwise, returns the original number.
- **Arguments**:
  - `number` (float): The number to be converted.
- **Returns**: The percentage value of the number if greater than one, otherwise the original number.

### `create_chunks(content: str, size_per_chunk: int) -> list`

- **Description**: Divides the content into chunks of specified size and returns a list of these chunks.
- **Arguments**:
  - `content` (str): The content to be chunked.
  - `size_per_chunk` (int): The desired size per chunk.
- **Returns**: A list of content chunks.

### `calculate_token_distribution(max_tokens: int = default_tokens(), prompt: str = "null", completion_percentage: float = 40, size_per_chunk: int = None, chunk_prompt: str = "", tokenize_js: dict = {}) -> dict`

- **Description**: Calculates the token distribution between prompts, completions, and chunks to ensure effective token utilization.
- **Arguments**:
  - `max_tokens` (int, optional): The maximum number of tokens allowed. Defaults to `default_tokens()`.
  - `prompt` (str, optional): The prompt to be used. Defaults to "null".
  - `completion_percentage` (float, optional): The completion percentage. Defaults to 40.
  - `size_per_chunk` (int, optional): The size per chunk. Defaults to None.
  - `chunk_prompt` (str, optional): The chunk prompt. Defaults to an empty string.
  - `tokenize_js` (dict, optional): Tokenization data. Defaults to an empty dictionary.
- **Returns**: A dictionary containing token distribution information.

Notes:
------
The module leverages the nltk library for tokenization. Ensure nltk is properly installed and set up. Additionally, the module provides various utilities that closely work with the OpenAI's token constraints. When working with large text, the module ensures that the text is properly segmented to fit within the API's limits.

About abstract_ai
--------------------
part of: abstract_ai
Version: 0.1.7.1
Author: putkoff
Contact: partners@abstractendeavors.com
Content Type: text/markdown
Source and Documentation:
For the source code, documentation, and more details, visit the official GitHub repository.
github: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai

Notes:
------
For optimal performance, it's important to understand the token limits imposed by OpenAI and adjust the configuration settings in the module accordingly. As OpenAI's API evolves, these constraints might change, so always keep an eye on their official documentation.
"""
from nltk.tokenize import word_tokenize
from .endpoints import default_tokens
def count_tokens(text):
    """
    Counts the number of tokens in the given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of tokens.
    """
    return len(word_tokenize(text))

def convert_to_percentage(number):
    """
    Converts a number to its percentage if greater than one; otherwise, returns the original number.
    
    Args:
        number (float): The number to be converted.
        
    Returns:
        float: The percentage value of the number if greater than one, otherwise the original number.
    """
    if number > 1:
        return number / 100
    else:
        return number

def create_chunks(content, size_per_chunk):
    """
    Divides the content into chunks of specified size and returns a list of these chunks.
    
    Args:
        content (str): The content to be chunked.
        size_per_chunk (int): The desired size per chunk.
        
    Returns:
        list: A list of content chunks.
    """
    tokens = word_tokenize(content)
    chunks = []
    current_chunk = []
    current_size = 0
    for token in tokens:
        current_size += 1
        if current_size > size_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 1
        current_chunk.append(token)
    chunks.append(' '.join(current_chunk))
    return chunks


def calculate_token_distribution(max_tokens:int=default_tokens(), prompt:str="null", completion_percentage:float=40, size_per_chunk:int=None,chunk_prompt:str="",tokenize_js:dict={}):
    """
    Calculates the token distribution between prompts, completions, and chunks to ensure effective token utilization.
    
    Args:
        max_tokens (int, optional): The maximum number of tokens allowed. Defaults to `default_tokens()`.
        prompt (str, optional): The prompt to be used. Defaults to "null".
        completion_percentage (float, optional): The completion percentage. Defaults to 40.
        size_per_chunk (int, optional): The size per chunk. Defaults to None.
        chunk_prompt (str, optional): The chunk prompt. Defaults to an empty string.
        tokenize_js (dict, optional): Tokenization data. Defaults to an empty dictionary.
        
    Returns:
        dict: A dictionary containing token distribution information.
    """
    total_prompt = ''
    for each in tokenize_js.keys():
        if each != "prompt_data":
            total_prompt+=str(tokenize_js[each])
    total_chunk_data = tokenize_js["prompt_data"]
    completion_percent = convert_to_percentage(tokenize_js["completion_percentage"])
    max_tokens = int(tokenize_js["max_tokens"])
    completion_desired = int(max_tokens*completion_percent)

    request_data_total_length = int(max_tokens)-int(completion_desired)
    total_prompt_length = int(count_tokens(total_prompt))
    ficticious_chunk_length = int(request_data_total_length) - int(total_prompt_length)
    total_chunk_length = int(count_tokens(total_chunk_data))
    ficticious_chunk_length=ficticious_chunk_length
    num_chunks=1
    while ficticious_chunk_length < total_chunk_length:
         total_chunk_length = total_chunk_length- ficticious_chunk_length
         num_chunks+=1
         print(num_chunks)
    chunked_data = create_chunks(total_chunk_data, ficticious_chunk_length)
    token_distribution = {
        "prompt": {
            "available": request_data_total_length-total_prompt_length-ficticious_chunk_length,
            "used": total_prompt_length,
            "desired": request_data_total_length
        },
        "completion": {
            "available": int(request_data_total_length-total_prompt_length-ficticious_chunk_length) + completion_desired,
            "used": 0,
            "desired": completion_desired
        },
        "chunks": {
            "total": num_chunks,
            "length_per": ficticious_chunk_length,
            "data": chunked_data
        }
    }
    print(token_distribution)
    return token_distribution

