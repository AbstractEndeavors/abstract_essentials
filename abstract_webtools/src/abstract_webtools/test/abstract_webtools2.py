"""
# `abstract_webtools.py` Documentation

This script, `abstract_webtools.py`, is a component of the `abstract_webtools` module and is a part of the `abstract_essentials` package. It provides a set of tools and functions to interact with and parse web content.

## Contents

1. **Imports**
   - Essential modules and classes for web requests, SSL configurations, and URL parsing are imported at the beginning.

2. **Core Functions**

   - `get_status(url: str) -> int or None`:
     Fetches the HTTP status code for a given URL.

   - `clean_url(url: str) -> list`:
     Returns variations of the given URL with different protocols.

   - `get_correct_url(url: str, session: requests.Session) -> str or None`:
     Identifies the correct URL from possible variations using HTTP requests.

   - `try_request(url: str, session: requests.Session) -> requests.Response or None`:
     Attempts to make an HTTP request to a given URL.

   - `is_valid(url: str) -> bool`:
     Validates if a given URL is structurally correct.

   - `desktop_user_agents() -> list`:
     Returns a list of popular desktop user-agent strings.

   - `get_user_agent(user_agent: str) -> dict`:
     Returns a dictionary containing the user-agent header.

3. **TLSAdapter Class**

   A custom HTTPAdapter class that manages SSL options and ciphers for web requests.

   - `TLSAdapter.__init__(self, ssl_options: int)`: 
     Initializes the adapter with specific SSL options.

   - Several methods to handle cipher strings, creation of cipher strings, and initialization of the pool manager with custom SSL configurations.

4. **Advanced Web Functions**

   - `get_Source_code(url: str, user_agent: str) -> str or None`:
     Retrieves the source code of a website with a custom user-agent.

   - `parse_react_source(url: str) -> list`:
     Extracts JavaScript and JSX source code from the specified URL.

   - `get_all_website_links(url: str) -> list`:
     Lists all the internal URLs found on a specific webpage.

   - `parse_all(url: str) -> dict`:
     Parses source code to extract details about elements, attributes, and class names.

   - `extract_elements(url: str, element_type: str, attribute_name: str, class_name: str)`:
     Extracts specific portions of source code based on provided filters. The function signature seems to be cut off, so the full details aren't available.

## Usage

The functions and classes provided in this module allow users to interact with websites, from simple actions like getting the status code of a URL to more advanced functionalities such as parsing ReactJS source codes or extracting specific HTML elements from a website.

To utilize this module, simply import the required function or class and use it in your application. The functions have been designed to be intuitive and the provided docstrings give clear guidance on their usage.

Author: putkoff
Version: 1.0
"""
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from abstract_utilities.time_utils import get_time_stamp,get_sleep,sleep_count_down
from abstract_utilities.json_utils import safe_json_loads
from urllib3.util import ssl_
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
import logging
from abstract_utilities.time_utils import get_time_stamp, sleep_count_down

logging.basicConfig(level=logging.INFO)

class DynamicRateLimiterManager:
    def __init__(self):
        self.services = {}

    def add_service(self, service_name, low_limit, high_limit, limit_epoch, starting_tokens=None, epoch_cycle_adjustment:int=None):
        if service_name in self.services:
            logging.warning(f"Service {service_name} already exists!")
            return
        self.services[service_name] = DynamicRateLimiter(low_limit, high_limit, limit_epoch, starting_tokens, epoch_cycle_adjustment)

    def request(self, service_name):
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not found!")
        
        limiter = self.services[service_name]
        can_request = limiter.request()
        self.log_request(service_name, can_request)
        return can_request

    def log_request(self, service_name, success):
        self.services[service_name].calculate_tokens()
        logging.info(f"[{service_name}] Request {'succeeded' if success else 'denied'}. Current tokens: {self.services[service_name].tokens}")

