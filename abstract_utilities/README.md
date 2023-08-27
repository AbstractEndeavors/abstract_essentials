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

## License

This project is licensed under the terms of

 the MIT license.
