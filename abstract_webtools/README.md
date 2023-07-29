```
# abstract_web_tools

[![PyPI version](https://badge.fury.io/py/web-scraping-toolkit.svg)](https://badge.fury.io/py/web-scraping-toolkit)

Abstract Web Tools is a Python package that provides various utility functions for web scraping tasks. It is built on top of popular libraries such as `requests`, `BeautifulSoup`, and `urllib3` to simplify the process of fetching and parsing web content.

## Installation

You can install the package via pip:

```bash
pip install abstract_webtools
```

## Usage

### Format URL

The `format_url` function ensures that the URL has a valid format and adds the 'https://' prefix if missing.

```python
from abstract_web_tools import format_url

url = format_url('example.com')
print(url)  # Output: 'https://example.com'
```

### Get Status Code

The `get_status` function fetches the status code of the URL.

```python
from abstract_web_tools import get_status

status_code = get_status('https://www.example.com')
print(status_code)  # Output: 200
```

### Clean URL

The `clean_url` function returns a list of possible URL variations for a given URL.

```python
from abstract_web_tools import clean_url

urls = clean_url('https://example.com')
print(urls)  # Output: ['https://example.com', 'http://example.com']
```

### Get Correct URL

The `get_correct_url` function returns the correct URL from the possible variations by attempting HTTP requests.

```python
from abstract_web_tools import get_correct_url

url = get_correct_url('example.com')
print(url)  # Output: 'https://example.com'
```

### Try Request

The `try_request` function makes HTTP requests to a URL and returns the response if successful.

```python
from abstract_web_tools import try_request

response = try_request('https://www.example.com')
print(response)  # Output: <Response [200]>
```

### Is Valid URL

The `is_valid` function checks whether a given URL is valid.

```python
from abstract_web_tools import is_valid

valid = is_valid('https://www.example.com')
print(valid)  # Output: True
```

### Get Source Code

The `get_Source_code` function fetches the source code of a URL with a custom user-agent.

```python
from abstract_web_tools import get_Source_code

source_code = get_Source_code('https://www.example.com')
print(source_code)  # Output: HTML source code of the URL
```

### Parse React Source

The `parse_react_source` function fetches the source code of a URL and extracts JavaScript and JSX source code (React components).

```python
from abstract_web_tools import parse_react_source

react_code = parse_react_source('https://www.example.com')
print(react_code)  # Output: List of JavaScript and JSX source code found in <script> tags
```

### Get All Website Links

The `get_all_website_links` function returns all URLs found on a specified URL that belong to the same website.

```python
from abstract_web_tools import get_all_website_links

links = get_all_website_links('https://www.example.com')
print(links)  # Output: List of URLs belonging to the same website as the specified URL
```

### Parse All

The `parse_all` function fetches the source code of a URL and extracts information about HTML elements, attribute values, attribute names, and class names.

```python
from abstract_web_tools import parse_all

element_types, attribute_values, attribute_names, class_names = parse_all('https://www.example.com')
print(element_types)       # Output: List of HTML element types
print(attribute_values)    # Output: List of attribute values
print(attribute_names)     # Output: List of attribute names
print(class_names)         # Output: List of class names
```

### Extract Elements

The `extract_elements` function fetches the source code of a URL and extracts portions of the source code based on provided filters.

```python
from abstract_web_tools import extract_elements

elements = extract_elements('https://www.example.com', element_type='div', attribute_name='class', class_name='container')
print(elements)  # Output: List of HTML elements that match the provided filters
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
