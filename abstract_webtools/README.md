```
# abstract_webtools for parsing web content.

## Installation

You can install the package via pip:

```bash
pip install abstract_webtools
```

## Usage

### Get Status Code

The `get_status` function fetches the status code of the URL.

```python
from abstract_webtools import clean_url

urls = clean_url('https://example.com')
print(urls)  # Output: ['https://example.com', 'http://example.com']
tps://example.com'
```

### Try Request

The `try_request` function makes HTTP requests to a URL and returns the response if successful.

```python
from abstract_webtools import try_request

response = try_request('https://www.example.com')
print(response)  # Output: <Response [200]>
```

### Is Valid URL

The `is_valid` function checks whether a given URL is valid.

```python
from abstract_webtools import is_valid

valid = is_valid('https://www.example.com')
print(valid)  # Output: True
```

### Get Source Code

The `get_Source_code` function fetches the source code of a URL with a custom user-agent.

```python
from abstract_webtools import get_Source_code

source_code = get_Source_code('https://www.example.com')
print(source_code)  # Output: HTML source code of the URL
```

### Parse React Source

The `parse_react_source` function fetches the source code of a URL and extracts JavaScript and JSX source code (React components).

```python
from abstract_webtools import parse_react_source

react_code = parse_react_source('https://www.example.com')
print(react_code)  # Output: List of JavaScript and JSX source code found in <script> tags
```

### Get All Website Links

The `get_all_website_links` function returns all URLs found on a specified URL that belong to the same website.

```python
from abstract_webtools import get_all_website_links

links = get_all_website_links('https://www.example.com')
print(links)  # Output: List of URLs belonging to the same website as the specified URL
```

### Parse All

The `parse_all` function fetches the source code of a URL and extracts information about HTML elements, attribute values, attribute names, and class names.

```python
from abstract_webtools import parse_all

HTML_components = parse_all('https://www.example.com')
print(HTML_components["element_types"])       # Output: List of HTML element types
print(HTML_components["attribute_values"])    # Output: List of attribute values
print(HTML_components["attribute_names"])     # Output: List of attribute names
print(HTML_components["class_names"])         # Output: List of class names
```

### Extract Elements

The `extract_elements` function fetches the source code of a URL and extracts portions of the source code based on provided filters.

```python
from abstract_webtools import extract_elements

elements = extract_elements('https://www.example.com', element_type='div', attribute_name='class', class_name='container')
print(elements)  # Output: List of HTML elements that match the provided filters
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

This project is licensed under the MIT License

MIT License

The MIT License was first developed at the Massachusetts Institute of Technology (MIT) in the late 1980s. The exact origins MIT license are bit of mystery. Like the Apache 2.0, and BSD family of licenses the MIT License is a permissive software license that places few restrictions of reuse. Users of software using an MIT License are permitted to use, copy, modify, merge publish, distribute, sublicense and sell copies of the software. Some notable projects use the MIT License including Ruby on Rails, and the X Windows System.
MIT License Conditions
The MIT License is relatively simple and short. Below is the text of the MIT License from the Open Software Initiative.
Begin license text.

Copyright <YEAR> <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
End license text.
Using MIT Licensed Code

 

The basic conditions of using the MIT License are:

1. The original copyright notice

2. A copy of the license itself

are including in all copies or any substantial portions of the software.
MIT License Compatibility

The MIT License is highly compatible with other permissive licenses. Including the BSD family of licenses. It is generally compatible with  GNU GPL group of licenses. However if you distribute the code that contains or is derivative of GNU GPL code the final project must of GPL compliant. In other words any source code must of publicly available. 
MIT License, Patents

The MIT License was developed before patenting software was a common practice in the U.S. It therefore does not contain an express patent license. The broad nature of the license in general, is considered by some to encompass an implicit waiver of patent rights. If you are concerned about patent rights, the Apache 2.0 license contains an explicit contributor's patent license.
MIT No Attribution License (MIT-0)

The MIT No Attribution License is a Public Domain equivalent license it is similar to the  BSD Free license. 

 

Copyright <YEAR><COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
