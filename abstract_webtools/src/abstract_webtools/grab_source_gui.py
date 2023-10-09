import requests
import ssl
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from abstract_utilities import *
import PySimpleGUI as sg
import inspect
import re
from .abstract_webtools import URLManagerSingleton,CipherManagerSingleton,SafeRequestSingleton,UserAgentManagerSingleton
from abstract_utilities.class_utils import call_functions,process_args,get_fun,mk_fun
window = None
def get_request_manager(url=None,):
  return SafeRequestSingleton().get_instance(url=url)
def get_url_manager(url=None):
  return URLManagerSingleton().get_instance(url=url)
def get_soup_manager(url=None,selected_option='html.parser',delim=""):
  return SoupManagerSingleton().get_instance(url=url,selected_option=selected_option,delim=delim)
def get_user_agent_manager(user_agent=None):
  return UserAgentManagerSingleton().get_instance(user_agent=user_agent)
def get_cipher_manager(cipher_list=None):
  return CipherManagerSingleton().get_instance(cipher_list=cipher_list)
def get_url():
  if window is None:
    return 'example.com'
  event, values = window.read()
  return values['-URL-']
class SoupManager:
  @staticmethod
  def get_parser_choices():
    return ['html.parser', 'lxml', 'html5lib']
  def __init__(self,url=None,selected_option='html.parser',delim="a"):
    self.url=url
    self.selected_option = selected_option
    self.url_manager = get_url_manager(url=self.url)
    self.request_manager = SafeRequestSingleton().get_instance(url=self.url_manager.correct_url)
    self.soup = BeautifulSoup(self.request_manager.source_code, self.selected_option)
    self.find_all = self.soup.find_all(delim)
class SoupManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,selected_option='html.parser',delim=""):
        if SoupManagerSingleton._instance is None:
            SoupManagerSingleton._instance = SoupManager(url=url,selected_option=selected_option,delim=delim)
        elif SoupManagerSingleton._instance.url != url:
            SoupManagerSingleton._instance = SoupManager(url=url,selected_option=selected_option,delim=delim)
        return SoupManagerSingleton._instance
def get_gui_fun(name:str='',args:dict={}):
  import PySimpleGUI
  return get_fun({"instance":PySimpleGUI,"name":name,"args":args})
def expandable(size:tuple=(None,None)):
    return {"size": size,"resizable": True,"scrollable": True,"auto_size_text": True,"expand_x":True,"expand_y": True}
def change_glob(var:any,val:any):
    globals()[var]=val
    return val
def get_parser_choices():
    bs4_module = inspect.getmodule(BeautifulSoup)
    docstring = bs4_module.__builtins__
    start_index = docstring.find("Supported parsers are:")
    end_index = docstring.find(")", start_index)
    choices_text = docstring[start_index:end_index]
    choices = [choice.strip() for choice in choices_text.split(",")]
    return choices
def add_string_list(ls:(list or str),delim:str='',string:str=''):
    for k in range(0,len(list(ls))):
        string=string+str(list(ls)[k])+delim
    return string
def get_ciphers():
    return "ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,AES256-SHA,AES128-SHA".split(',')
def create_ciphers_string(ls:list=get_ciphers()):
    cipher_string = add_string_list(ls=ls,delim=':')[:-1]
    print(cipher_string)
    globals()['CIPHERS']=cipher_string
    return cipher_string
create_ciphers_string()

def get_browsers():
    return 'Chrome,Firefox,Safari,Microsoft Edge,Internet Explorer,Opera'.split(',')
def get_user_agents():
    return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14']
def create_user_agent(user_agent:str=get_user_agents()[0]):
    return {"user-agent": user_agent}
def get_operating_systems():
  return ['Windows NT 10.0','Macintosh; Intel Mac OS X 10_15_7','Linux','Android','iOS']
def ssl_options():
    return ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
def get_user_agent():
    return {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, *args, **kwargs):
        self.ssl_options = ssl_options
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)
def create_columns(ls,i,k):
    if float(i)%float(k)==float(0.00) and i != 0:
        lsN = list(ls[:-k])
        lsN.append(list(ls[-k:]))
        ls = lsN
    return ls
def get_cypher_checks(ciphers:list=get_ciphers()):
    ls=[[[sg.Text('CIPHERS: ')],sg.Multiline(CIPHERS,key='-CIPHERS_OUTPUT-', size=(80, 5), disabled=False)]]
    for k in range(0,len(ciphers)):
        ls.append(sg.Checkbox(ciphers[k],key=ciphers[k],default=True,enable_events=True))
        ls = create_columns(ls,k,5)
    return ls
def format_url(url):
    # Ensure the URL starts with 'http://' or 'https://'
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
def try_request(url: str, session:type(requests.Session)=requests):
    try:
        return session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def get_parsed_html(url:str='https://www.example.com', header:str=create_user_agent()):
    s = requests.Session()
    s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
    s.headers.update({"user-agent": get_user_agents()[0]})
    adapter = TLSAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    s.mount('https://', adapter)
    r = try_request(url=url, session=s)
    data = r.text
    if r is False:
        return None
    data = r.text
    return data
