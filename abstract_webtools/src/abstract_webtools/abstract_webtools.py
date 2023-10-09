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
import ssl
import re
import yt_dlp
import threading
import requests
from requests.adapters import HTTPAdapter
from typing import Optional, List,Union
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from urllib.parse import urlparse
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from abstract_utilities.time_utils import get_time_stamp,get_sleep,sleep_count_down
from abstract_utilities.string_clean import eatInner,eatAll
from abstract_utilities.json_utils import convert_to_json
import socket
import shutil
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
    def __init__(self, ciphers=None, ssl_options=None, certification=None):
        self.ciphers = ciphers or "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:AES256-SHA:AES128-SHA"
        self.ssl_options = ssl_options or ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
        self.certification = certification or ssl.CERT_REQUIRED
        self.ssl_context = self.get_context()

    def get_context(self):
        return ssl_.create_urllib3_context(ciphers=self.ciphers, cert_reqs=self.certification, options=self.ssl_options)

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
    def __init__(self, ssl_manager=None,ciphers=None, certification: Optional[str] = None, ssl_options: Optional[List[str]] = None):
        if ssl_manager == None:
            ssl_manager = SSLManager(ciphers=ciphers, ssl_options=ssl_options, certification=certification)
        self.ssl_manager = ssl_manager
        self.ciphers = ssl_manager.ciphers
        self.certification = ssl_manager.certification
        self.ssl_options = ssl_manager.ssl_options
        self.ssl_context = self.ssl_manager.ssl_context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)
class TLSAdapterSingleton:
    _instance: Optional[TLSAdapter] = None
    
    @staticmethod
    def get_instance(ciphers: Optional[List[str]] = None, certification: Optional[str] = None, ssl_options: Optional[List[str]] = None) -> TLSAdapter:
        if (not TLSAdapterSingleton._instance) or (
            TLSAdapterSingleton._instance.ciphers != ciphers or 
            TLSAdapterSingleton._instance.certification != certification or 
            TLSAdapterSingleton._instance.ssl_options != ssl_options
        ):
            TLSAdapterSingleton._instance = TLSAdapter(ciphers=ciphers, certification=certification, ssl_options=ssl_options)
        return TLSAdapterSingleton._instance
class UserAgentManager:
    def __init__(self, user_agent=None):
        if user_agent == None:
            user_agent = self.desktop_user_agents()[0]
        self.user_agent = user_agent
        self.user_agent=self.get_user_agent(self.user_agent)
    @staticmethod
    def desktop_user_agents() -> list:
        return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14']
    @staticmethod
    def big_user_agent_list(n=0):
        from .big_user_agent_list import big_user_agent_list
        return big_user_agent_list[n]
    @staticmethod
    def get_user_agent(user_agent: str = desktop_user_agents()[0]) -> dict:
        if isinstance(user_agent,dict):
            return user_agent
        return {"user-agent": user_agent}
class UserAgentManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(user_agent=UserAgentManager.desktop_user_agents()[0]):
        if UserAgentManagerSingleton._instance is None:
            UserAgentManagerSingleton._instance = UserAgentManager(user_agent=user_agent)
        elif UserAgentManagerSingleton._instance.user_agent != user_agent:
            UserAgentManagerSingleton._instance = UserAgentManager(user_agent=user_agent)
        return UserAgentManagerSingleton._instance
class NetworkManager:
    def __init__(self, user_agent_manager=None,ssl_manager=None, tls_adapter=None,user_agent=None,proxies=None,auth=None,cookies=None,ciphers=None, certification: Optional[str] = None, ssl_options: Optional[List[str]] = None):
        if ssl_manager == None:
            ssl_manager = SSLManager(ciphers=ciphers, ssl_options=ssl_options, certification=certification)
        self.ssl_manager=ssl_manager
        if tls_adapter == None:
            tls_adapter=TLSAdapter(ssl_manager=ssl_manager,ciphers=ciphers, certification=certification, ssl_options=ssl_options)
        self.tls_adapter=tls_adapter
        self.ciphers=tls_adapter.ciphers
        self.certification=tls_adapter.certification
        self.ssl_options=tls_adapter.ssl_options
        self.proxies=None or {}
        self.auth=auth
        self.cookies=cookies or "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
class MySocketClient:
    def __init__(self, ip_address=None, port=None,domain_name=None):
        self.sock
        self.ip_address= ip_address or None
        self.port = port  or None
        
        self.domain_name = domain_name  or None
    def receive_data(self):
        chunks = []
        while True:
            chunk = self.sock.recv(4096)
            if chunk:
                chunks.append(chunk)
            else:
                break
        return b''.join(chunks).decode('utf-8')
    def _parse_socket_response_as_json(self, data, *args, **kwargs):
        return self._parse_json(data[data.find('{'):data.rfind('}') + 1], *args, **kwargs)
    def process_data(self):
        data = self.receive_data()
        return self._parse_socket_response_as_json(data)
    def _parse_json(self,json_string):
        return json.loads(json_string)
    def get_ip(self,domain=None):
        try:
            return self.sock.gethostbyname(domain_name if domain_name != None else self.domain_name)
        except self.sock.gaierror:
            return None
    def grt_host_name(self,ip_address=None):
        return self.sock.gethostbyaddr(ip_address if ip_address != None else self.ip_address)
    def toggle_sock(self):
        if self.sock != None:
            self.sock.close()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if host and socket:
                self.sock.connect((host, port))
