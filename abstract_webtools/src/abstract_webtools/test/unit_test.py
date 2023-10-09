from abstract_webtools import URLManager,SafeRequest,SoupManager,LinkManager,VideoDownloader
url_1='thedailydialectics.com'
url_2='example.com'
source_code_bytes = b'a charset="utf-8" />\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href="https://www.iana.org/domains/example">More information...</a></p>\n</div>\n</body>\n</html>\n'
source_code_str = """<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
        
    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }
    </style>    
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>"""
url_manager = URLManager(url=url_1)
request_manager = SafeRequest(url=url_1)
soup_manager = SoupManager(url=url_1)
link_manager = LinkManager(url=url_1)

def print_results(url,url_manager,request_manager,soup_manager,link_manager):
    print(f"url = {url}")
    if url_manager != None:
        print(f"url_managers url = {url_manager.url}")
    if request_manager != None:
        print(f"request managers url_managers url = {request_manager.url_manager.url}")
        print(f"request managers url = {request_manager.url}")
    print(f"soup_managers url_managers url = {soup_manager.url_manager.url}")
    print(f"soup_managers url = {soup_manager.url}")
    print(f"link_managers url_managers url from {link_manager.url_manager.url}")
    print(f"link_managers url ={link_manager.url}")

    print(f"source_code from {url}")
    if request_manager != None:
        print(f"request managers source_code = {request_manager.source_code}")
        print(f"request managers source_code type= {type(request_manager.source_code)}")
    print(f"soup_managers request_managers source_code = {soup_manager.request_manager.source_code}")
    print(f"soup_managers request_managers source_code type= {type(soup_manager.request_manager.source_code)}")
    print(f"soup_managers source_code = {soup_manager.source_code}")
    print(f"soup_managers source_code type = {type(soup_manager.source_code)}")
    print(f"link_managers request_managers source_code = {link_manager.request_manager.source_code}")
    print(f"link_managers request_managers source_code type = {type(link_manager.request_manager.source_code)}")
    print(f"link_managers source_code = {link_manager.source_code}")
    print(f"link_managers source_code type= {type(link_manager.source_code)}")
print_results(url_1,url_manager,request_manager,soup_manager,link_manager)
print(f"updating url to {url_2}")
url_manager.update_url(url=url_2)
request_manager.update_url(url=url_2)
soup_manager.update_url(url=url_2)
link_manager.update_url(url=url_2)
print_results(url_2,url_manager,request_manager,soup_manager,link_manager)

print(f"updating url_manager to {url_1} and updating url managers")
url_manager.update_url(url=url_1)
request_manager.update_url_manager(url_manager=url_manager)
soup_manager.update_url_manager(url_manager=url_manager)
link_manager.update_url_manager(url_manager=url_manager)
print_results(url_1,url_manager,request_manager,soup_manager,link_manager)


print(f"updating source_code to example.com source_code_bytes")
soup_manager.update_source_code(source_code=source_code_bytes)
link_manager.update_source_code(source_code=source_code_bytes)
print_results(url_2,None,None,soup_manager,link_manager)

print(f"updating source_code to example.com source_code_text")
soup_manager.update_source_code(source_code=source_code_str)
link_manager.update_source_code(source_code=source_code_str)
print_results(url_2,None,None,soup_manager,link_manager)

print(f"link managers all_desired_links default {url_1}")
print(link_manager.all_desired_links)
print(f"link manager updated all_desired_links defaults {url_1}")
link_manager.update_desired(link_tags=["li","a"],link_attrs=["href","src"],strict_order_tags=False)
print(link_manager.all_desired_links)
input()
#img_attr_value_desired=None,img_attr_value_undesired=None,link_attr_value_desired=None,link_attr_value_undesired=None,image_link_tags=None,img_link_attrs=None,,associated_data_attr=None,get_img=None
#print_results(url_1,url_manager,request_manager,soup_manager,link_manager)
#print(f"link_managers url_managers url from {link_manager.url_manager.url}")
'''
print(f"link_managers url_managers url from {link_manager.url_manager.url}")
request_manager.update_url(url=url2)
print(request_manager.url_manager.url)
input(request_manager.source_code)
soup_manager = SoupManager(url=url)
images = soup_manager.find_all(element="img")
print(soup_manager.url_manager.url)
input(images)
soup_manager.update_url(url=url2)
images = soup_manager.find_all(element='a')
print(soup_manager.url_manager.url)
input(images)
'''