class DynamicRateLimiter:
    def __init__(self, low_limit, high_limit, limit_epoch, starting_tokens=None, epoch_cycle_adjustment:int=None):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.limit_epoch = limit_epoch
        self.current_limit = starting_tokens or low_limit
        self.epoch_cycle_adjustment = epoch_cycle_adjustment or 0
        self.last_adjusted_time = get_time_stamp()
        self.initialize_request_status()

    def initialize_request_status(self):
        self.request_status = {
            "successful": [],
            "unsuccessful": [],
            "last_requested": get_time_stamp(),
            "epoch_initial_time": 0,
            "epoch_left": self.limit_epoch,
            "count_since_fail": 0
        }
    def request_tracker(self,success):
        if self.request_status["epoch_initial_time"]==0:
            self.request_status["epoch_initial_time"] = get_time_stamp()
        if success == True:
            self.request_status["successful"].append(get_time_stamp())
            self.request_status["count_since_fail"]=max(self.request_status["count_since_fail"]+1,1)
        else:
            self.request_status["unsuccessful"].append(get_time_stamp())
            self.request_status["last_fail"]=get_time_stamp()
            self.request_status["count_since_fail"]=min(self.request_status["count_since_fail"]-1,0)
            print(f"count since fail {self.request_status['count_since_fail']}")
        self.request_status["last_requested"]=get_time_stamp()

    def is_past_first_epoch(self):
        return (get_time_stamp() - self.request_status["epoch_initial_time"]) > self.limit_epoch

    def calculate_tokens(self):
        self.get_elapsed_time_for_current_epoch()
        elapsed_time = get_time_stamp() - self.request_status["last_requested"]
        new_tokens = int((elapsed_time / self.limit_epoch) * self.current_limit)
        self.tokens = min(self.current_limit, new_tokens)
        return self.request_status
    def adjust_rate(self):
        if self.is_past_first_epoch() and self.request_status["count_since_fail"] < -2:
            if self.request_status["count_since_fail"] % 2 == 0:
                self.limit_epoch += 1
                sleep_count_down(self.limit_epoch)

    def request(self):
        self.adjust_rate()
        self.calculate_tokens()
        if self.tokens > 0:
            return True
        return False
    def requests_in_current_epoch(self,type_request:str="successful"):
        epoch_elapsed = self.get_elapsed_time_for_current_epoch()
        epoch_left = self.limit_epoch-epoch_elapsed
        fraction_elapsed = epoch_elapsed / self.limit_epoch
        successful = []
        for each in self.request_status[type_request]:
            if (each - self.request_status["current_epoch_start"])<self.limit_epoch:
                successful.append(each)
        return len(successful)
    def get_elapsed_time_for_current_epoch(self):
        elapsed_time_in_current_epoch = 0
        current_time = get_time_stamp()
        if self.request_status["epoch_initial_time"] != None:
            elapsed_time_in_current_epoch = (current_time - self.request_status["epoch_initial_time"]) % self.limit_epoch
        self.request_status["current_epoch_start"]=current_time-elapsed_time_in_current_epoch
        self.request_status["epoch_left"]=self.limit_epoch-elapsed_time_in_current_epoch
        #print(f" epoch initial time = {self.request_status['epoch_initial_time']}\ncurrent epoch time elapsed = {elapsed_time_in_current_epoch}")
        return elapsed_time_in_current_epoch
class DynamicRateLimiterManagerSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        if DynamicRateLimiterManagerSingleton._instance is None:
            DynamicRateLimiterManagerSingleton._instance = DynamicRateLimiterManager()
        return DynamicRateLimiterManagerSingleton._instance

def desktop_user_agents() -> list:
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

def get_user_agent(user_agent:str=desktop_user_agents()[0]) -> dict:
    """
    Returns the user-agent header dictionary with the specified user-agent.

    Args:
        user_agent (str, optional): The user-agent string to be used. Defaults to the first user-agent in the list.

    Returns:
        dict: A dictionary containing the 'user-agent' header.
    """
    return {"user-agent": user_agent}

