import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
import requests
from urllib.parse import urlparse
import logging
import xml.etree.ElementTree as ET
from abstract_utilities.time_utils import get_time_stamp,get_sleep,sleep_count_down
logging.basicConfig(level=logging.INFO)
class DynamicRateLimiterManager:
    def __init__(self):
        # Key: Service Name, Value: DynamicRateLimiter instance
        self.services = {}
    
    def add_service(self, service_name, low_limit, high_limit, limit_epoch, starting_tokens=None):
        if service_name in self.services:
            print(f"Service {service_name} already exists!")
            return
        self.services[service_name] = DynamicRateLimiter(low_limit, high_limit, limit_epoch, starting_tokens)
    
    def request(self, service_name):
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not found!")
        
        limiter = self.services[service_name]
        can_request = limiter.request()
        
        # Log the outcome of the request attempt
        self.log_request(service_name, can_request)
        
        return can_request
    
    def log_request(self, service_name, success):
        # Placeholder logging method, replace with actual logging implementation
        print(f"[{service_name}] Request {'succeeded' if success else 'denied'}. Current tokens: {self.services[service_name].get_current_tokens()}")
class DynamicRateLimiter:
    def __init__(self, low_limit, high_limit, limit_epoch, starting_tokens=None,epoch_cycle_adjustment:int=None):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.limit_epoch = limit_epoch  # in seconds
        self.request_status_json = {"succesful":[],"unsuccesful":[],"last_requested":get_time_stamp(),"first_requested":get_time_stamp(),"epoch_left":self.limit_epoch,"last_fail":get_time_stamp(),"count_since_fail":0}
        self.current_limit = starting_tokens or low_limit  # Default to high_limit if starting_tokens isn't provided
        self.epoch_cycle_adjustment = epoch_cycle_adjustment
        # Additional attributes for tracking adjustment logic
        self.last_adjusted_time = get_time_stamp()
        self.successful_epochs_since_last_adjustment = 0
        self.request_count_in_current_epoch = 0

    def _refill_tokens(self):
        time_since_last_request = get_time_stamp() - self.request_status_json["last_requested"]
        new_tokens = (time_since_last_request / self.limit_epoch) * self.current_limit
        self.tokens = min(self.current_limit, self.get_current_tokens())
    def request_tracker(self,success):
        if success:
            self.request_status_json["succesful"].append(get_time_stamp())
        else:
            self.request_status_json["unsuccesful"].append(get_time_stamp())
            self.request_status_json["last_fail"]=get_time_stamp()
            self.request_status_json["count_since_fail"]=0
            self.adjust_limit()
        self.request_status_json["last_requested"]=get_time_stamp()
    def calculate_tokens(self):
        successful = []
        for each in self.request_status_json["succesful"]:
            if (get_time_stamp() - each)<self.limit_epoch:
                successful.append(each)
        self.request_status_json["succesful"]=successful
        unsuccessful = []
        for each in self.request_status_json["unsuccesful"]:
            if (get_time_stamp() - each)<self.limit_epoch:
                unsuccessful.append(each)
        self.request_status_json["unsuccesful"]=unsuccessful
        if len(successful)==0 and len(unsuccessful)==0:
            pass
        elif len(successful)!=0 and len(unsuccessful)==0:
            self.request_status_json["first_requested"] = successful[0]
        elif len(successful)==0 and len(unsuccessful)!=0:
            self.request_status_json["first_requested"] = unsuccessful[0]
        else:
            self.request_status_json["first_requested"] = min(unsuccessful[0],successful[0])
        self.request_status_json["epoch_left"]=self.limit_epoch-(self.request_status_json["last_requested"]-self.request_status_json["first_requested"])
        
        return self.request_status_json
    def get_current_tokens(self):
        self.request_status_json = self.calculate_tokens()
        total_requests = len(self.request_status_json["succesful"])+len(self.request_status_json["unsuccesful"])
        return max(0,self.current_limit-total_requests)
    def get_sleep(self):
        self.request_status_json = self.calculate_tokens()
        self.request_status_json["current_sleep"]=self.request_status_json["epoch_left"]/max(1,self.get_current_tokens())
        return self.request_status_json
    def request(self):
        self._refill_tokens()
        if self.tokens > 0:
            return True  # The request can be made
        else:
            if self.tokens == 0:
                self.request_status_json["count_since_fail"]+=1
                if self.epoch_cycle_adjustment != None:
                    if self.request_status_json["count_since_fail"] >=self.epoch_cycle_adjustment:
                        self.current_limit=min(self.current_limit+1,self.high_limit)
            return False  # The request cannot be made
    def _adjust_limit(self):
        current_time = get_time_stamp()
        if current_time - self.last_adjusted_time >= self.limit_epoch:
            if len(self.clear_epoch()["succesful"]) >= self.tokens:
                # We hit the rate limit this epoch, decrease our limit
                self.tokens = max(1, self.tokens - 1)
            else:
                self.successful_epochs_since_last_adjustment += 1
                if self.successful_epochs_since_last_adjustment >= 5:
                    # We've had 5 successful epochs, increase our limit
                    self.current_limit = min(self.high_limit, self.tokens + 1)
                    self.successful_epochs_since_last_adjustment = 0
            
            # Reset our counters for the new epoch
            self.last_adjusted_time = current_time
            self.request_count_in_current_epoch = 0
    def adjust_limit(self):
        # Set the tokens to succesful requests_made - 1
        self.tokens = len(self.calculate_tokens()["succesful"])

        # Adjust the high_limit
        self.current_limit = self.tokens

        # Log the adjustment
        print(f"Adjusted tokens to: {self.tokens} and high_limit to: {self.current_limit}")
class DynamicRateLimiterManagerSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        if DynamicRateLimiterManagerSingleton._instance is None:
            DynamicRateLimiterManagerSingleton._instance = DynamicRateLimiterManager()
        return DynamicRateLimiterManagerSingleton._instance

class CipherManager:
    @staticmethod
    def get_default_ciphers() -> list:
        return [
            "ECDHE-RSA-AES256-GCM-SHA384", "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-SHA384", "ECDHE-ECDSA-AES256-SHA384",
            "ECDHE-RSA-AES256-SHA", "ECDHE-ECDSA-AES256-SHA",
            "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-AES128-SHA256",
            "ECDHE-ECDSA-AES128-GCM-SHA256", "ECDHE-ECDSA-AES128-SHA256",
            "AES256-SHA", "AES128-SHA"
        ]

    @staticmethod
    def create_list(lst=None):
        if not lst:
            return []
        elif isinstance(lst, str):
            return lst.split(',')
        return lst

    @staticmethod
    def add_string_list(cipher_list=[], delim=','):
        return delim.join(cipher_list)


class SSLManager:
    @staticmethod
    def get_default_certification():
        return ssl.CERT_REQUIRED

    @staticmethod
    def get_default_tls_options():
        return ["OP_NO_TLSv1", "OP_NO_TLSv1_1", "OP_NO_COMPRESSION"]

    @staticmethod
    def get_all_tls_options() -> int:
        """
        Returns the SSL options to be used when creating the SSL context.
            [
         ssl.OP_SINGLE_ECDH_USE,
         ssl.OP_SINGLE_DH_USE,
         ssl.OP_NO_TLSv1_3,
         ssl.OP_NO_TLSv1_2,
         ssl.OP_NO_TLSv1_1,
         ssl.OP_NO_TLSv1,
         ssl.OP_NO_TICKET,
         ssl.OP_NO_RENEGOTIATION,
         ssl.OP_NO_QUERY_MTU,
         ssl.OP_NO_COMPRESSION,
         ssl.OP_CIPHER_SERVER_PREFERENCE,
         ssl.OP_ALLOW_NO_DHE_KEX,
         ssl.OP_ALL
         ]
         The `ssl` module in the Python standard library provides several constants that you can use to set various SSL options. Here are the available options as of Python 3.9:

        1. `ssl.OP_ALL`:
           - Enables a collection of various bug workaround options.

        2. `ssl.OP_ALLOW_NO_DHE_KEX`:
           - Allow a non-(EC)DHE handshake on a server socket if no suitable security level can be reached.

        3. `ssl.OP_CIPHER_SERVER_PREFERENCE`:
           - Uses the server's cipher ordering preference rather than the client's.

        4. `ssl.OP_NO_COMPRESSION`:
           - Prevents using SSL/TLS compression to avoid CRIME attacks.

        5. `ssl.OP_NO_QUERY_MTU`:
           - Disables automatic querying of kernel for MTU.

        6. `ssl.OP_NO_RENEGOTIATION`:
           - Disallows all renegotiation.

        7. `ssl.OP_NO_TICKET`:
           - Disables use of RFC 5077 session tickets.

        8. `ssl.OP_NO_TLSv1`:
           - Prevents the use of TLSv1.

        9. `ssl.OP_NO_TLSv1_1`:
           - Prevents the use of TLSv1.1.

        10. `ssl.OP_NO_TLSv1_2`:
           - Prevents the use of TLSv1.2.

        11. `ssl.OP_NO_TLSv1_3`:
           - Prevents the use of TLSv1.3.

        12. `ssl.OP_SINGLE_DH_USE`:
           - Always create a new key when using temporary/ephemeral DH parameters. This option provides forward secrecy.

        13. `ssl.OP_SINGLE_ECDH_USE`:
           - Always create a new key when using temporary/ephemeral ECDH parameters. This option provides forward secrecy.

        These constants can be combined using the bitwise OR (`|`) operator to set multiple options. For example, to prevent the use of TLSv1 and TLSv1.1, you would use:
        Please note that the availability of some options might vary depending on the version of OpenSSL that Python's `ssl` module is linked against and the version of Python itself. You can always check the Python documentation specific to your version to get the most accurate and updated list.

        Returns:
            int: The SSL options.

        """
        return [
            "OP_SINGLE_ECDH_USE",
            "OP_SINGLE_DH_USE",
            "OP_NO_TLSv1_3",
            "OP_NO_TLSv1_2",
            "OP_NO_TLSv1_1",
            "OP_NO_TLSv1",
            "OP_NO_TICKET",
            "OP_NO_RENEGOTIATION",
            "OP_NO_QUERY_MTU",
            "OP_NO_COMPRESSION",
            "OP_CIPHER_SERVER_PREFERENCE",
            "OP_ALLOW_NO_DHE_KEX",
            "OP_ALL"
            ]

    @staticmethod
    def create_list(lst=None):
        return CipherManager.create_list(lst)

    @staticmethod
    def combine_ssl_options(ssl_options_values=[]):
        combined_options = 0
        for option in ssl_options_values:
            combined_options |= option
        return combined_options

    @staticmethod
    def get_options_values(ssl_options_list=[]):
        return [getattr(ssl, option_name) for option_name in ssl_options_list]

    @staticmethod
    def get_context(ciphers=None, options=None, cert_reqs=None):
        return ssl_.create_urllib3_context(ciphers=ciphers, cert_reqs=cert_reqs, options=options)

    def __init__(self, ciphers=None, ssl_options_list=None, certification=None):
        self.ssl_options_list = self.create_list(ssl_options_list or self.get_default_tls_options())
        self.ssl_options_values = self.get_options_values(self.ssl_options_list)
        self.ssl_options = self.combine_ssl_options(self.ssl_options_values)
        self.certification = certification or self.get_default_certification()
        self.ssl_context = self.get_context(ciphers=ciphers, options=self.ssl_options, cert_reqs=self.certification)
