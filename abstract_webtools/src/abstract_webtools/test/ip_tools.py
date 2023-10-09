from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip

if __name__ == '__main__':
    app.run()
import socket

def get_ip(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror:
        return None

domain = "www.google.com"
ip_address = get_ip(domain)
if ip_address:
    print(f"The IP address of {domain} is {ip_address}")
else:
    print(f"Could not resolve IP address for {domain}")
import requests

def get_location(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data

ip_address = "8.8.8.8"  # Example IP address
location_data = get_location(ip_address)
print(location_data)
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    ip_address = request.remote_addr
    print(f"IP Address of the client is: {ip_address}")
    return "Hello World!"
    def eat_till_quote(self, component_str):
        while component_str and component_str[0] not in ['"', "'"]:
            component_str = component_str[1:]

        if component_str:
            initial_quote = component_str[0]
            component_str = component_str[1:]
            k = 0
            while k < len(component_str) and component_str[k] != initial_quote:
                k += 1
            return component_str[:k], component_str[k+1:]
        return None, None

    def find_class_name(self, string):
        while string and string[0] in [' ', '\t', '\n']:
            string = string[1:]

        if '=' in string:
            class_name, string = string.split('=', 1)
            class_name = class_name.strip()
            if class_name.startswith('"') or class_name.startswith("'"):
                class_name = class_name[1:]
            return class_name.strip(), string.strip()
        return None, None

    def get_all_class_names(self):
        for attribute in self.attributes:
            attrib_sources = self.pure_source.split(f'<{attribute} ')

            for attrib_source in attrib_sources[1:]:
                class_items = attrib_source.split('>')[0]
                while len(class_items) > 0:
                    class_name, class_items = self.find_class_name(class_items)
                    class_value, class_items = self.eat_till_quote(class_items)
                    if class_name and class_value:
                        print(f'Class Name: {class_name}, Class Value: {class_value}')
def get_all_class_names(self):
    for attribute in self.attributes:
        attrib_sources = self.pure_source.split(f'<{attribute} ')
        for attrib_source in attrib_sources[1:]:
            try:
                class_items = attrib_source.split('>')[0]
                class_item_bef = class_items.split('=')[0]
                class_items = class_items[len(class_item_bef+'='):]
                class_name = self.extract_class_name(class_item_bef)
                class_values = self.extract_class_values(class_items)
                self.update_class_data(attribute, class_name, class_values)
            except Exception as e:
                # Handle any parsing errors or exceptions here
                print(f"Error parsing attribute '{attribute}': {str(e)}")

def extract_class_name(self, class_item_bef):
    # Implement logic to extract and clean class names here
    class_name = class_item_bef.strip(' \t\n;\'"')
    return class_name

def extract_class_values(self, class_items):
    # Implement logic to extract and clean class values here
    class_values = class_items.split()
    class_values = [value.strip(' \t\n;\'"') for value in class_values]
    return class_values

def update_class_data(self, attribute, class_name, class_values):
    # Update class-related data structures here
    if class_name not in self.class_names:
        self.class_names.append(class_name)
    self.class_values.extend(class_values)
    
    if class_name not in self.attribute_tracker_js:
        self.attribute_tracker_js[class_name] = {"class_values": [], "attributions": []}
    
    self.attribute_tracker_js[class_name]["class_values"].extend(class_values)
    self.attribute_tracker_js[class_name]["attributions"].append(attribute)