class SafeRequest:
    def __init__(self, max_retries=3,last_request_time=None,request_wait_limit=1.5):
        self.session = self.initialize_session()
        self.max_retries = max_retries
        self.last_request_time = last_request_time
        self.request_wait_limit = request_wait_limit
        
    def initialize_session(self,user_agent:str= desktop_user_agents()[0]):
        s = requests.Session()
        s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
        s.headers.update(get_user_agent(user_agent))
        # Add any other headers or cookie settings here
        adapter = TLSAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        s.mount('https://', adapter)
        return s

    @staticmethod
    def clean_url(url):
        """
        Given a URL, return a list with both HTTP and HTTPS versions.
        """
        cleaned = url.replace("http://", "").replace("https://", "")
        return [f"http://{cleaned}", f"https://{cleaned}"]

    def wait_between_requests(self):
        """
        Wait between requests based on the request_wait_limit.
        """
        if self.last_request_time:
            sleep_time = self.request_wait_limit - (get_time_stamp() - self.last_request_time)
            if sleep_time > 0:
                logging.info(f"Sleeping for {sleep_time:.2f} seconds.")
                get_sleep(sleep_time)

    def make_request(self, url, last_request_time=None, request_wait_limit=None):
        """
        Make a request and handle potential errors.
        """
        # Update the instance attributes if they are passed
        if last_request_time is not None:
            self.last_request_time = last_request_time
        if request_wait_limit is not None:
            self.request_wait_limit = request_wait_limit
            

        self.wait_between_requests()

        cleaned_urls = self.clean_url(url)
        for _ in range(self.max_retries):
            for cleaned_url in cleaned_urls:
                try:
                    response = self.session.get(cleaned_url)
                    if response.status_code == 200:
                        self.last_request_time = get_time_stamp()
                        return response
                    elif response.status_code == 429:
                        logging.warning(f"Rate limited by {cleaned_url}. Retrying...")
                        get_sleep(5)  # adjust this based on the server's rate limit reset time

                except requests.ConnectionError:
                    logging.error(f"Connection error for URL {cleaned_url}.")
                except requests.Timeout:
                    logging.error(f"Request timeout for URL {cleaned_url}.")
                except requests.RequestException as e:
                    logging.error(f"Request exception for URL {cleaned_url}: {e}")

        logging.error(f"Failed to retrieve content from {url} after {self.max_retries} retries.")
        return None


    @staticmethod
    def is_valid_url(url):
        """
        Check if the given URL is valid.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    def get_source_code(self, url):
        if self.is_valid_url(url):
            response = self.make_request(url)
            return response.text if response else None
        else:
            logging.error(f"Invalid URL: {url}")
            return None
## ## 
# Usage
## safe_requester = SafeRequest()
## 
## url = "example.com"  # replace with your URL
## if safe_requester.is_valid_url(url):
##     response = safe_requester.make_request(url)
##     if response:
##         print(response.text)
## else:
##     logging.error(f"Invalid URL: {url}")
# Usage 2
##    safe_requester = SafeRequest()
##    source_code = safe_requester.get_source_code('https://www.example.com')
##    if source_code:
##        print(source_code)
## ## 
class TLSAdapter(HTTPAdapter):
    """
    A custom HTTPAdapter class that sets TLS/SSL options and ciphers.

    Attributes:
        ssl_options (int): The TLS/SSL options to use when creating the SSL context.
    """
    def ssl_options(self) -> int:
        """
        Returns the SSL options to be used when creating the SSL context.

        Returns:
            int: The SSL options.
        """
        return ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION

    def __init__(self, ssl_options:int=0, *args, **kwargs):
        """
        Initializes the TLSAdapter with the specified SSL options.

        Args:
            ssl_options (int, optional): The TLS/SSL options to use when creating the SSL context. Defaults to 0.
        """
        self.ssl_options = ssl_options
        super().__init__(*args, **kwargs)

    def add_string_list(self, ls: (list or str), delim: str = '', string: str = '') -> str:
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

    def get_ciphers(self) -> str:
        """
        Returns a list of preferred TLS/SSL ciphers.

        Returns:
            list: A list of TLS/SSL ciphers.
        """
        return "ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,AES256-SHA,AES128-SHA".split(',')

    def create_ciphers_string(self, ls:list=None) ->str:
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

    def init_poolmanager(self, *args, **kwargs) ->None:
        """
        Initializes the pool manager with the custom SSL context and ciphers.
        """
        context = ssl_.create_urllib3_context(ciphers=self.create_ciphers_string(), cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)
def safe_json_loads(obj):
    if isinstance(obj,(dict,list)):
        return obj
    try_obj = str(obj)
    try:
        obj = json.loads(try_obj)
    except:
        pass
    return obj
def get_token_sleep(manager, service_name, success, response):
    manager.services[service_name].request_tracker(success)
    print(f"Rate limited by {service_name}. Adjusted limit. Retrying...")
    sleep_count_down(manager.services[service_name].calculate_tokens()["token_sleep"])
    print(response)
    return True

def get_limited_request(request_url, service_name="default"):
    manager = DynamicRateLimiterManagerSingleton.get_instance()
    
    while True:
        if not manager.request(service_name):
            print(f"Rate limit for {service_name} limited by user. \nsuccessful runs = {manager.services[service_name].requests_in_current_epoch(type_request='successful')}\nWaiting for the next epoch...")
            sleep_count_down(manager.services[service_name].calculate_tokens()["epoch_left"])
            manager.services[service_name].request_status["successful"] = []
            manager.services[service_name].request_status["unsuccessful"] = []

        response = requests.get(request_url)
        if manager.services[service_name].request_status["epoch_initial_time"] is None:
            manager.services[service_name].request_status["epoch_initial_time"] = get_time_stamp()

        if response.status_code == 200:
            response_data = response.json()
            try_sleep = False

            if 'status' in response_data and isinstance(response_data, dict):
                if response_data['status'] == '0':
                    try_sleep = True

            if 'response' in response_data:
                if any(limit_message in response_data['response'].lower() for limit_message in ['max rate limit reached', "you've exceeded the rate limit"]):
                    try_sleep = get_token_sleep(manager, service_name, False, response_data)

            if not try_sleep:
                manager.services[service_name].request_tracker(True)
                return response_data
            else:
                print(response_data)

        elif response.status_code == 429:
            get_token_sleep(manager, service_name, False, response.json())

        elif response.status_code not in [200, 429]:
            print(f"Unexpected response: {response.status_code}. Message: {response.text}")
            return None

        
def strip_web(url: str) -> str:
    """
    Strip the 'http://' or 'https://' prefix from a URL, if present.

    Parameters:
    url (str): The URL string to process.

    Returns:
    str: The URL string with the prefix removed.
    """
    if url.startswith("http://"):
        url = url.replace("http://", '', 1)
    elif url.startswith("https://"):
        url = url.replace("https://", '', 1)
    return url

def get_status(url:str=None) -> int:
    """
    Gets the HTTP status code of the given URL.

    Args:
        url (str): The URL to check the status of.

    Returns:
        int: The HTTP status code of the URL, or None if the request fails.
    """
    # Get the status code of the URL
    return try_request(url=url).status_code

def clean_url(url:str=None) -> (list or None):
    """
    Cleans the given URL and returns a list of possible variations.

    Args:
        url (str): The URL to clean.

    Returns:
        list: A list of possible URL variations, including 'http://' and 'https://' prefixes.
    """
    # Clean the URL and return possible variations
    if url == None:
        return
    urls = [url]
    if url.startswith('https://'):
        urls.append('http://' + url[len('https://'):])
    elif url.startswith('http://'):
        urls.append('https://' + url[len('http://'):])
    else:
        urls.append('https://' + url)
        urls.append('http://' + url)
    return urls

def get_correct_url(url: str=None, session: type(requests.Session) = requests) -> (str or None):
    """
    Gets the correct URL from the possible variations by trying each one with an HTTP request.

    Args:
        url (str): The URL to find the correct version of.
        session (type(requests.Session), optional): The requests session to use for making HTTP requests.
            Defaults to requests.

    Returns:
        str: The correct version of the URL if found, or None if none of the variations are valid.
    """
    if url == None:
        return
    # Get the correct URL from the possible variations
    urls = clean_url(url)
    for url in urls:
        try:
            source = session.get(url)
            return url
        except requests.exceptions.RequestException as e:
            print(e)
    return None

def try_request(url:str=None, session:type(requests.Session)=requests) -> (requests.Response or None):
    """
    Tries to make an HTTP request to the given URL using the provided session.

    Args:
        url (str): The URL to make the request to.
        session (type(requests.Session), optional): The requests session to use for making HTTP requests.
            Defaults to requests.

    Returns:
        requests.Response or None: The response object if the request is successful, or None if the request fails.
    """
    if url == None:
        return
    # Try to make the HTTP request and return the response if successful
    urls = clean_url(url)
    for url in urls:
        try:
            return session.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
    return None

def is_valid(url:str=None) -> bool:
    """
    Checks whether `url` is a valid URL.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    if url == None:
        return False
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)                      