def parse_all(data):
    ls_type,ls_tag,ls_class,ls_desc =[],[],[],[]
    data = str(data).split('<')
    for k in range(1,len(data)):
        dat = data[k].split('>')[0]
        if dat[0] != '/':
            if dat.split(' ')[0] not in ls_type:
                ls_type.append(dat.split(' ')[0])
        dat = dat[len(dat.split(' ')[0])+1:].split('"')
        for c in range(1,len(dat)):
            if len(dat[c])>0:
                if '=' == dat[c][-1] and ' ' == dat[c][0] and dat[c] != '/':
                    if dat[c][1:]+'"'+dat[c+1]+'"' not in ls_desc:
                        ls_desc.append(dat[c][1:]+'"'+dat[c+1]+'"')
                    if dat[c][1:-1] not in ls_tag:
                        ls_tag.append(dat[c][1:-1])
                    if dat[c+1] not in ls_class:
                        ls_class.append(dat[c+1])
    return ls_type,ls_desc,ls_tag,ls_class

def parse_react_source(data):
    soup = BeautifulSoup(data, 'html.parser')
    script_tags = soup.find_all('script', type=lambda t: t and ('javascript' in t or 'jsx' in t))
    react_source_code = []
    for script_tag in script_tags:
        react_source_code.append(script_tag.string)
    return react_source_code
def all_soup(data,tag,typ,clas,inp):
    return getattr(get_soup_manager(url=get_url()).soup,tag,typ)
def find_all_soup(string:str):
    return get_soup_manager(url=get_url(),delim=string).find_all
def get_bs4_options():
    bs4_options = [
        'BeautifulSoup',
        'Tag',
        'NavigableString',
        'Comment',
        'ResultSet',
        'SoupStrainer',
        'CData'
    ]
    descriptions = [
        'The main BeautifulSoup class used for parsing HTML.',
        'Represents an HTML tag.',
        'Represents a string within an HTML document.',
        'Represents an HTML comment.',
        'Represents a collection of tags found during a search.',
        'Allows parsing only a specific subset of the HTML document.',
        'Represents a CDATA section within an XML document.'
    ]
    return list(zip(bs4_options, descriptions))
def get_multi_line(args):
    return get_gui_fun(name='Multiline',args={**args,**expandable()})
def get_gpt_layout():
    # Add a dropdown for selecting BeautifulSoup parsing capabilities
    parser_choices = ['html.parser', 'lxml', 'html5lib']
    sg.theme('LightGrey1')
    layout = [[sg.Text('URL:', size=(8, 1)), sg.Input('www.example.com', key='-URL-',enable_events=True),sg.Text('status:'),sg.Text(try_request(url='https://www.example.com').status_code,key="-STATUS_CODE-"),
               sg.Text('warning: https://www.example.com is valid'),sg.Text('',key="-URL_WARNING-"),sg.Button('correct url',key='-CORRECT_URL-',visible=True)],
        [sg.Checkbox('Custom User-Agent', default=False, key='-CUSTOMUA-', enable_events=True)],
        [sg.Text('User-Agent:', size=(8, 1)), sg.Combo(get_user_agents(), default_value=get_user_agents()[0], key='-USERAGENT-', disabled=False)],
        [get_cypher_checks()],
        [sg.Button('Grab URL'), sg.Button('Action')],
        [get_multi_line({"key":"-SOURCECODE-"})],
        [sg.Text('Parsing Capabilities:', size=(15, 1)), sg.DropDown(parser_choices, default_value='html.parser', key='-PARSER-',enable_events=True)],
        [get_multi_line({"key":"-SOUP_OUTPUT-"})],
        [sg.Text('find soup:'),[[sg.Checkbox('',default=True,key='-CHECK_TAG-',enable_events=True),sg.Combo([], size=(15, 1),key='-SOUP_TAG-',enable_events=True)],
                                [sg.Checkbox('',default=False,key='-CHECK_ELEMENT-',enable_events=True),sg.Combo([], size=(15, 1),key='-SOUP_ELEMENT-',enable_events=True)],
                                [sg.Checkbox('',default=False,key='-CHECK_TYPE-',enable_events=True),sg.Combo([], size=(15, 1),key='-SOUP_TYPE-',enable_events=True)],
                                [sg.Checkbox('',default=False,key='-CHECK_CLASS-',enable_events=True),sg.Combo([], size=(15, 1),key='-SOUP_CLASS-',enable_events=True)],
                                sg.Input(key='-SOUP_INPUT-'), sg.Button('get soup'),sg.Button('all soup')]],
              
        [get_multi_line({"key":"-FIND_ALL_OUTPUT-"})]]
    return layout
