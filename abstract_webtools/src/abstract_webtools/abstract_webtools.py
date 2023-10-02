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
# -*- coding: UTF-8 -*-
import requests
import os
# Google Chrome Driver
from selenium import webdriver
import yt_dlp
import ssl
import requests
from requests.adapters import HTTPAdapter
from typing import Optional, List
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from urllib.parse import urlparse
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from abstract_utilities.time_utils import get_time_stamp,get_sleep,sleep_count_down
from abstract_utilities.string_clean import eatInner,eatAll
logging.basicConfig(level=logging.INFO)
class DynamicRateLimiterManager:
    def __init__(self):
        # Key: Service Name, Value: DynamicRateLimiter instance
        self.services = {}
    
    def add_service(self, service_name="default", low_limit=10, high_limit=30, limit_epoch=60,starting_tokens=10,epoch_cycle_adjustment=True):
        if service_name in self.services:
            print(f"Service {service_name} already exists!")
            return
        self.services[service_name] = DynamicRateLimiter(service_name=service_name, low_limit=low_limit, high_limit=limit_epoch, limit_epoch=60,starting_tokens=starting_tokens,epoch_cycle_adjustment=epoch_cycle_adjustment)
    
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
    def get_instance(service_name="default", low_limit=10, high_limit=30, limit_epoch=60,starting_tokens=10,epoch_cycle_adjustment=True):
        if DynamicRateLimiterManagerSingleton._instance is None:
            DynamicRateLimiterManagerSingleton._instance = DynamicRateLimiterManager(service_name=service_name, low_limit=low_limit, high_limit=limit_epoch, limit_epoch=60,starting_tokens=starting_tokens,epoch_cycle_adjustment=epoch_cycle_adjustment)
        return DynamicRateLimiterManagerSingleton._instance

class CipherManager:
    @staticmethod
    def  get_default_ciphers()-> list:
        return [
            "ECDHE-RSA-AES256-GCM-SHA384", "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-SHA384", "ECDHE-ECDSA-AES256-SHA384",
            "ECDHE-RSA-AES256-SHA", "ECDHE-ECDSA-AES256-SHA",
            "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-AES128-SHA256",
            "ECDHE-ECDSA-AES128-GCM-SHA256", "ECDHE-ECDSA-AES128-SHA256",
            "AES256-SHA", "AES128-SHA"
        ]

    def __init__(self,cipher_list=None):
        if cipher_list == None:
            cipher_list=self.get_default_ciphers()
        self.cipher_list = cipher_list
        self.create_list()
        self.ciphers_string = self.add_string_list()
    def add_string_list(self):
        if len(self.cipher_list)==0:
            return ''
        return','.join(self.cipher_list)
    def create_list(self):
        if self.cipher_list == None:
            self.cipher_list= []
        elif isinstance(self.cipher_list, str):
            self.cipher_list=self.cipher_list.split(',')
        if isinstance(self.cipher_list, str):
            self.cipher_list=[self.cipher_list]
class CipherManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(cipher_list=None):
        if CipherManagerSingleton._instance is None:
            CipherManagerSingleton._instance = CipherManager(cipher_list=cipher_list)
        elif CipherManagerSingleton._instance.cipher_list != cipher_list:
            CipherManagerSingleton._instance = CipherManager(cipher_list=cipher_list)
        return CipherManagerSingleton._instance
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
    def get_context(ciphers=None, options=None, cert_reqs=None):
        
        return ssl_.create_urllib3_context(ciphers=ciphers, cert_reqs=cert_reqs, options=options)

    def __init__(self, ciphers=None, ssl_options_list=None, certification=None):
        self.ssl_options_list = ssl_options_list
        self.create_list()
        self.ssl_options_values = self.get_options_values()
        self.ssl_options = self.combine_ssl_options()
        self.certification = certification or self.get_default_certification()
        self.cipher_manager = CipherManagerSingleton().get_instance(cipher_list=ciphers)
        self.ssl_context = self.get_context(ciphers=self.cipher_manager.ciphers_string, options=self.ssl_options, cert_reqs=self.certification)
    def create_list(self):
        if self.ssl_options_list == None:
            self.ssl_options_list= []
        elif isinstance(self.ssl_options_list, str):
            self.ssl_options_list=self.ssl_options_list.split(',')
        if isinstance(self.ssl_options_list, str):
            self.ssl_options_list=[self.ssl_options_list]
    def get_options_values(self):
        return [getattr(ssl, option_name) for option_name in self.ssl_options_list]
    def combine_ssl_options(self):
        combined_options = 0
        for option in self.ssl_options_values:
            combined_options |= option
        return combined_options
class SSLManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(ciphers=None, ssl_options_list=None, certification=None):
        if SSLManagerSingleton._instance is None:
            SSLManagerSingleton._instance = SSLManager(ciphers=ciphers, ssl_options_list=ssl_options_list, certification=certification)
        elif SSLManagerSingleton._instance.cipher_manager.ciphers_string != ciphers or SSLManagerSingleton._instance.ssl_options_list !=ssl_options_list or SSLManagerSingleton._instance.certification !=certification:
            SSLManagerSingleton._instance = SSLManager(ciphers=ciphers, ssl_options_list=ssl_options_list, certification=certification)
        return SSLManagerSingleton._instance
class TLSAdapter(HTTPAdapter):
    def __init__(self, ciphers: Optional[List[str]] = None, certification: Optional[str] = None, ssl_options: Optional[List[str]] = None):
        super().__init__()
        self.ciphers = ciphers
        self.certification = certification
        self.ssl_options = ssl_options
        
        self.cipher_manager = CipherManagerSingleton.get_instance(cipher_list=self.ciphers)
        self.ssl_manager = SSLManagerSingleton.get_instance(
            ciphers=self.cipher_manager.ciphers_string, 
            ssl_options_list=ssl_options, 
            certification=certification
        )
        self.ssl_context = self.ssl_manager.ssl_context

    def init_poolmanager(self, *args, **kwargs):
        return super().init_poolmanager(*args, **kwargs)


class TLSAdapterSingleton:
    _instance = None
    @staticmethod
    def get_instance(ciphers=None, certification=None, ssl_options=None):
        if TLSAdapterSingleton._instance is None:
            TLSAdapterSingleton._instance = TLSAdapter(ciphers=ciphers, certification=certification, ssl_options=ssl_options)
        elif TLSAdapterSingleton._instance.ciphers != ciphers or SSLManagerSingleton._instance.certification !=certification or SSLManagerSingleton._instance.ssl_options_list !=ssl_options:
            TLSAdapterSingleton._instance = TLSAdapter(ciphers=ciphers, certification=certification, ssl_options=ssl_options)
        return TLSAdapterSingleton._instance
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
        self.user_agent = user_agent
        self.user_agent_header=self.get_user_agent(user_agent=user_agent)
class UserAgentManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(user_agent=UserAgentManager.desktop_user_agents()[0]):
        if UserAgentManagerSingleton._instance is None:
            UserAgentManagerSingleton._instance = UserAgentManager(user_agent=user_agent)
        elif UserAgentManagerSingleton._instance.user_agent != user_agent:
            UserAgentManagerSingleton._instance = UserAgentManager(user_agent=user_agent)
        return UserAgentManagerSingleton._instance
