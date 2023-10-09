```markdown
# Abstract WebTools
Provides utilities for inspecting and parsing web content, including React components and URL utilities, with enhanced capabilities for managing HTTP requests and TLS configurations.

- **Features**:
  - URL Validation: Ensures URL correctness and attempts different URL variations.
  - HTTP Request Manager: Custom HTTP request handling, including tailored user agents and improved TLS security through a custom adapter.
  - Source Code Acquisition: Retrieves the source code of specified websites.
  - React Component Parsing: Extracts JavaScript and JSX source code from web pages.
  - Comprehensive Link Extraction: Collects all internal links from a specified website.
  - Web Content Analysis: Extracts and categorizes various web content components such as HTML elements, attribute values, attribute names, and class names.

### abstract_webtools.py
**Description:**  
Abstract WebTools offers a suite of utilities designed for web content inspection and parsing. One of its standout features is its ability to analyze URLs, ensuring their validity and automatically attempting different URL variations to obtain correct website access. It boasts a custom HTTP request management system that tailors user-agent strings and employs a specialized TLS adapter for heightened security. The toolkit also provides robust capabilities for extracting source code, including detecting React components on web pages. Additionally, it offers functionalities for extracting all internal website links and performing in-depth web content analysis. This makes Abstract WebTools an indispensable tool for web developers, cybersecurity professionals, and digital analysts.
![image](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/0451d8ea-996f-4de5-9e6c-92a606aae4ef)

- **Dependencies**:
  - `requests`
  - `ssl`
  - `HTTPAdapter` from `requests.adapters`
  - `PoolManager` from `urllib3.poolmanager`
  - `ssl_` from `urllib3.util`
  - `urlparse`, `urljoin` from `urllib.parse`
  - `BeautifulSoup` from `bs4`


# UrlManager

The `UrlManager` is a Python class designed to handle and manipulate URLs. It provides methods for cleaning and normalizing URLs, determining the correct version of a URL, extracting URL components, and more. This class is particularly useful for web scraping, web crawling, or any application where URL management is essential.

## Usage

To use the `UrlManager` class, first import it into your Python script:

```python
from abstract_webtools import UrlManager
```

### Initializing a UrlManager Object

You can create a `UrlManager` object by providing an initial URL and an optional `requests` session. If no URL is provided, it defaults to 'www.example.com':

```python
url_manager = UrlManager(url='https://www.example.com')
```

### URL Cleaning and Normalization

The `clean_url` method takes a URL and returns a list of potential URL variations, including versions with and without 'www.', 'http://', and 'https://':

```python
cleaned_urls = url_manager.clean_url()
```

### Getting the Correct URL

The `get_correct_url` method tries each possible URL variation with an HTTP request to determine the correct version of the URL:

```python
correct_url = url_manager.get_correct_url()
```

### Updating the URL

You can update the URL associated with the `UrlManager` object using the `update_url` method:

```python
url_manager.update_url('https://www.example2.com')
```

### Extracting URL Components

The `url_to_pieces` method extracts various components of the URL, such as protocol, domain name, path, and query:

```python
url_manager.url_to_pieces()
print(url_manager.protocol)
print(url_manager.domain_name)
print(url_manager.path)
print(url_manager.query)
```

### Additional Utility Methods

- `get_domain_name(url)`: Returns the domain name (netloc) of a given URL.
- `is_valid_url(url)`: Checks if a URL is valid.
- `make_valid(href, url)`: Ensures a relative or incomplete URL is valid by joining it with a base URL.
- `get_relative_href(url, href)`: Converts a relative URL to an absolute URL based on a base URL.

## Compatibility Note

The `get_domain` method is kept for compatibility but is inconsistent. Use it only for "webpage_url_domain." Similarly, `url_basename`, `base_url`, and `urljoin` methods are available for URL manipulation.

## Example

Here's a quick example of using the `UrlManager` class:

```python
from abstract_webtools import UrlManager

url_manager = UrlManager(url='https://www.example.com')
cleaned_urls = url_manager.clean_url()
correct_url = url_manager.get_correct_url()
url_manager.update_url('https://www.example2.com')