def display_soup(window,values,soup_manager):
    event, values = window.read()
    if soup_manager.soup != None:
        #window['-REACT_OUTPUT-'].update(value=parse_react_source(source_code))
        window['-SOUP_OUTPUT-'].update(value=soup_manager.soup )
        ls_type,ls_desc,ls_tag,ls_class = parse_all(soup_manager.soup)
        if len(ls_type)>0:
          window['-SOUP_TAG-'].update(values=ls_type)
        if len(ls_desc)>0:
            window['-SOUP_ELEMENT-'].update(values=ls_desc,value=ls_desc[0])
        if len(ls_tag) >0:
            window['-SOUP_TYPE-'].update(values=ls_tag,value=ls_tag[0])
        if len(ls_class) >0:
           window['-SOUP_CLASS-'].update(values=ls_class,value=ls_class[0])
    window['-FIND_ALL_OUTPUT-'].update(value=soup_manager.find_all)
def get_selected_cipher_list():
  ls = []
  event, values = window.read()
  for k in range(len(get_ciphers())):
      if values[get_ciphers()[k]] == True:
          ls.append(get_ciphers()[k])
  return ls
def process_url(window,values):
    url = values['-URL-']
    delim= values['-SOUP_INPUT-']
    selected_option = values['-PARSER-']
    user_agent=values['-USERAGENT-']
    soup_input =values['-SOUP_TAG-']
    cipher_list = get_selected_cipher_list()
    try:
      url_manager = get_url_manager(url)
      cipher_manager = get_cipher_manager(cipher_list=cipher_list)
      request_manager = get_request_manager(url=url_manager.correct_url)
      soup_manager = get_soup_manager(url=url,selected_option=selected_option,delim=delim)
      user_agent_manager = get_user_agent_manager(user_agent=user_agent)
      window['-STATUS_CODE-'].update(value=request_manager.status_code)
      window['-SOURCECODE-'].update(value=request_manager.source_code)
      window['-SOUP_OUTPUT-'].update(value=soup_manager.soup)
      window['-CIPHERS_OUTPUT-'].update(value=cipher_manager.ciphers_string)
    except:
      print(url)
  

    return url_manager,request_manager,soup_manager,user_agent_manager,cipher_manager
def url_grabber_while(window):
    while True:

      
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if 'SOUP_' in event:
            soup_manager = get_soup_manager(url=url_manager.correct_url,selected_option=selected_option,delim=values['-SOUP_INPUT-'])
            name = event.split("SOUP_")[-1][:-1]
            check_name = f'-CHECK_{name}-'
            window[check_name].update(value=True)
            for each in values.keys():
              if 'CHECK_' in each and each != check_name:
                window[each].update(value=False)
            window[check_name].update(value=find_all_soup(values[event]))
        cipher_list=get_selected_cipher_list()
        url_manager,request_manager,soup_manager,user_agent_manager,cipher_manager=process_url(window,values)
        if event=='-CORRECT_URL-':
          if url_manager.correct_url:
            window['-URL-'].update(value=url_manager.correct_url)
        if event == 'all soup':
          selected_option = values['-PARSER-']
          soup_manager = get_soup_manager(url=url_manager.correct_url,selected_option=selected_option,delim=values['-SOUP_INPUT-'])
          display_soup(window,values,soup_manager)
          
        if event == 'all soup':
            delim= values['-SOUP_INPUT-']
            window['-FIND_ALL_OUTPUT-'].update(value=soup_manager.find_all)
        
        elif event == 'get soup':
            window['-FIND_ALL_OUTPUT-'].update(value=all_soup(values['-SOUP_OUTPUT-'],values['-SOUP_TAG-'],values['-SOUP_TYPE-'],values['-SOUP_CLASS-'],values['-SOUP_INPUT-']))
        if event == '-CUSTOMUA-':
            window['-SOURCECODE-'].update(disabled=values['-CUSTOMUA-'])
            if not values['-CUSTOMUA-']:
                
                window['-USERAGENT-'].update(value=user_agent_manager.user_agent_header)
                window['-USERAGENT-'].update(disabled=True)
            else:
                window['-USERAGENT-'].update(disabled=False)
        if event == 'Grab URL':
            if url_manager.correct_url:
                # Perform actions with the formatted URL
                process_url(window,values)
            else:
                # Invalid URL format, display an error message
                sg.popup('Invalid URL format. Please enter a valid URL.')
        if event == 'Action':
            selected_option = values['-PARSER-']
            if selected_option == 'BeautifulSoup':
                result = soup
            elif selected_option == 'Tag':
                result = soup.find('tag_name')
            elif selected_option == 'NavigableString':
                result = soup.find('tag_name').string
            elif selected_option == 'Comment':
                result = soup.find(text=lambda text: isinstance(text, Comment))
            elif selected_option == 'ResultSet':
                result = soup.find_all('tag_name')
            elif selected_option == 'SoupStrainer':
                result = BeautifulSoup(source_code, 'html.parser', parse_only=SoupStrainer('tag_name'))
            elif selected_option == 'CData':
                result = soup.find(text=lambda text: isinstance(text, CData))
            else:
                result = None
            window['-SOUP_OUTPUT-'].update(value=str(result))

    
def url_grabber_component():
    globals()['curr_check']='TAG-'
    layout = get_gpt_layout()
    globals()['window'] = get_gui_fun(name='Window',args={'title':'URL Grabber', 'layout':layout,**expandable()})
    url_grabber_while(window)

    
url_grabber_component()