class MySocketClient():
    _instance = None
    @staticmethod
    def get_instance(ip_address='local_host',port=22,domain_name="example.com"):
        if MySocketClientSingleton._instance is None:
            MySocketClientSingleton._instance = MySocketClient(ip_address=ip_address,port=port,domain_name=domain_name)
        elif MySocketClientSingleton._instance.ip_address != ip_address or MySocketClientSingleton._instance.port != port or URLManagerSingleton._instance.domain_name != domain_name:
            MySocketClientSingleton._instance = MySocketClient(ip_address=ip_address,port=port,domain_name=domain_name)
        return MySocketClient
def safe_json_loads(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
def convert_to_json(obj):
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        return safe_json_loads(obj)
    return None
class URLManager:
    def __init__(self, url=None, session=requests):
        if url==None:
            url='www.example.com'
        self.url = url
        self.session = session
        # These methods seem essential for setting up the URLManager object.
        self.clean_urls = self.clean_url()
        self.correct_url = self.get_correct_url()
        self.url_to_pieces()
        self.url = url =self.correct_url
        self.url_to_pieces()
        self.all_urls = []
    def url_to_pieces(self):
        match = re.match(r'^(https?):\/\/([^\/]+)(\/[^?]+)?(\?.+)?', self.url)
        if match:
            self.protocol = match.group(1)
            self.domain_name = match.group(2)
            self.path = match.group(3) if match.group(3) else ""  # Handle None
            self.query = match.group(4) if match.group(4) else ""  # Handle None
    def clean_url(self,url=None) -> list:
        """
        Given a URL, return a list with potential URL versions including with and without 'www.', 
        and with 'http://' and 'https://'.
        """
        if url == None:
            url=self.url
        if url:
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

    def get_correct_url(self,url=None,clean_urls=None) -> (str or None):
        """
        Gets the correct URL from the possible variations by trying each one with an HTTP request.

        Args:
            url (str): The URL to find the correct version of.
            session (type(requests.Session), optional): The requests session to use for making HTTP requests.
                Defaults to requests.

        Returns:
            str: The correct version of the URL if found, or None if none of the variations are valid.
        """
        if url!=None and clean_urls==None:
            clean_urls=self.clean_url(url)
        if url == None:
            url=self.url
        if clean_urls==None:
            clean_urls=self.clean_urls
        # Get the correct URL from the possible variations
        for url in clean_urls:
            try:
                source = self.session.get(url)
                return url
            except requests.exceptions.RequestException as e:
                print(e)
        return None
    def update_url(self,url):
        # These methods seem essential for setting up the URLManager object.
        self.url = url
        self.clean_urls = self.clean_url()
        self.correct_url = self.get_correct_url()
        self.url_to_pieces()
        self.url = url =self.correct_url
        self.all_urls = []
    def get_domain_name(self,url):
        return urlparse(url).netloc
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, new_url):
        self._url = new_url
    @staticmethod
    def is_valid_url(url):
        """
        Check if the given URL is valid.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    @staticmethod
    def make_valid(href,url):
        def is_valid_url(url):
            """
            Check if the given URL is valid.
            """
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        if is_valid_url(href):
            return href
        new_link=urljoin(url,href)
        if is_valid_url(new_link):
            return new_link
        return False
    @staticmethod
    def get_relative_href(url,href):
        # join the URL if it's relative (not an absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        return href
    def get_domain(url):
        """
        This implementation is inconsistent, but is kept for compatibility.
        Use this only for "webpage_url_domain"
        """
        return remove_start(urllib.parse.urlparse(url).netloc, 'www.') or None


    def url_basename(url):
        path = urllib.parse.urlparse(url).path
        return path.strip('/').split('/')[-1]


    def base_url(url):
        return re.match(r'https?://[^?#]+/', url).group()


    def urljoin(base, path):
        if isinstance(path, bytes):
            path = path.decode()
        if not isinstance(path, str) or not path:
            return None
        if re.match(r'^(?:[a-zA-Z][a-zA-Z0-9+-.]*:)?//', path):
            return path
        if isinstance(base, bytes):
            base = base.decode()
        if not isinstance(base, str) or not re.match(
                r'^(?:https?:)?//', base):
            return None
        return urllib.parse.urljoin(base, path)
class URLManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,session=requests):
        if URLManagerSingleton._instance is None:
            URLManagerSingleton._instance = URLManager(url,session=session)
        elif URLManagerSingleton._instance.session != session or URLManagerSingleton._instance.url != url:
            URLManagerSingleton._instance = URLManager(url,session=session)
        return URLManagerSingleton._instance
class SafeRequest:
    def __init__(self,
                 url=None,
                 url_manager=None,
                 network_manager=None,
                 user_agent_manager=None,
                 ssl_manager=None,
                 tls_adapter=None,
                 user_agent=None,
                 proxies=None,
                 headers=None,
                 auth=None,
                 cookies=None,
                 session=None,
                 adapter=None,
                 protocol=None,
                 ciphers=None,
                 certification=None,
                 ssl_options=None,
                 stream=False,
                 timeout = None,
                 last_request_time=None,
                 max_retries=None,
                 request_wait_limit=None):
        if url_manager == None:
            url_manager = URLManager(url=url)
        self.url_manager=url_manager
        if network_manager == None:
            network_manager=NetworkManager(user_agent_manager=user_agent_manager,ssl_manager=ssl_manager, tls_adapter=tls_adapter,user_agent=user_agent,proxies=proxies,auth=auth,cookies=cookies,ciphers=ciphers, certification=certification, ssl_options=ssl_options)
        if user_agent_manager == None:
            user_agent_manager = UserAgentManager(user_agent=user_agent)
        self.user_agent_manager = user_agent_manager
        self.user_agent= self.user_agent_manager.user_agent   
        self.network_manager = network_manager
        self.stream=stream
        self.tls_adapter=self.network_manager.tls_adapter
        self.ciphers=self.network_manager.ciphers
        self.certification=self.network_manager.certification
        self.ssl_options=self.network_manager.ssl_options
        self.proxies=self.network_manager.proxies
        self.auth=self.network_manager.auth
        self.timeout=timeout
        self.cookies=self.network_manager.cookies
        self.session = session or requests.session()
        self.protocol=protocol or 'https://'
        self.headers=headers or self.user_agent or {'Accept': '*/*'}
        self.stream=stream if isinstance(stream,bool) else False
        self.initialize_session()
        self.last_request_time=last_request_time
        self.max_retries = max_retries or 3
        self.request_wait_limit = request_wait_limit or 1.5
        self._response=None
        self.make_request()
        self.source_code = None
        self.source_code_bytes=None
        self.source_code_json = {}
        self.react_source_code=[]
        self._response_data = None
        self.process_response_data()
    def update_url_manager(self,url_manager):
        self.url_manager=url_manager
        self.re_initialize()
    def update_url(self,url):
        self.url_manager.update_url(url=url)
        self.re_initialize()
    def re_initialize(self):
        self._response=None
        self.make_request()
        self.source_code = None
        self.source_code_bytes=None
        self.source_code_json = {}
        self.react_source_code=[]
        self._response_data = None
        self.process_response_data()
    @property
    def response(self):
        """Lazy-loading of response."""
        if self._response is None:
            self._response = self.fetch_response()
        return self._response
    
    def fetch_response(self) -> Union[requests.Response, None]:
        """Actually fetches the response from the server."""
        # You can further adapt this method to use retries or other logic you had
        # in your original code, but the main goal here is to fetch and return the response
        return self.try_request()
    def initialize_session(self):
        s = self.session  
        s.proxies = self.network_manager.proxies  # Use the proxies from the NetworkManager
        s.auth = self.network_manager.auth  # Use the auth from SafeRequest (if provided)
        # Add any other headers or cookie settings here
        s.cookies["cf_clearance"] = self.network_manager.cookies
        s.headers.update(self.headers)
        s.mount(self.protocol, self.network_manager.tls_adapter)  # Use the TLSAdapter from the NetworkManager
        return s
    def process_response_data(self):
        """Processes the fetched response data."""
        if not self.response:
            return  # No data to process
        
        self.source_code = self.response.text
        self.source_code_bytes = self.response.content
        
        if self.response.headers.get('content-type') == 'application/json':
            data = convert_to_json(self.source_code)
            if data:
                self.source_code_json = data.get("response", data)
        
        self.get_react_source_code()
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
        soup = BeautifulSoup(self.source_code_bytes,"html.parser")
        script_tags = soup.find_all('script', type=lambda t: t and ('javascript' in t or 'jsx' in t))
        for script_tag in script_tags:
            self.react_source_code.append(script_tag.string)


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

    def make_request(self):
        """
        Make a request and handle potential errors.
        """
        # Update the instance attributes if they are passed

        self.wait_between_requests()
        for _ in range(self.max_retries):
            try:
                self.try_request()  # 10 seconds timeout
                if self.response:
                    if self.response.status_code == 200:
                        self.last_request_time = get_time_stamp()
                        return self.response
                    elif self.response.status_code == 429:
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
    def try_request(self) -> Union[requests.Response, None]:
        """
        Tries to make an HTTP request to the given URL using the provided session.

        Args:
            timeout (int): Timeout for the request.

        Returns:
            requests.Response or None: The response object if the request is successful, or None if the request fails.
        """
        try:
            return self.session.get(url=self.url_manager.url, timeout=self.timeout,stream=self.stream)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_limited_request(self,request_url,service_name="default"):
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
            if response.status_code ==429:
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
    @property
    def url(self):
        return self.url_manager.url

    @url.setter
    def url(self, new_url):
        self._url_manager.url = new_url
class SafeRequestSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,headers:dict=None,max_retries=3,last_request_time=None,request_wait_limit=1.5):
        if SafeRequestSingleton._instance is None:
            SafeRequestSingleton._instance = SafeRequest(url,url_manager=URLManagerSingleton,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        elif SafeRequestSingleton._instance.url != url or SafeRequestSingleton._instance.headers != headers or SafeRequestSingleton._instance.max_retries != max_retries or SafeRequestSingleton._instance.request_wait_limit != request_wait_limit:
            SafeRequestSingleton._instance = SafeRequest(url,url_manager=URLManagerSingleton,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        return SafeRequestSingleton._instance
class SoupManager:
    def __init__(self,url=None,source_code=None,url_manager=None,request_manager=None, parse_type="html.parser"):
        self.soup=[]
        self.url=url
        if url_manager == None:
            url_manager=URLManager(url=self.url)
        if self.url != None and url_manager != None and url_manager.url != URLManager(url=url).url:
            url_manager.update_url(url=self.url)
        self.url_manager= url_manager
        self.url=self.url_manager.url
        if request_manager == None:
            request_manager = SafeRequest(url_manager=self.url_manager)
        self.request_manager = request_manager
        if self.request_manager.url_manager != self.url_manager:
           self.request_manager.update_url_manager(url_manager=self.url_manager)
        self.parse_type = parse_type
        if source_code != None:
            self.source_code = source_code
        else:
            self.source_code = self.request_manager.source_code_bytes
        self.soup= BeautifulSoup(self.source_code, self.parse_type)
        self._all_links_data = None
        self._meta_tags_data = None
    def re_initialize(self):
        self.soup= BeautifulSoup(self.source_code, self.parse_type)
        self._all_links_data = None
        self._meta_tags_data = None
    def update_url(self,url):
        self.url_manager.update_url(url=url)
        self.url=self.url_manager.url
        self.request_manager.update_url(url=url)
        self.source_code = self.request_manager.source_code_bytes
        self.re_initialize()
    def update_source_code(self,source_code):
        self.source_code = source_code
        self.re_initialize()
    def update_request_manager(self,request_manager):
        self.request_manager = request_manager
        self.url_manager=self.request_manager.url_manager
        self.url=self.url_manager.url
        self.source_code = self.request_manager.source_code_bytes
        self.re_initialize()
    def update_url_manager(self,url_manager):
        self.url_manager=url_manager
        self.url=self.url_manager.url
        self.request_manager.update_url_manager(url_manager=self.url_manager)
        self.source_code = self.request_manager.source_code_bytes
        self.re_initialize()
    def update_parse_type(self,parse_type):
        self.parse_type=parse_type
        self.re_initialize()
    @property
    def all_links(self):
        """This is a property that provides access to the _all_links_data attribute.
        The first time it's accessed, it will load the data."""
        if self._all_links_data is None:
            print("Loading all links for the first time...")
            self._all_links_data = self._all_links_get()
        return self._all_links_data
    def _all_links_get(self):
        """A method that loads the data (can be replaced with whatever data loading logic you have)."""
        return self.get_all_website_links()
    def get_all_website_links(self,tag="a",attr="href") -> list:
        """
        Returns all URLs that are found on the specified URL and belong to the same website.

        Args:
            url (str): The URL to search for links.

        Returns:
            list: A list of URLs that belong to the same website as the specified URL.
        """
        all_urls=[self.url_manager.url]
        domain_name = self.url_manager.domain_name
        all_desired=self.get_all_desired_soup(tag=tag,attr=attr)
        for tag in all_desired:
            href = tag.attrs.get(attr)
            if href == "" or href is None:
                # href empty tag
                continue
            href=self.url_manager.get_relative_href(self.url_manager.url,href)
            if not self.url_manager.is_valid_url(href):
                # not a valid URL
                continue
            if href in all_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                continue
            all_urls.append(href)
                
        return all_urls


    @property
    def meta_tags(self):
        """This is a property that provides access to the _all_links_data attribute.
        The first time it's accessed, it will load the data."""
        if self._meta_tags_data is None:
            print("Loading all links for the first time...")
            self._meta_tags_data = self._all_links_get()
        return self._meta_tags_data
    def _meta_tags_get(self):
        """A method that loads the data (can be replaced with whatever data loading logic you have)."""
        return self.get_meta_tags()
    def get_meta_tags(self):
        tags = self.find_all("meta")
        for meta_tag in tags:
            for attr, values in meta_tag.attrs.items():
                if attr not in self.meta_tags:
                    self.meta_tags[attr] = []
                if values not in self.meta_tags[attr]:
                    self.meta_tags[attr].append(values)

                    
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
    
    def get_all_desired_soup(self, tag=None, attr=None, attr_value=None):
        if not tag:
            tags = self.soup.find_all(True)  # get all tags
        else:
            tags = self.soup.find_all(tag)  # get specific tags
        extracted_tags = []
        for tag in tags:
            if attr:
                attribute_value = tag.get(attr)
                if not attribute_value:  # skip tags without the desired attribute
                    continue
                if attr_value and attr_value not in attribute_value:  # skip tags without the desired attribute value
                    continue
            extracted_tags.append(tag)
        return extracted_tags

    def extract_elements(self,url:str=None, tag:str=None, class_name:str=None, class_value:str=None) -> list:
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
        elements = []
        # If no filters are provided, return the entire source code
        if not tag and not class_name and not class_value:
            elements.append(str(self.soup))
            return elements
        # Find elements based on the filters provided
        if tag:
            elements.extend([str(tags) for tags in self.get_all_desired(tag)])
        if class_name:
            elements.extend([str(tags) for tags in self.get_all_desired(tag={class_name: True})])
        if class_value:
            elements.extend([str(tags) for tags in self.get_all_desired(class_name=class_name)])
        return elements
    def find_all_with_attributes(self, class_name=None, *attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes.

        Args:
            base_url (str): The URL from which to discover classes.

        Returns:
            set: A set of unique class names.
        """

    
        unique_classes = set()
        for tag in self.get_find_all_with_attributes(*attrs):
            class_list = self.get_class(class_name=class_name, soup=tag)
            unique_classes.update(class_list)
        return unique_classes
    def get_images(self, tag_name, class_name, class_value):
        images = []
        for tag in self.soup.find_all(tag_name):
            if class_name in tag.attrs and tag.attrs[class_name] == class_value:
                content = tag.attrs.get('content', '')
                if content:
                    images.append(content)
        return images
    def discover_classes_and_meta_images(self, tag_name, class_name_1, class_name_2, class_value, attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes. Also, fetches 
        image references from meta tags.

        Args:
            base_url (str): The URL from which to discover classes and meta images.

        Returns:
            tuple: A set of unique class names and a list of meta images.
        """
    
        unique_classes = self.find_all_with_attributes(class_name=class_name_1, *attrs)
        images = self.get_images(tag_name=tag_name, class_name=class_name_2, class_value=class_value)
        return unique_classes, images
    def get_all_tags_and_attribute_names():
        tag_names = set()  # Using a set to ensure uniqueness
        attribute_names = set()
        for tag in get_all:  # True matches all tags
            tag_names.add(tag.name)
            for attr in tag.attrs:
                attribute_names.add(attr)
        tag_names_list = list(tag_names)
        attribute_names_list = list(attribute_names)
        return {"tags":tag_names_list,"attributes":attribute_names_list}

    def get_all_attribute_values():
        attribute_values={}
        for tag in get_all:  # True matches all tags
            for attr, value in tag.attrs.items():
                # If attribute is not yet in the dictionary, add it with an empty set
                if attr not in attribute_values:
                    attribute_values[attr] = set()
                # If the attribute value is a list (e.g., class), extend the set with the list
                if isinstance(value, list):
                    attribute_values[attr].update(value)
                else:
                    attribute_values[attr].add(value)
        for attr, values in attribute_values.items():
            attribute_values[attr] = list(values)
        return attribute_values
    
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, new_url):
        self._url = new_url

class SoupManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url_manager,request_manager,parse_type="html.parser",source_code=None):
        if SoupManagerSingleton._instance is None:
            SoupManagerSingleton._instance = SoupManager(url_manager,request_manager,parse_type=parse_type,source_code=source_code)
        elif parse_type != SoupManagerSingleton._instance.parse_type  or source_code != SoupManagerSingleton._instance.source_code:
            SoupManagerSingleton._instance = SoupManager(url_manager,request_manager,parse_type=parse_type,source_code=source_code)
        return SoupManagerSingleton._instance
class VideoDownloader:
    def __init__(self, link,temp_directory=None,video_directory=None,remove_existing=True):
        if video_directory==None:
            video_directory=os.path.join(os.getcwd(),'videos')
        if temp_directory == None:
            temp_directory=os.path.join(video_directory,'temp_files')
        self.link = link
        self.temp_directory = temp_directory
        self.video_directory = video_directory
        self.remove_existing=remove_existing
        self.video_urls=self.link if isinstance(self.link,list) else [self.link]
        self.video_url=self.link[0]
        self.starttime = None
        self.downloaded = 0
        self.temp_file_name = None
        self.file_name = None
        self.dl_speed = None
        self.dl_eta=None
        self.total_bytes_est=None
        self.percent_speed=None
        self.percent=None
        self.speed_track = []
        self.last_checked = None
        self.num=0
        self.start()
    def remove_temps(self,file_name):
        for temp_vid in os.listdir(self.temp_directory):
            if len(file_name)<=len(temp_vid):
                if temp_vid[:len(file_name)] == file_name:
                    os.remove(os.path.join(self.temp_directory,temp_vid))
        
    def move_video(self,complete_temp=None,file_name = None):
        if file_name != None:
            self.file_name = file_name
        if self.file_name:
            if complete_temp != None:
                self.complete_temp = complete_temp
            else:
                self.complete_temp = os.path.join(self.temp_directory, self.file_name)
            if os.path.exists(self.complete_temp):
                self.complete_final = os.path.join(self.video_directory, self.file_name)
                if os.path.exists(self.complete_final):
                    if self.remove_existing:
                        os.remove(self.complete_temp)
                        print(f"{self.file_name} already existed in {self.video_directory}; removing it from {self.temp_directory}")
                    self.remove_temps(self.file_name)
                    return True
                else:
                    print(f"moving {self.file_name} from {self.temp_directory} to {self.video_directory}")
                    shutil.move(self.complete_temp, self.video_directory)
                    self.remove_temps(self.file_name)
                    return True
    def progress_callback(self, d):
        self_vars =self.file_name,self.percent,self.dl_eta,self.dl_speed,self.temp_file_name,self.total_bytes_est
        strings = ['filename','_percent_str','eta','speed','tmpfilename','_total_bytes_estimate_str']
        if d['status'] == 'finished':
            print("Done downloading, moving video to final directory...")
            self.file_name = d['filename']
            self.complete_temp = os.path.join(self.temp_directory, d['filename'])
            self.move_video(complete_temp=self.complete_temp,file_name=self.file_name)
            return
        for i,each in enumerate(self_vars):
            string = strings[i]
            try:
                each = d[string]
            except:
                print(f"{string} could not be loaded")
        if self.file_name != None:
            if os.path.exists(os.path.join(self.video_directory,self.file_name)):
                d['status'] == 'finished'
        if get_time_stamp()-self.last_checked>5:
            print(f"{self.file_name} {self.percent} downloaded; eta: {self.eta}")
            self.last_checked = get_time_stamp()

        self.speed_track.append(self.dl_speed)
        if self.speed_track[-1] and self.speed_track[0]:
            if float(self.speed_track[0]) != float(0) and float(self.speed_track[-1]) !=float(0):
                self.percent_speed = (self.speed_track[0] - self.speed_track[-1])/self.speed_track[0]
        else:
            for each in [0,None,float(0)]:  
                while each in self.speed_track:
                    self.speed_track.remove(each)
        if self.percent_speed:
            print(self.percent_speed)
            if self.percent_speed < -0.25:
                self.start()
        
    def video_already_exists(self):
        self.info_dict=self.yt_dlp_instance(url=self.video_url,ydl_opts={'quiet': True, 'no_warnings': True},download=False)
        if self.info_dict:
            video_title = self.info_dict.get('title', None)
            video_ext = self.info_dict.get('ext', 'mp4')
            self.file_name =f"{video_title}.{video_ext}"
            expected_filepath = os.path.join(self.video_directory, self.file_name)
            self.move_video()
            # Extract video info without downloading
            return os.path.exists(expected_filepath)
    def yt_dlp_instance(self,url,download=True,ydl_opts={}):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.info_dict = ydl.extract_info(url=url, download=download)
            return self.info_dict
        except:
            print(f"{url} would not download")
            return False
    def download(self):
        if not os.path.exists(self.video_directory):
            os.makedirs(self.video_directory,exist_ok=True)
        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory,exist_ok=True)
        for video_url in self.video_urls[self.num:]:
            self.last_checked = get_time_stamp()
            self.downloaded = 0
            self.temp_file_name = None
            self.file_name = None
            self.dl_speed = None
            self.percent=None
            self.dl_eta=None
            self.total_bytes_est=None
            self.percent_speed=None
            self.speed_track = []
            ydl_opts = {

                'outtmpl': os.path.join(self.temp_directory, '%(title)s.%(ext)s'),
                'noprogress':True,
                'progress_hooks': [self.progress_callback]  
            }
            self.video_url = video_url
            if not self.video_already_exists():
                print("Starting download...")  # Check if this point in code is reached
                result = self.yt_dlp_instance(url=self.video_url,ydl_opts=ydl_opts)
                print("Download finished!")  # Check if download completes
                
            else:
                print(f"The video from {self.video_url} already exists in the directory {self.video_directory}. Skipping download.")
            self.move_video()
            self.num+=1
    def monitor(self):
        while True:
            time.sleep(60)  # check every minute

            if self.starttime:
                elapsed_time = get_time_stamp() - self.starttime
                percent = self.downloaded / (self.downloaded + elapsed_time)
                downloaded_minutes = elapsed_time / 60
                estimated_download_time = downloaded_minutes / percent - downloaded_minutes

                if estimated_download_time >= 1.5:
                    print("Seems like YouTube is limiting our download speed, restarting the download to mitigate the problem..")
                    # TODO: Find a way to stop the current download and restart. This may not work efficiently since pytube doesn't expose a cancel download method.
                    self.start()  # Restart the download process

    def start(self):
        download_thread = threading.Thread(target=self.download)
        download_thread.start()  