class SafeRequest:
    user_agent_manager = UserAgentManagerSingleton().get_instance()
    def __init__(self,
                 url=None,
                 service_name="default",
                 headers:dict=user_agent_manager.user_agent_header,
                 max_retries=3,
                 last_request_time=None,
                 request_wait_limit=1.5,
                 ):
        self.url =url 
        if isinstance(headers,str):
            headers = UserAgentManagerSingleton().get_instance(user_agent=headers).user_agent_header
        self.headers = headers
        self.max_retries=max_retries
        
        self.request_wait_limit = request_wait_limit
        
        self.url_manager = URLManagerSingleton().get_instance(url=url)
        self.session = self.initialize_session()
        
        self.last_request_time = last_request_time

        self.response = self.make_request()
        
        self.status_code = None if self.response ==  None else self.response.status_code
        
        self.source_code = '' if self.response == None else self.response.text
        self.react_source_code = []
        self.get_react_source_code()
    def initialize_session(self):
        s = requests.Session()
        s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
        s.headers.update(self.headers)
        # Add any other headers or cookie settings here
        adapter = TLSAdapterSingleton().get_instance()
        s.mount('https://', adapter)
        return s
    @staticmethod
    def get_response(response):
        if response.headers.get('content-type') == 'application/json':
            data = safe_json_loads(response.text)
            if data:
                return data.get("response", data)
        return response.text
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
    def wait_between_requests(self):
        """
        Wait between requests based on the request_wait_limit.
        """
        if self.last_request_time:
            sleep_time = self.request_wait_limit - (get_time_stamp() - self.last_request_time)
            if sleep_time > 0:
                logging.info(f"Sleeping for {sleep_time:.2f} seconds.")
                get_sleep(sleep_time)

    def make_request(self, last_request_time=None, request_wait_limit=None):
        """
        Make a request and handle potential errors.
        """
        # Update the instance attributes if they are passed
        if last_request_time is not None:
            self.last_request_time = last_request_time
        if request_wait_limit is not None:
            self.request_wait_limit = request_wait_limit
            
        
        self.wait_between_requests()
        
        for _ in range(self.max_retries):
            try:
                self.response = self.try_request()  # 10 seconds timeout
                if self.response.status_code == 200:
                    self.last_request_time = get_time_stamp()
                    return self.response
                elif response.status_code == 429:
                    logging.warning(f"Rate limited by {self.url_manager.correct_url}. Retrying...")
                    get_sleep(5)  # adjust this based on the server's rate limit reset time
            except requests.Timeout as e:
                logging.error(f"Request to {cleaned_url} timed out: {e}")
            except requests.ConnectionError:
                logging.error(f"Connection error for URL {self.url_manager.correct_url}.")
            except requests.Timeout:
                logging.error(f"Request timeout for URL {self.url_manager.correct_url}.")
            except requests.RequestException as e:
                logging.error(f"Request exception for URL {self.url_manager.correct_url}: {e}")

        logging.error(f"Failed to retrieve content from {self.url_manager.correct_url} after {self.max_retries} retries.")
        return None
    def try_request(self,timeout=10) -> (requests.Response or None):
        """
        Tries to make an HTTP request to the given URL using the provided session.

        Args:
            url (str): The URL to make the request to.
            session (type(requests.Session), optional): The requests session to use for making HTTP requests.
                Defaults to requests.

        Returns:
            requests.Response or None: The response object if the request is successful, or None if the request fails.
        """
        try:
            self.request = self.session.get(url=self.url_manager.correct_url, timeout=10)
            return self.request
        except requests.exceptions.RequestException as e:
            print(e)
        return False
    def get_source_code(self, url=None,response=None):
        if self.response:
            return get_response(self.response)
        else:
            logging.error(f"Invalid URL: {url}")
            return None
        self.clean_url(self.url_manager.correct_url)
    def get_react_source_code(self) -> list:
        """
        Fetches the source code of the specified URL and extracts JavaScript and JSX source code (React components).

        Args:
            url (str): The URL to fetch the source code from.

        Returns:
            list: A list of strings containing JavaScript and JSX source code found in <script> tags.
        """
        if  self.url_manager.correct_url is None:
            return []
        soup_manager = SoupManagerSingleton().get_instance(url=self.url_manager.correct_url,source_code=self.source_code)
        script_tags = soup_manager.soup.find_all('script', type=lambda t: t and ('javascript' in t or 'jsx' in t))
        for script_tag in script_tags:
            self.react_source_code.append(script_tag.string)
    def get_limited_request(self,request_url=str,service_name="default"):
        manager = DynamicRateLimiterManagerSingleton.get_instance()  # Get the singleton instance
        unwanted_response=True
        # Check with the rate limiter if we can make a request
        while True:
            if not manager.request(service_name):
                print("Rate limit reached for coin_gecko. Waiting for the next epoch...")
                sleep_count_down(manager.services[service_name].get_sleep()["current_sleep"])  # Wait for the limit_epoch duration
            # Make the actual request
            response = try_request(request_url=request_url)
            
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

class SafeRequestSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,headers:dict=UserAgentManager().user_agent_header,max_retries=3,last_request_time=None,request_wait_limit=1.5):
        if SafeRequestSingleton._instance is None:
            SafeRequestSingleton._instance = SafeRequest(url=url,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        elif SafeRequestSingleton._instance.url != url or SafeRequestSingleton._instance.headers != headers or SafeRequestSingleton._instance.max_retries != max_retries or SafeRequestSingleton._instance.request_wait_limit != request_wait_limit:
            SafeRequestSingleton._instance = SafeRequest(url=url,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        return SafeRequestSingleton._instance
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
class URLManager:
    def __init__(self,url=None,session=requests):
        self.url = url
        self.session = session
        self.striped_url = None if url ==  None else self.strip_web()
        self.clean_urls = None if url ==  None else self.clean_url(url=self.url)
        self.correct_url = None if url ==  None else self.get_correct_url()
        self.domain_name = None if url ==  None else self.get_domain_name(self.correct_url)
        self.all_urls=[]
    def strip_web(self) -> str:
        """
        Strip the 'http://' or 'https://' prefix from a URL, if present.

        Parameters:
        url (str): The URL string to process.

        Returns:
        str: The URL string with the prefix removed.
        """
        url = self.url
        if self.url.startswith("http://"):
            url = self.url.replace("http://", '', 1)
        elif self.url.startswith("https://"):
            url = self.url.replace("https://", '', 1)
        return url
    @staticmethod
    def clean_url(url: str) -> list:
        """
        Given a URL, return a list with potential URL versions including with and without 'www.', 
        and with 'http://' and 'https://'.
        """
        # Remove http:// or https:// prefix
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

        # Add variants with 'www' if it wasn't present
        else:
            urls.extend([
                f"https://www.{cleaned}",
                f"http://www.{cleaned}",
            ])

        return urls

    def get_correct_url(self) -> (str or None):
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
        for url in self.clean_urls:
            try:
                source = self.session.get(url)
                return url
            except requests.exceptions.RequestException as e:
                print(e)
        return None

    def get_all_website_links(self,url=None,tag="a",class_name="href") -> list:
        """
        Returns all URLs that are found on the specified URL and belong to the same website.

        Args:
            url (str): The URL to search for links.

        Returns:
            list: A list of URLs that belong to the same website as the specified URL.
        """
        if url==None:
            url = self.correct_url
        if url is None:
            return []
        all_desired=SoupManagerSingleton().get_instance(url=url).get_all_desired(tag=tag,class_name=class_name)
        for tag in all_desired:
            href = tag.attrs.get(class_name)
            if href == "" or href is None:
                # href empty tag
                continue
            href=self.get_relative_href(self.correct_url,href)
            if not self.is_valid_url(href):
                # not a valid URL
                continue
            if href in self.all_urls:
                # already in the set
                continue
            if self.domain_name not in href:
                # external link
                continue
            self.all_urls.append(href)
        return self.all_urls
    @staticmethod
    def get_domain_name(url):
        return urlparse(url).netloc
    @staticmethod
    def is_valid_url(url):
        """
        Check if the given URL is valid.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    @staticmethod
    def get_relative_href(url,href):
        # join the URL if it's relative (not an absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        return href

class URLManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,session=requests):
        if URLManagerSingleton._instance is None:
            URLManagerSingleton._instance = URLManager(url=url,session=session)
        elif URLManagerSingleton._instance.session != session or URLManagerSingleton._instance.url != url:
            URLManagerSingleton._instance = URLManager(url=url,session=session)
        return URLManagerSingleton._instance

class VideoDownloader:
    
    def __init__(self, url,title=None,download_directory=os.getcwd(),user_agent=None,video_extention='mp4'):
        self.url = url
        self.video_extention=video_extention
        self.header = UserAgentManagerSingleton().get_instance(user_agent=user_agent).user_agent_header
        self.base_name = os.path.basename(self.url)
        self.file_name,self.ext = os.path.splitext(self.base_name)
        self.download_directory=download_directory
        self.title = url.split('/')[3] if title == None else title
        self.video_urls = []
        self.fetch_video_urls()
        self.download_videos()
    def fetch_video_urls(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        self.page_source = driver.page_source
        for each in self.page_source.split('<source ')[1:]:
            # NOTE: Make sure to import the `eatAll` function and use it here.
            self.video_urls.append(eatInner(each.split('.{self.video_extention}'.replace('..','.'))[0].split('http')[-1],['h','t','t','p','s',':','//','/','s','=',' ','\n','\t',''])+'.mp4')
    def download_videos(self):
        for video_url in self.video_urls:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url)
                self.base_name = os.path.basename(info['url'])
                self.file_name,self.ext = os.path.splitext(self.base_name)
                video_content =SafeRequestSingleton().get_instance(url=info['url']).response
                print("Start downloading")
                content_length = int(video_content.headers['content-length'])
                print(f'Size: {content_length / 1024 / 1024:.2f}MB')
                down_size = 0
                with open(f'{os.path.join(self.download_directory,self.base_name)}', "wb") as video:
                    for chunk in video_content.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            video.write(chunk)
                            down_size += len(chunk)
                            print(f'Progress: {down_size / content_length:.2%}', end='\r')
class VideoDownloaderSingleton():
    _instance = None
    @staticmethod
    def get_instance(url,title=None,video_extention='mp4',download_directory=os.getcwd(),user_agent=None):
        if VideoDownloaderSingleton._instance is None:
            VideoDownloaderSingleton._instance = VideoDownloader(url=url,parse_type=parse_type)
        elif VideoDownloaderSingleton._instance.title != title or video_extention != VideoDownloaderSingleton._instance.video_extention or url != VideoDownloaderSingleton._instance.url or download_directory != VideoDownloaderSingleton._instance.download_directory or user_agent != VideoDownloaderSingleton._instance.user_agent:
            VideoDownloaderSingleton._instance = VideoDownloader(url=url,parse_type=parse_type)
        return VideoDownloaderSingleton._instance
class SoupManager:
    def __init__(self,url=None,source_code=None,parse_type="html.parser"):
        self.url = url
        self.source_code = source_code
        self.parse_type = parse_type
        if self.source_code ==None:
            if self.url != None:
                self.url_manager =  URLManagerSingleton().get_instance(url=url)
                self.request_manager = SafeRequestSingleton().get_instance(url=self.url_manager.correct_url)
                self.source_code = self.request_manager.source_code
            else:
                return
        self.soup = BeautifulSoup(self.source_code, self.parse_type)
        self.all_tags = self.find_all(element=True)
        self.class_names,self.class_values,self.tag_names,self.meta_tags,self.attribute_tracker_js= [],[],[],{},{}
        self.get_all_class_and_values()
        self.get_meta_tags()
        self.all_urls=[]
    def get_all_desired(self, tag=None, class_name=None, class_value=None):
        if not tag:
            tags = self.soup.find_all(True)  # get all tags
        else:
            tags = self.soup.find_all(tag)  # get specific tags
        extracted_tags = []
        for tag in tags:
            if class_name:
                attribute_value = tag.get(class_name)
                if not attribute_value:  # skip tags without the desired attribute
                    continue
                if class_value and class_value not in attribute_value:  # skip tags without the desired attribute value
                    continue
            extracted_tags.append(tag)
        # For debugging:
        return extracted_tags
    def get_tag_name(self,tag):
        return eatAll(str(tag)[1:].split('>')[0].split(' ')[0],[' ','','\n','\t','/','\\'])
    def if_not_append(self,obj,list_obj):
        if obj not in list_obj:
            list_obj.append(obj)
        return list_obj
    def find_all(self,element,soup=None):
        soup = self.soup if soup == None else soup
        return soup.find_all(element)
    def get_class(self,class_name,soup=None):
        soup = self.soup if soup == None else soup
        return soup.get(class_name)
    @staticmethod
    def has_attributes(tag, *attrs):
        return any(tag.has_attr(attr) for attr in attrs)

    def get_find_all_with_attributes(self, *attrs):
        return self.soup.find_all(lambda t: self.has_attributes(t, *attrs))

    def get_meta_tags(self):
        tags = self.find_all("meta")
        for meta_tag in tags:
            for attr, values in meta_tag.attrs.items():
                if attr not in self.meta_tags:
                    self.meta_tags[attr] = []
                if values not in self.meta_tags[attr]:
                    self.meta_tags[attr].append(values)
    def get_all_class_and_values(self):
        for tag in self.all_tags:
            tag_name = self.get_tag_name(tag)
            self.tag_names=self.if_not_append(tag_name,self.tag_names)
            for attr, values in tag.attrs.items():
                self.class_names=self.if_not_append(attr,self.class_names)
                if attr not in self.attribute_tracker_js:
                    self.attribute_tracker_js[attr] = {"class_values":[],"tags":[]}
                if tag_name not in self.attribute_tracker_js[attr]["tags"]:
                    self.attribute_tracker_js[attr]["tags"].append(tag_name)
                # If the attribute has a single value (like "id"), append it directly.
                # If it has multiple values (like "class" when there's more than one class), append them individually.
                if isinstance(values,str):
                    values = [values]
                if isinstance(values, list):
                    for value in values:
                        self.class_values=self.if_not_append(value, self.class_values)
                        if value not in self.attribute_tracker_js[attr]["class_values"]:
                            self.attribute_tracker_js[attr]["class_values"].append(value)
    def extract_elements(url:str=None, tag:str=None, class_name:str=None, class_value:str=None) -> list:
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
        if self.soup is None:
            return [], [], [], []
        elements = []
        # If no filters are provided, return the entire source code
        if not tag and not class_name and not class_value:
            elements.append(str(soup))
            return elements
        # Find elements based on the filters provided
        if tag:
            elements.extend([str(tags) for tags in self.get_all_desired(tag)])
        if attribute_name:
            elements.extend([str(tags) for tags in self.get_all_desired(attrs={attribute_name: True})])
        if class_name:
            elements.extend([str(tags) for tags in self.get_all_desired(class_name=class_name)])
        return elements
    def find_all_with_attributes(soup,class_name, *attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes.

        Args:
            base_url (str): The URL from which to discover classes.

        Returns:
            set: A set of unique class names.
        """
        unique_classes = set()
        for tag in self.get_find_all_with_attributes(attrs=attrs):
            class_list=self.get_class(class_name=class_name,soup=tag)
            unique_classes.update(class_list)
        return unique_classes
    def get_images(self,tag_name,class_name,class_value):
        images = []
        for tag in soup.find_all(tag_name):
            if class_name in tag.attrs and tag.attrs[class_name] == class_value:
                content = tag.attrs.get('content', '')
                if content:
                    images.append(content)
        return images
    def discover_classes_and_meta_images(self,tag_name,class_name_1,class_name_2,class_value,attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes. Also, fetches 
        image references from meta tags.

        Args:
            base_url (str): The URL from which to discover classes and meta images.

        Returns:
            tuple: A set of unique class names and a list of meta images.
        """

        unique_classes=find_all_with_attributes(soup=self.soup,class_name=class_name_1, *attrs)
        
        images=get_images(self,soup=self.soup,tag_name=tag_name,class_name=class_name_2,class_value=class_value)
        return unique_classes, images

    
class SoupManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url=None,parse_type="html.parser",source_code=None):
        if SoupManagerSingleton._instance is None:
            SoupManagerSingleton._instance = SoupManager(url=url,parse_type=parse_type,source_code=source_code)
        elif parse_type != SoupManagerSingleton._instance.parse_type or url != SoupManagerSingleton._instance.url  or source_code != SoupManagerSingleton._instance.source_code:
            SoupManagerSingleton._instance = SoupManager(url=url,parse_type=parse_type,source_code=source_code)
        return SoupManagerSingleton._instance
def CrawlManager():
    def __init__(self,url=None,source_code=None,parse_type="html.parser"):
        self.url=url
        self.source_code=source_code
        self.parse_type=parse_type
        get_new_source_and_url(self,url)
        self.all_site_links = self.url_manager.get_all_website_links(domain=self.url_manager.domain)
    def get_new_source_and_url(self,url=None):
        if url == None:
            url = self.url
        
        self.url=self.url_manager.corrct_url
        self.response_manager= SafeRequest().get_instance(url=self.url)
        self.response = self.response_manager.response
        self.source_code=self.response_manager.source_code
        self.soup_manager = SoupManagerSingleton().get_instance(source_code=self.response_manager.source_code)
        self.soup=  self.soup_manager.soup
    def get_classes_and_meta_info():
        class_name_1,class_name_2, class_value = 'meta','class','property','og:image'
        attrs = 'href','src'
        unique_classes, images=discover_classes_and_images(self,tag_name,class_name_1,class_name_2,class_value,attrs)
        return unique_classes, images
    def extract_links_from_url(self):
        """
        Extracts all href and src links from a given URL's source code.

        Args:
            base_url (str): The URL from which to extract links.

        Returns:
            dict: Dictionary containing image links and external links under the parent page.
        """
        agg_js = {'images':[],'external_links':[]}
        
        if self.response != None:
            attrs = 'href','src'
            href_links,src_links='',''
            links = [href_links,src_links]
            for i,each in enumerate(attrs):
                 links[i]= [a[attr[i]] for a in get_find_all_with_attributes(self, attrs[i])]
            # Convert all links to absolute links
            absolute_links = [urljoin(url, link) for link in links[0] + links[1]]
            # Separate images and external links
            images = [link for link in absolute_links if link.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
            external_links = [link for link in absolute_links if urlparse(link).netloc != urlparse(url).netloc]
            agg_js['images']=images
            agg_js['external_links']=external_links
           
        return agg_js


    def correct_xml(xml_string):
        # Parse the XML string
        root = ET.fromstring(xml_string)

        # Loop through each <image:loc> element and correct its text if needed
        for image_loc in root.findall(".//image:loc", namespaces={'image': 'http://www.google.com/schemas/sitemap-image/1.1'}):
            # Replace '&' with '&amp;' in the element's text
            if '&' in image_loc.text:
                image_loc.text = image_loc.text.replace('&', '&amp;')

        # Convert the corrected XML back to string
        corrected_xml = ET.tostring(root, encoding='utf-8').decode('utf-8')
        return corrected_xml


    def determine_values(self):
        # This is just a mockup. In a real application, you'd analyze the URL or its content.

        # Assuming a blog site
        if 'blog' in self.url:
            if '2023' in self.url:  # Assuming it's a current year article
                return ('weekly', '0.8')
            else:
                return ('monthly', '0.6')
        elif 'contact' in self.url:
            return ('yearly', '0.3')
        else:  # Homepage or main categories
            return ('weekly', '1.0')
    def crawl(url, max_depth=3, depth=1):
        
        if depth > max_depth:
            return []

        if url in visited:
            return []

        visited.add(url)

        try:
            
            links = [a['href'] for a in self.soup.find_all('a', href=True)]
            valid_links = []

            for link in links:
                parsed_link = urlparse(link)
                base_url = "{}://{}".format(parsed_link.scheme, parsed_link.netloc)
            
                if base_url == url:  # Avoiding external URLs
                    final_link = urljoin(url, parsed_link.path)
                    if final_link not in valid_links:
                        valid_links.append(final_link)

            for link in valid_links:
                crawl(link, max_depth, depth+1)

            return valid_links

        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []


    # Define or import required functions here, like get_all_website_links, determine_values, 
    # discover_classes_and_meta_images, and extract_links_from_url.
    def get_meta_info(self):
        
        meta_info = {}
        # Fetch the title if available
        title_tag = self.soup.title
        if title_tag:
            meta_info["title"] = title_tag.string
        
        # Fetch meta tags
        for meta_tag in soup.find_all('meta'):
            name = meta_tag.get('name') or meta_tag.get('property')
            if name:
                content = meta_tag.get('content')
                if content:
                    meta_info[name] = content

        return meta_info
    def generate_sitemap(self,domain):
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            string = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            
            for url in self.all_site_links:
                string += f'  <url>\n    <loc>{url}</loc>\n'
                preprocess=[]
                self.get_new_source_and_url(url=url)
                links = extract_links_from_url(url)
                
                for img in links['images']:
                    if str(img).lower() not in preprocess:
                        try:
                            escaped_img = img.replace('&', '&amp;')

                            str_write = f'    <image:image>\n      <image:loc>{escaped_img}</image:loc>\n    </image:image>\n'
                            string += str_write
                        except:
                            pass
                        preprocess.append(str(img).lower())
                frequency, priority = determine_values(url)
                string += f'    <changefreq>{frequency}</changefreq>\n'
                string += f'    <priority>{priority}</priority>\n'
                string += f'  </url>\n'
                
            string += '</urlset>\n'
            f.write(string)            
        # Output summary
        print(f'Sitemap saved to sitemap.xml with {len(urls)} URLs.')
        
        # Output class and link details
        for url in urls:
            input(get_meta_info(url))
            print(f"\nDetails for {url}:")
            classes, meta_img_refs = discover_classes_and_meta_images(url)

            print("\nClasses with href or src attributes:")
            for class_name in classes:
                print(f"\t{class_name}")
            
            print("\nMeta Image References:")
            for img_ref in meta_img_refs:
                print(f"\t{img_ref}")
            
            links = extract_links_from_url(url)

            print("\nImages:")
            for img in links['images']:
                print(f"\t{img}")
            
            print("\nExternal Links:")
            for ext_link in links['external_links']:
                print(f"\t{ext_link}")
class CrawlManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url=None,source_code=None,parse_type="html.parser"):
        if CrawlManagerSingleton._instance is None:
            CrawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        elif parse_type != CrawlManagerSingleton._instance.parse_type or url != CrawlManagerSingleton._instance.url  or source_code != CrawlManagerSingleton._instance.source_code:
            CrawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        return CrawlManagerSingleton._instance

input(SafeRequestSingleton().get_instance(url='https://thedailydialectics.com').source_code)
