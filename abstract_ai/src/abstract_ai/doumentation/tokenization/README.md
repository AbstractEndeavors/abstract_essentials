# Tokenization.py (part of Abstract_AI Module)

**Author:** putkoff  
**Email:** partners@abstractendeavors.com  
**GitHub:** [GitHub Link](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai)  
**PyPI:** [PyPI Link](https://pypi.org/project/abstract-ai/)  
**License:** MIT  
**Version:** 0.1.4.0  

## Overview 

Tokenization.py is an integral script in the Abstract_AI module. It primarily involves tokenizing text inputs and distributing them effectively. Containing several key functions, it is focused on token processing which is essential in tasks such as natural language processing and machine learning applications. 

## Functions
Within the script, several functions play crucial roles. They include:

### 1. `count_tokens(text: str) -> int`
This function takes in an input text, tokenizes it into words and returns the count of the tokens.  

### 2. `convert_to_percentage(number: float) -> float`
The function converts the input number to a percentage. If the number is greater than one, it is divided by 100, if not the number itself is returned.

### 3. `create_chunks(content: str, size_per_chunk: int) -> list`
This function is used to split the input content into chunks of the specified size (in tokens). It performs tokenization and constructs chunks according to the given size.

### 4. `calculate_token_distribution(max_tokens: int, prompt: str, completion_percentage: float = 40, size_per_chunk: int = None) -> dict`
This function plays a critical role by calculating the distribution of tokens for a prompt and its completion text. It takes in the maximum tokens limit, the prompt, percentage of completion, and optionally the size per chunk. It returns a comprehensive dictionary with the token distribution details related to prompt, completion and chunks.

Please note that all the above functions have well-drafted docstrings to provide better understanding on their usage.", "notation":"Token distribution calculation and processing issues have been duly addressed.
