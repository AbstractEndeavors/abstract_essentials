import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests

# Function to send an HTTP GET request and return the response object
def try_request(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        return None

# Function to get a list of User-Agent strings (replace with your own list)
def get_user_agents():
    user_agents = ["User-Agent 1", "User-Agent 2", "User-Agent 3"]
    return user_agents

# Function to create a layout for checking multiple elements at once
def get_multi_line(config):
    # Replace with your multi-line element configuration
    return sg.Multiline("", key=config["key"], size=(40, 10), autoscroll=True, reroute_stdout=True)

# Function to create a layout for checking different types of elements in BeautifulSoup
def get_cypher_checks():
    # Replace with your checkbox and combo box configuration for different element types
    return [sg.Checkbox('Check Tag', default=True, key='-CHECK_TAG-', enable_events=True), sg.Combo([], size=(15, 1), key='-SOUP_TAG-', enable_events=True)]

# Add more parsing capabilities if needed
parser_choices = ['html.parser', 'lxml', 'html5lib']

# Create the GUI layout
sg.theme('LightGrey1')
layout = [
    [sg.Text('URL:', size=(8, 1)), sg.Input('www.example.com', key='-URL-', enable_events=True),
     sg.Text('Status:'), sg.Text('', key="-STATUS_CODE-"),
     sg.Text('', key="-URL_WARNING-"), sg.Button('Correct URL', key='-CORRECT_URL-', visible=True)],
    [sg.Checkbox('Custom User-Agent', default=False, key='-CUSTOMUA-', enable_events=True)],
    [sg.Text('User-Agent:', size=(8, 1)), sg.Combo(get_user_agents(), default_value=get_user_agents()[0], key='-USERAGENT-', disabled=False)],
    [get_cypher_checks()],
    [sg.Button('Grab URL'), sg.Button('Action')],
    [get_multi_line({"key": "-SOURCECODE-"})],
    [sg.Text('Parsing Capabilities:', size=(15, 1)), sg.DropDown(parser_choices, default_value='html.parser', key='-PARSER-', enable_events=True)],
    [get_multi_line({"key": "-SOUP_OUTPUT-"})],
    [sg.Text('Find Soup:')],
    [
        [sg.Checkbox('', default=True, key='-CHECK_TAG-', enable_events=True), sg.Combo([], size=(15, 1), key='-SOUP_TAG-', enable_events=True)],
        [sg.Checkbox('', default=False, key='-CHECK_ELEMENT-', enable_events=True), sg.Combo([], size=(15, 1), key='-SOUP_ELEMENT-', enable_events=True)],
        [sg.Checkbox('', default=False, key='-CHECK_TYPE-', enable_events=True), sg.Combo([], size=(15, 1), key='-SOUP_TYPE-', enable_events=True)],
        [sg.Checkbox('', default=False, key='-CHECK_CLASS-', enable_events=True), sg.Combo([], size=(15, 1), key='-SOUP_CLASS-', enable_events=True)],
        sg.Input(key='-SOUP_INPUT-'), sg.Button('Get Soup'), sg.Button('All Soup')
    ],
    [get_multi_line({"key": "-FIND_ALL_OUTPUT-"})]
]

# Create the window
window = sg.Window('BeautifulSoup Console', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    # Handle URL input change event
    if event == '-URL-':
        url = values['-URL-']
        response = try_request(url)
        if response:
            window['-STATUS_CODE-'].update(response.status_code)
            window['-URL_WARNING-'].update('Valid URL')
            window['-CORRECT_URL-'].update(visible=False)
        else:
            window['-URL_WARNING-'].update('Invalid URL')
            window['-STATUS_CODE-'].update('')

    # Handle Custom User-Agent checkbox
    if event == '-CUSTOMUA-':
        custom_ua_enabled = values['-CUSTOMUA-']
        window['-USERAGENT-'].update(disabled=not custom_ua_enabled)

    # Handle Grab URL button click event
    if event == 'Grab URL':
        url = values['-URL-']
        response = try_request(url)
        if response:
            soup = BeautifulSoup(response.text, values['-PARSER-'])
            window['-SOUP_OUTPUT-'].print(soup.prettify(), end='', text_color='black')

    # Handle Get Soup button click event
    if event == 'Get Soup':
        tag = values['-SOUP_TAG-']
        element = values['-SOUP_ELEMENT-']
        element_type = values['-SOUP_TYPE-']
        class_name = values['-SOUP_CLASS-']
        input_text = values['-SOUP_INPUT-']
        
        # Replace with your BeautifulSoup logic to find and display the selected elements
        # Example: soup.find(tag, {"class": class_name})
        # Update the -FIND_ALL_OUTPUT- element with the result



# Close the window
window.close()