class TLSAdapter(HTTPAdapter):
    def __init__(self, ciphers=None, certification=None, ssl_options=None):
        ssl_manager = SSLManager(ciphers, ssl_options, certification)
        self.ssl_context = ssl_manager.ssl_context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)
class UserAgentManager:
    @staticmethod
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
    @staticmethod
    def get_user_agent(user_agent:str=desktop_user_agents()[0]) -> dict:
        """
        Returns the user-agent header dictionary with the specified user-agent.

        Args:
            user_agent (str, optional): The user-agent string to be used. Defaults to the first user-agent in the list.

        Returns:
            dict: A dictionary containing the 'user-agent' header.
        """
        return {"user-agent": user_agent}
    def __init__(self,user_agent=desktop_user_agents()[0]):
        self.user_agent=self.get_user_agent(user_agent=user_agent)
class SafeRequest:
    def __init__(self,
                 url=None,
                 headers:dict=UserAgentManager().user_agent,
                 max_retries=3,
                 last_request_time=None,
                 request_wait_limit=1.5,
                 ):
        if isinstance(headers,str):
            get_user_agent(headers)
        self.headers = headers
        self.session = self.initialize_session()
        self.max_retries = max_retries
        self.last_request_time = last_request_time
        self.request_wait_limit = request_wait_limit
        self.url = url
        self.source_code = '' if self.url == None else self.get_source_code(self.url)
        
    def initialize_session(self,user_agent:str= None):
        if isinstance(user_agent,str):
            user_agent = get_user_agent(user_agent)
        s = requests.Session()
        s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
        s.headers.update(self.headers if user_agent==None else user_agent)
        # Add any other headers or cookie settings here
        adapter = TLSAdapter()
        s.mount('https://', adapter)
        return s

    @staticmethod
    def clean_url(url):
        """
        Given a URL, return a list with potential URL versions.
        """
        cleaned = url.replace("http://", "").replace("https://", "")
        no_subdomain = cleaned.replace("www.", "", 1)

        urls = [
            f"https://{cleaned}",
            f"http://{cleaned}",
        ]

        # Add variants without 'www' if it was present
        if cleaned != no_subdomain:
            urls.extend([
                f"https://{no_subdomain}",
                f"http://{no_subdomain}",
            ])

        return urls

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
        url = get_correct_url(url)
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
def get_limited_request(request_url=str,service_name="default"):
    manager = DynamicRateLimiterManagerSingleton.get_instance()  # Get the singleton instance
    unwanted_response=True
    # Check with the rate limiter if we can make a request
    while True:
        if not manager.request(service_name):
            print("Rate limit reached for coin_gecko. Waiting for the next epoch...")
            sleep_count_down(manager.services[service_name].get_sleep()["current_sleep"])  # Wait for the limit_epoch duration
        # Make the actual request
        response = requests.get(request_url)
        
        # If you get a rate-limit error (usually 429 status code but can vary), adjust the rate limiter
        if response.status_code == 429:
            print(response.json())
            manager.services[service_name].request_tracker(False)
            print("Rate limited by coin_gecko. Adjusted limit. Retrying...")
            if len(manager.services[service_name].calculate_tokens()["succesful"])<2:
                sleep_count_down(manager.services[service_name].limit_epoch)  # Wait for the limit_epoch duration
            else:
                manager.services[service_name].current_limit-=1
                sleep_count_down(manager.services[service_name].limit_epoch/len(manager.services[service_name].calculate_tokens()["succesful"]))  # Wait for the limit_epoch duration
        # Return the data if the request was successful
        if response.status_code == 200:
            manager.services[service_name].request_tracker(True)
            return response.json()
        elif response.status_code not in [200,429]:
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

def get_Source_code(url: str ='https://www.example.com' , user_agent:str= UserAgentManager().desktop_user_agents()[0]) -> (str or None):
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

    data = SafeRequest().get_source_code(url=url)
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