def get_Source_code(url: str = 'https://www.example.com', user_agent:str= desktop_user_agents()[0]) -> (str or None):
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

def parse_react_source(url:str=None) -> list:
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

def get_all_website_links(url:str=None) -> list:
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

def parse_all(url:str=None):
    """
    Parses the source code of the specified URL and extracts information about HTML elements, attribute values, attribute names, and class names.

    Args:
        url (str): The URL to fetch the source code from.

    Returns:
        dict: A dict containing keys: [element_types, attribute_values, attribute_names, class_names] with values as lists for keys element types, attribute values, attribute names, and class names found in the source code.
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
    return {"element_types":element_types, "attribute_values":attribute_values, "attribute_names":attribute_names, "class_names":class_names}
def extract_elements(url:str=None, element_type:str=None, attribute_name:str=None, class_name:str=None) -> list:
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
def get_response(response):
    if response.headers.get('content-type') == 'application/json':
        data = safe_json_loads(response.text)
        if data:
            return data.get("response", data)
    return response.text
request_manager = DynamicRateLimiterManagerSingleton.get_instance()
def get_request(request_url:str=None, request_type: str = None, request_min: int = 20, request_max: int = 30,limit_epoch: int = 60, request_start: int = None,epoch_cycle_adjustment:int=None):
    """
    Make a limited request to the ABI URL using rate-limiting.

    :param request_type: Type of the request (default is None).
    :param request_min: Minimum requests allowed in a rate-limited epoch (default is 10).
    :param request_max: Maximum requests allowed in a rate-limited epoch (default is 30).
    :param limit_epoch: Length of the rate-limited epoch in seconds (default is 60).
    :param request_start: Start of the rate-limited epoch (default is None).
    :param json_data: JSON data for the request (default is None).
    :return: Limited response from the ABI URL.
    """
    manager = DynamicRateLimiterManagerSingleton.get_instance()
    if request_type not in manager.services:
        request_manager.add_service(request_type, request_min, request_max, limit_epoch, request_start,epoch_cycle_adjustment=epoch_cycle_adjustment)
    return get_limited_request(request_url=request_url, service_name=request_type)
def get_response(request=None):
    """
    Parse the JSON response and return the ABI.

    :return: Parsed ABI response.
    """
    if "result" in request:
        return safe_json_loads(request["result"])
    return safe_json_loads(request)

while True:
    abi = get_request(request_url="https://api.coingecko.com/api/v3/simple/price?ids=usdc&vs_currencies=usd",request_min=15,request_max=30,limit_epoch=60,request_start=30,epoch_cycle_adjustment=5)
    print(abi)