print(f"Cleaned URLs: {cleaned_urls}")
print(f"Correct URL: {correct_url}")
```

## Dependencies

The `UrlManager` class relies on the `requests` library for making HTTP requests. Ensure you have the `requests` library installed in your Python environment.
# SafeRequest

The `SafeRequest` class is a versatile Python utility designed to handle HTTP requests with enhanced safety features. It integrates with other managers like `URLManager`, `NetworkManager`, and `UserAgentManager` to manage various aspects of the request, such as user-agent, SSL/TLS settings, proxies, headers, and more.

## Usage

To use the `SafeRequest` class, first import it into your Python script:

```python
from abstract_webtools import SafeRequest
```

### Initializing a SafeRequest Object

You can create a `SafeRequest` object with various configuration options. By default, it uses sensible default values, but you can customize it as needed:

```python
safe_request = SafeRequest(url='https://www.example.com')
```

### Updating URL and URLManager

You can update the URL associated with the `SafeRequest` object using the `update_url` method, which also updates the underlying `URLManager`:

```python
safe_request.update_url('https://www.example2.com')
```

You can also update the `URLManager` directly:

```python
from url_manager import URLManager

url_manager = URLManager(url='https://www.example3.com')
safe_request.update_url_manager(url_manager)
```

### Making HTTP Requests

The `SafeRequest` class handles making HTTP requests using the `try_request` method. It handles retries, timeouts, and rate limiting:

```python
response = safe_request.try_request()
if response:
    # Process the response here
```

### Accessing Response Data

You can access the response data in various formats:

- `safe_request.source_code`: HTML source code as a string.
- `safe_request.source_code_bytes`: HTML source code as bytes.
- `safe_request.source_code_json`: JSON data from the response (if the content type is JSON).
- `safe_request.react_source_code`: JavaScript and JSX source code extracted from `<script>` tags.

### Customizing Request Configuration

The `SafeRequest` class provides several options for customizing the request, such as headers, user-agent, proxies, SSL/TLS settings, and more. These can be set during initialization or updated later.

### Handling Rate Limiting

The class can handle rate limiting scenarios by implementing rate limiters and waiting between requests.

### Error Handling

The `SafeRequest` class handles various request-related exceptions and provides error messages for easier debugging.

## Dependencies

The `SafeRequest` class relies on the `requests` library for making HTTP requests. Ensure you have the `requests` library installed in your Python environment:

```bash
pip install requests
```

## Example

Here's a quick example of using the `SafeRequest` class:

```python
from abstract_webtools import SafeRequest

safe_request = SafeRequest(url='https://www.example.com')
response = safe_request.try_request()
if response:
    print(f"Response status code: {response.status_code}")
    print(f"HTML source code: {safe_request.source_code}")
```

# SoupManager

The `SoupManager` class is a Python utility designed to simplify web scraping by providing easy access to the BeautifulSoup library. It allows you to parse and manipulate HTML or XML source code from a URL or provided source code.

## Usage

To use the `SoupManager` class, first import it into your Python script:

```python
from abstract_webtools import SoupManager
```

### Initializing a SoupManager Object

You can create a `SoupManager` object with various configuration options. By default, it uses sensible default values, but you can customize it as needed:

```python
soup_manager = SoupManager(url='https://www.example.com')
```

### Updating URL and Request Manager

You can update the URL associated with the `SoupManager` object using the `update_url` method, which also updates the underlying `URLManager` and `SafeRequest`:

```python
soup_manager.update_url('https://www.example2.com')
```

You can also update the source code directly:

```python
source_code = '<html>...</html>'
soup_manager.update_source_code(source_code)
```

### Accessing and Parsing HTML

The `SoupManager` class provides easy access to the BeautifulSoup object, allowing you to search, extract, and manipulate HTML elements easily. You can use methods like `find_all`, `get_class`, `has_attributes`, and more to work with the HTML content.

```python
elements = soup_manager.find_all(tag='a')
```

### Extracting Links

The class also includes methods for extracting all website links from the HTML source code:

```python
all_links = soup_manager.all_links
```

### Extracting Meta Tags

You can extract meta tags from the HTML source code using the `meta_tags` property:

```python
meta_tags = soup_manager.meta_tags
```

### Customizing Parsing

You can customize the parsing behavior by specifying the parser type during initialization or updating it:

```python
soup_manager.update_parse_type('lxml')
```

## Dependencies

The `SoupManager` class relies on the `BeautifulSoup` library for parsing HTML or XML. Ensure you have the `beautifulsoup4` library installed in your Python environment:

```bash
pip install beautifulsoup4
```

## Example

Here's a quick example of using the `SoupManager` class:

```python
from abstract_webtools import SoupManager

