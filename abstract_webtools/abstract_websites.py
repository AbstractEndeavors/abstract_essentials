import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def format_url(url):
    """
    Formats the given URL by adding 'https://' if missing and returns the formatted URL.

    Args:
        url (str): The URL to format.

    Returns:
        str: The formatted URL.
    """
    # Check if the URL starts with 'http://' or 'https://'
    if not url.startswith(('http://', 'https://')):
        # Add 'https://' prefix if missing
        url = 'https://' + url
    # Check if the URL has a valid format
    if not re.match(r'^https?://\w+', url):
        # Return None if the URL is invalid
        return None
    return url

def get_status(url):
    """
    Gets the HTTP status code of the given URL.

    Args:
        url (str): The URL to check the status of.

    Returns:
        int: The HTTP status code of the URL, or None if the request fails.
    """
    # Get the status code of the URL
    return try_request(url=url).status_code

def clean_url(url: str):
    """
    Cleans the given URL and returns a list of possible variations.

    Args:
        url (str): The URL to clean.

    Returns:
        list: A list of possible URL variations, including 'http://' and 'https://' prefixes.
    """
    # Clean the URL and return possible variations
    urls = [url]
    if url.startswith('https://'):
        urls.append('http://' + url[len('https://'):])
    elif url.startswith('http://'):
        urls.append('https://' + url[len('http://'):])
    else:
        urls.append('https://' + url)
        urls.append('http://' + url)
    return urls

def get_correct_url(url: str, session: type(requests.Session) = requests):
    """
    Gets the correct URL from the possible variations by trying each one with an HTTP request.

    Args:
        url (str): The URL to find the correct version of.
        session (type(requests.Session), optional): The requests session to use for making HTTP requests.
            Defaults to requests.

    Returns:
        str: The correct version of the URL if found, or None if none of the variations are valid.
    """
    # Get the correct URL from the possible variations
    urls = clean_url(url)
    for url in urls:
        try:
            source = session.get(url)
            return url
        except requests.exceptions.RequestException as e:
            print(e)
    return None

def try_request(url: str, session: type(requests.Session) = requests):
    """
    Tries to make an HTTP request to the given URL using the provided session.

    Args:
        url (str): The URL to make the request to.
        session (type(requests.Session), optional): The requests session to use for making HTTP requests.
            Defaults to requests.

    Returns:
        requests.Response or None: The response object if the request is successful, or None if the request fails.
    """
    # Try to make the HTTP request and return the response if successful
    urls = clean_url(url)
    for url in urls:
        try:
            return session.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
    return None

