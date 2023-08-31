# Overview
This Python application allows users to select and interact with various APIs. It consists of three main parts:
![image](https://user-images.githubusercontent.com/57512254/228689331-9d417ad5-7dd4-408c-bfce-84e205a7a261.png)


The Graphical User Interface (GUI)
The API Selector
The API Grabber
The GUI is based on PySimpleGUI and provides a convenient way to interact with the API Selector and API Grabber components. The API Selector allows users to create or choose from preset APIs, while the API Grabber is responsible for fetching data from the selected API.

GUI
The GUI consists of the following elements:

Menu bar: Allows users to access various functions such as opening a file, saving data, and accessing network tools or APIs.
Input fields: Users can enter the API URL and other relevant information.
Buttons: Actions like creating an API, selecting a preset API, choosing or adding RPC, scanning an API, copying the URL, or saving output can be performed using these buttons.
Output window: Displays the output of the API requests and other relevant information.
API Selector
The API Selector is responsible for creating or choosing APIs. Users can either create a custom API or choose from a list of preset APIs. The custom API is created using the selApi.createMix() function, and the preset APIs can be selected using the selApi.buildApi() function.

API Grabber
The API Grabber is responsible for fetching data from the selected API. It performs the following operations:
![image](https://user-images.githubusercontent.com/57512254/228689559-08cc68b0-41d5-4e21-9709-8b6c70253ee2.png)

Sends an HTTP request to the API endpoint using the requests library.
Parses the JSON response and stores the result in a file named recent.json.
Displays the content of recent.json in the output window.
The main function responsible for fetching the data is sites(A), which takes the API URL as input and returns the JSON response.

Usage
To use the application, follow these steps:

Run the Python script.
The main GUI window will appear. Use the menu bar or buttons to perform desired actions.
Enter the API URL in the 'api url' input field or choose a preset API.
Click the 'SCAN' button to fetch data from the API.
The output will be displayed in the output window. You can save the output or copy the API URL to the clipboard if needed.
Dependencies
PySimpleGUI
Requests
JSON
Time
Clipboard
Pathlib
OS
![image](https://user-images.githubusercontent.com/57512254/228689642-9cdb43c6-8d92-4d14-b9da-1c3c6bf3302f.png)