soup_manager = SoupManager(url='https://www.example.com')
all_links = soup_manager.all_links
print(f"All Links: {all_links}")
```
# LinkManager

The `LinkManager` class is a Python utility designed to simplify the extraction and management of links (URLs) and associated data from HTML source code. It leverages other classes like `URLManager`, `SafeRequest`, and `SoupManager` to facilitate link extraction and manipulation.

## Usage

To use the `LinkManager` class, first import it into your Python script:

```python
from abstract_webtools import LinkManager
```

### Initializing a LinkManager Object

You can create a `LinkManager` object with various configuration options. By default, it uses sensible default values, but you can customize it as needed:

```python
link_manager = LinkManager(url='https://www.example.com')
```

### Updating URL and Request Manager

You can update the URL associated with the `LinkManager` object using the `update_url` method, which also updates the underlying `URLManager`, `SafeRequest`, and `SoupManager`:

```python
link_manager.update_url('https://www.example2.com')
```

### Accessing Extracted Links

The `LinkManager` class provides easy access to extracted links and associated data:

```python
all_links = link_manager.all_desired_links
```

### Customizing Link Extraction

You can customize the link extraction behavior by specifying various parameters during initialization or updating them:

```python
link_manager.update_desired(
    img_attr_value_desired=['thumbnail', 'image'],
    img_attr_value_undesired=['icon'],
    link_attr_value_desired=['blog', 'article'],
    link_attr_value_undesired=['archive'],
    image_link_tags='img',
    img_link_attrs='src',
    link_tags='a',
    link_attrs='href',
    strict_order_tags=True,
    associated_data_attr=['data-title', 'alt', 'title'],
    get_img=['data-title', 'alt', 'title']
)
```

## Dependencies

The `LinkManager` class relies on other classes within the `abstract_webtools` module, such as `URLManager`, `SafeRequest`, and `SoupManager`. Ensure you have these classes and their dependencies correctly set up in your Python environment.

## Example

Here's a quick example of using the `LinkManager` class:

```python
from abstract_webtools import LinkManager

link_manager = LinkManager(url='https://www.example.com')
all_links = link_manager.all_desired_links
print(f"All Links: {all_links}")
```
##Overall Usecases
```python
from abstract_webtools import URLManager, SafeRequest, SoupManager, LinkManager, VideoDownloader

# --- URLManager: Manages and manipulates URLs for web scraping/crawling ---
url = "example.com"
url_manager = URLManager(url=url)

# --- SafeRequest: Safely handles HTTP requests by managing user-agent, SSL/TLS, proxies, headers, etc. ---
request_manager = SafeRequest(
    url_manager=url_manager,
    proxies={'8.219.195.47', '8.219.197.111'},
    timeout=(3.05, 70)
)

# --- SoupManager: Simplifies web scraping with easy access to BeautifulSoup ---
soup_manager = SoupManager(
    url_manager=url_manager,
    request_manager=request_manager
)

# --- LinkManager: Extracts and manages links and associated data from HTML source code ---
link_manager = LinkManager(
    url_manager=url_manager,
    soup_manager=soup_manager,
    link_attr_value_desired=['/view_video.php?viewkey='],
    link_attr_value_undesired=['phantomjs']
)

# Download videos from provided links (list or string)
video_manager = VideoDownloader(link=link_manager.all_desired_links).download()

# Use them individually, with default dependencies for basic inputs:
standalone_soup = SoupManager(url=url).soup
standalone_links = LinkManager(url=url).all_desired_links

# Updating methods for manager classes
url_1 = 'thedailydialectics.com'
print(f"updating URL to {url_1}")
url_manager.update_url(url=url_1)
request_manager.update_url(url=url_1)
soup_manager.update_url(url=url_1)
link_manager.update_url(url=url_1)

# Updating URL manager references
request_manager.update_url_manager(url_manager=url_manager)
soup_manager.update_url_manager(url_manager=url_manager)
link_manager.update_url_manager(url_manager=url_manager)

# Updating source code for managers
source_code_bytes = request_manager.source_code_bytes
soup_manager.update_source_code(source_code=source_code_bytes)
link_manager.update_source_code(source_code=source_code_bytes)
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

#### Module Information
-**Author**: putkoff
-**Author Email**: partners@abstractendeavors.com
-**Github**: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_webtools
-**PYPI**: https://pypi.org/project/abstract-webtools
-**Part of**: abstract_essentials
-**Date**: 10/10/2023
-**Version**: 0.1.4.54
---

```