class VideoDownloaderSingleton():
    _instance = None
    @staticmethod
    def get_instance(url_manager,request_manager,title=None,video_extention='mp4',download_directory=os.getcwd(),user_agent=None,download=True,get_info=False):
        if VideoDownloaderSingleton._instance is None:
            VideoDownloaderSingleton._instance = VideoDownloader(url=url,title=title,video_extention=video_extention,download_directory=download_directory,download=download,get_info=get_info,user_agent=user_agent)
        elif VideoDownloaderSingleton._instance.title != title or video_extention != VideoDownloaderSingleton._instance.video_extention or url != VideoDownloaderSingleton._instance.url or download_directory != VideoDownloaderSingleton._instance.download_directory or user_agent != VideoDownloaderSingleton._instance.user_agent:
            VideoDownloaderSingleton._instance = VideoDownloader(url=url,title=title,video_extention=video_extention,download_directory=download_directory,download=download,get_info=get_info,user_agent=user_agent)
        return VideoDownloaderSingleton._instance

class LinkManager:
    def __init__(self,url="https://example.com",source_code=None,url_manager=None,request_manager=None,soup_manager=None,image_link_tags='img',img_link_attrs='src',link_tags='a',link_attrs='href',strict_order_tags=False,img_attr_value_desired=None,img_attr_value_undesired=None,link_attr_value_desired=None,link_attr_value_undesired=None,associated_data_attr=["data-title",'alt','title'],get_img=["data-title",'alt','title']):
        self.url=url
        if url_manager==None:
            url_manager=URLManager(url=url)
        self.url_manager= url_manager
        self.url=self.url_manager.url
        if request_manager==None:
            request_manager = SafeRequest(url_manager=self.url_manager)
        self.request_manager=request_manager
        if soup_manager == None:
            soup_manager = SoupManager(url_manager=self.url_manager,request_manager=self.request_manager)
        self.soup_manager = soup_manager
        if source_code != None:
            self.source_code=source_code
        else:
            self.source_code=self.request_manager.source_code_bytes
        if self.source_code != self.soup_manager.source_code:
            self.soup_manager.update_source_code(source_code=self.source_code)
        self.strict_order_tags=strict_order_tags
        self.image_link_tags=image_link_tags
        self.img_link_attrs=img_link_attrs
        self.link_tags=link_tags
        self.link_attrs=link_attrs
        self.img_attr_value_desired=img_attr_value_desired
        self.img_attr_value_undesired=img_attr_value_undesired
        self.link_attr_value_desired=link_attr_value_desired
        self.link_attr_value_undesired=link_attr_value_undesired
        self.associated_data_attr=associated_data_attr
        self.get_img=get_img
        self.all_desired_image_links=self.find_all_desired_links(tag=self.image_link_tags,
                                                                 attr=self.img_link_attrs,
                                                                 attr_value_desired=self.img_attr_value_desired,
                                                                 attr_value_undesired=self.img_attr_value_undesired)
        self.all_desired_links=self.find_all_desired_links(tag=self.link_tags,
                                                           attr=self.link_attrs,
                                                           attr_value_desired=self.link_attr_value_desired,
                                                           attr_value_undesired=self.link_attr_value_undesired,
                                                           associated_data_attr=self.associated_data_attr,
                                                           get_img=get_img)
    def re_initialize(self):
        self.all_desired_image_links=self.find_all_desired_links(tag=self.image_link_tags,attr=self.img_link_attrs,strict_order_tags=self.strict_order_tags,attr_value_desired=self.img_attr_value_desired,attr_value_undesired=self.img_attr_value_undesired)
        self.all_desired_links=self.find_all_desired_links(tag=self.link_tags,attr=self.link_attrs,strict_order_tags=self.strict_order_tags,attr_value_desired=self.link_attr_value_desired,attr_value_undesired=self.link_attr_value_undesired,associated_data_attr=self.associated_data_attr,get_img=self.get_img)
    def update_url_manager(self,url_manager):
        self.url_manager=url_manager
        self.url=self.url_manager.url
        self.request_manager.update_url_manager(url_manager=self.url_manager)
        self.soup_manager.update_url_manager(url_manager=self.url_manager)
        self.source_code=self.soup_manager.source_code
        self.re_initialize()
    def update_url(self,url):
        self.url=url
        self.url_manager.update_url(url=self.url)
        self.url=self.url_manager.url
        self.request_manager.update_url(url=self.url)
        self.soup_manager.update_url(url=self.url)
        self.source_code=self.soup_manager.source_code
        self.re_initialize()
    def update_source_code(self,source_code):
        self.source_code=source_code
        if self.source_code != self.soup_manager.source_code:
            self.soup_manager.update_source_code(source_code=self.source_code)
        self.re_initialize()
    def update_soup_manager(self,soup_manager):
        self.soup_manager=soup_manager
        self.source_code=self.soup_manager.source_code
        self.re_initialize()
    def update_desired(self,img_attr_value_desired=None,img_attr_value_undesired=None,link_attr_value_desired=None,link_attr_value_undesired=None,image_link_tags=None,img_link_attrs=None,link_tags=None,link_attrs=None,strict_order_tags=None,associated_data_attr=None,get_img=None):
           self.strict_order_tags = strict_order_tags or self.strict_order_tags
           self.img_attr_value_desired=img_attr_value_desired or self.img_attr_value_desired
           self.img_attr_value_undesired=img_attr_value_undesired or self.img_attr_value_undesired
           self.link_attr_value_desired=link_attr_value_desired or self.link_attr_value_desired
           self.link_attr_value_undesired=link_attr_value_undesired or self.link_attr_value_undesired
           self.image_link_tags=image_link_tags or self.image_link_tags
           self.img_link_attrs=img_link_attrs or self.img_link_attrs
           self.link_tags=link_tags or self.link_tags
           self.link_attrs=link_attrs or self.link_attrs
           self.associated_data_attr=associated_data_attr or self.associated_data_attr
           self.get_img=get_img or self.get_img
           self.re_initialize()
    def find_all_desired(self,tag='img',attr='src',strict_order_tags=False,attr_value_desired=None,attr_value_undesired=None,associated_data_attr=None,get_img=None):
            def make_list(obj):
                if isinstance(obj,list) or obj==None:
                    return obj
                return [obj]
            def get_desired_value(attr,attr_value_desired=None,attr_value_undesired=None):
                if attr_value_desired:
                    for value in attr_value_desired:
                        if value not in attr:
                            return False
                if attr_value_undesired:
                    for value in attr_value_undesired:
                        if value in attr:
                            return False
                return True
            attr_value_desired,attr_value_undesired,associated_data_attr,tags,attribs=make_list(attr_value_desired),make_list(attr_value_undesired),make_list(associated_data_attr),make_list(tag),make_list(attr)
            desired_ls = []
            assiciated_data=[]
            for i,tag in enumerate(tags):
                attribs_list=attribs
                if strict_order_tags:
                    if len(attribs)<=i:
                        attribs_list=[None]
                    else:
                        attribs_list=make_list(attribs[i])
                for attr in attribs_list:
                    for component in self.soup_manager.soup.find_all(tag):
                        if attr in component.attrs and get_desired_value(attr=component[attr],attr_value_desired=attr_value_desired,attr_value_undesired=attr_value_undesired):
                            if component[attr] not in desired_ls:
                                desired_ls.append(component[attr])
                                assiciated_data.append({"value":component[attr]})
                                if associated_data_attr:
                                    for data in associated_data_attr:
                                        if data in component.attrs:
                                            assiciated_data[-1][data]=component.attrs[data]
                                            if get_img and component.attrs[data]:
                                                if data in get_img and len(component.attrs[data])!=0:
                                                    for each in self.soup_manager.soup.find_all('img'):
                                                        if 'alt' in each.attrs:
                                                            if each.attrs['alt'] == component.attrs[data] and 'src' in each.attrs:
                                                                assiciated_data[-1]['image']=each.attrs['src']
            desired_ls.append(assiciated_data)
            return desired_ls
    def find_all_domain(self):
        domains_ls=[self.url_manager.protocol+'://'+self.url_manager.domain_name]
        for desired in all_desired[:-1]:
            if url_manager.is_valid_url(desired):
                parse = urlparse(desired)
                domain = parse.scheme+'://'+parse.netloc
                if domain not in domains_ls:
                    domains_ls.append(domain)
    def find_all_desired_links(self,tag='img', attr='src',attr_value_desired=None,strict_order_tags=False,attr_value_undesired=None,associated_data_attr=None,all_desired=None,get_img=None):
        all_desired = all_desired or self.find_all_desired(tag=tag,attr=attr,strict_order_tags=strict_order_tags,attr_value_desired=attr_value_desired,attr_value_undesired=attr_value_undesired,associated_data_attr=associated_data_attr,get_img=get_img)
        assiciated_attrs = all_desired[-1]
        valid_assiciated_attrs = []
        desired_links=[]
        for i,attr in enumerate(all_desired[:-1]):
            valid_attr=self.url_manager.make_valid(attr,self.url_manager.protocol+'://'+self.url_manager.domain_name) 
            if valid_attr:
                desired_links.append(valid_attr)
                valid_assiciated_attrs.append(assiciated_attrs[i])
                valid_assiciated_attrs[-1]["link"]=valid_attr
        desired_links.append(valid_assiciated_attrs)
        return desired_links

def CrawlManager():
    def __init__(self,url=None,source_code=None,parse_type="html.parser"):
        self.url=url
        self.source_code=source_code
        self.parse_type=parse_type
        get_new_source_and_url(self,url)
    def get_new_source_and_url(self,url=None):
        if url == None:
            url = self.url
        self.response = self.response_manager.response
        self.source_code=self.response_manager.source_code
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
        title_tag = parse_title()
        if title_tag:
            meta_info["title"] = title_tag
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