def is_valid(url):
    """
    Checks whether `url` is a valid URL.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)                      

def desktop_user_agents():
    """
    Returns a list of popular desktop user-agent strings for various browsers.

    Returns:
        list: A list of desktop user-agent strings.
    """
    return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14']

def get_user_agent(user_agent=desktop_user_agents()[0]):
    """
    Returns the user-agent header dictionary with the specified user-agent.

    Args:
        user_agent (str, optional): The user-agent string to be used. Defaults to the first user-agent in the list.

    Returns:
        dict: A dictionary containing the 'user-agent' header.
    """
    return {"user-agent": user_agent}

class TLSAdapter(HTTPAdapter):
    """
    A custom HTTPAdapter class that sets TLS/SSL options and ciphers.

    Attributes:
        ssl_options (int): The TLS/SSL options to use when creating the SSL context.
    """
    def ssl_options(self):
        """
        Returns the SSL options to be used when creating the SSL context.

        Returns:
            int: The SSL options.
        """
        return ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION

    def __init__(self, ssl_options=0, *args, **kwargs):
        """
        Initializes the TLSAdapter with the specified SSL options.

        Args:
            ssl_options (int, optional): The TLS/SSL options to use when creating the SSL context. Defaults to 0.
        """
        self.ssl_options = ssl_options
        super().__init__(*args, **kwargs)

    def add_string_list(self, ls: (list or str), delim: str = '', string: str = ''):
        """
        Concatenates the elements of a list into a single string with the given delimiter.

        Args:
            ls (list or str): The list of elements or a comma-separated string.
            delim (str, optional): The delimiter to use when concatenating elements. Defaults to an empty string.
            string (str, optional): The initial string to append elements. Defaults to an empty string.

        Returns:
            str: The concatenated string.
        """
        if isinstance(ls, str):
            ls = list(ls.split(','))
        if isinstance(ls, list):
            string = ''
            for part in ls:
                string = string + delim + part
        return string

    def get_ciphers(self):
        """
        Returns a list of preferred TLS/SSL ciphers.

        Returns:
            list: A list of TLS/SSL ciphers.
        """
        return "ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,AES256-SHA,AES128-SHA".split(',')

    def create_ciphers_string(self, ls: list = None):
        """
        Creates a colon-separated string of TLS/SSL ciphers from a list of ciphers.

        Args:
            ls (list, optional): The list of TLS/SSL ciphers to use. Defaults to None, in which case it uses the default list.

        Returns:
            str: The colon-separated string of TLS/SSL ciphers.
        """
        if ls is None:
            ls = self.get_ciphers()
        cipher_string = self.add_string_list(ls=ls, delim=':')[:-1]
        globals()['CIPHERS'] = cipher_string
        return cipher_string

    def init_poolmanager(self, *args, **kwargs):
        """
        Initializes the pool manager with the custom SSL context and ciphers.
        """
        context = ssl_.create_urllib3_context(ciphers=self.create_ciphers_string(), cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)

def get_Source_code(url: str = 'https://www.example.com', user_agent= desktop_user_agents()[0]):
    """
    Fetches the source code of the specified URL using a custom user-agent.

    Args:
        url (str, optional): The URL to fetch the source code from. Defaults to 'https://www.example.com'.
        user_agent (str, optional): The user-agent to use for the request. Defaults to the first user-agent in the list.

    Returns:
        str or None: The source code of the URL if the request is successful, or None if the request fails.
    """
    url = get_correct_url(url)
    if url is None:
        return None
    
    s = requests.Session()
    s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
    s.headers.update(get_user_agent(user_agent))
    adapter = TLSAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    s.mount('https://', adapter)
    r = try_request(url=url, session=s)

    if r is None:
        return None
    return r.text

def parse_react_source(url):
    """
    Fetches the source code of the specified URL and extracts JavaScript and JSX source code (React components).

    Args:
        url (str): The URL to fetch the source code from.

    Returns:
        list: A list of strings containing JavaScript and JSX source code found in <script> tags.
    """
    url = get_correct_url(url)
    if url is None:
        return []
    
    data = get_Source_code(url)
    soup = BeautifulSoup(data, 'html.parser')
    script_tags = soup.find_all('script', type=lambda t: t and ('javascript' in t or 'jsx' in t))
    react_source_code = []
    for script_tag in script_tags:
        react_source_code.append(script_tag.string)
    return react_source_code

def get_all_website_links(url):
    """
    Returns all URLs that are found on the specified URL and belong to the same website.

    Args:
        url (str): The URL to search for links.

    Returns:
        list: A list of URLs that belong to the same website as the specified URL.
    """
    url = get_correct_url(url)
    if url is None:
        return []
    
    urls = [url]
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(get_Source_code(url=url), "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not an absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            continue
        urls.append(href)
    return urls

def parse_all(url):
    """
    Parses the source code of the specified URL and extracts information about HTML elements, attribute values, attribute names, and class names.

    Args:
        url (str): The URL to fetch the source code from.

    Returns:
        tuple: A tuple containing lists of element types, attribute values, attribute names, and class names found in the source code.
    """
    url = get_correct_url(url)
    if url is None:
        return [], [], [], []
    
    data = get_Source_code(url)
    element_types, attribute_values, attribute_names, class_names = [], [], [], []
    data = str(data).split('<')
    for k in range(1, len(data)):
        dat = data[k].split('>')[0]
        if dat[0] != '/':
            if dat.split(' ')[0] not in element_types:
                element_types.append(dat.split(' ')[0])
        dat = dat[len(dat.split(' ')[0]) + 1:].split('"')
        for c in range(1, len(dat)):
            if len(dat[c]) > 0:
                if '=' == dat[c][-1] and ' ' == dat[c][0] and dat[c] != '/':
                    if dat[c][1:] + '"' + dat[c + 1] + '"' not in attribute_values:
                        attribute_values.append(dat[c][1:] + '"' + dat[c + 1] + '"')
                    if dat[c][1:-1] not in attribute_names:
                        attribute_names.append(dat[c][1:-1])
                    if dat[c + 1] not in class_names:
                        class_names.append(dat[c + 1])
    return element_types, attribute_values, attribute_names, class_names
def extract_elements(url, element_type=None, attribute_name=None, class_name=None):
    """
    Extracts portions of the source code from the specified URL based on provided filters.

    Args:
        url (str): The URL to fetch the source code from.
        element_type (str, optional): The HTML element type to filter by. Defaults to None.
        attribute_name (str, optional): The attribute name to filter by. Defaults to None.
        class_name (str, optional): The class name to filter by. Defaults to None.

    Returns:
        list: A list of strings containing portions of the source code that match the provided filters.
    """
    url = get_correct_url(url)
    if url is None:
        return []

    data = get_Source_code(url)
    soup = BeautifulSoup(data, 'html.parser')

    elements = []

    # If no filters are provided, return the entire source code
    if not element_type and not attribute_name and not class_name:
        elements.append(str(soup))
        return elements

    # Find elements based on the filters provided
    if element_type:
        elements.extend([str(tag) for tag in soup.find_all(element_type)])

    if attribute_name:
        elements.extend([str(tag) for tag in soup.find_all(attrs={attribute_name: True})])

    if class_name:
        elements.extend([str(tag) for tag in soup.find_all(class_=class_name)])

    return elements

