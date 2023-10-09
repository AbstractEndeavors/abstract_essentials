from abstract_webtools import *
response = SafeRequest()
def discover_classes_with_links(base_url):
    """
    Discovers classes in the HTML content of the provided URL 
    that have associated href or src attributes.

    Args:
        base_url (str): The URL from which to discover classes.

    Returns:
        set: A set of unique class names.
    """
    
    if response:
        soup = BeautifulSoup(response, 'html.parser')
    
        unique_classes = set()

        for tag in soup.find_all(lambda t: t.has_attr('href') or t.has_attr('src')):
            class_list = tag.get('class', [])
            unique_classes.update(class_list)

        return unique_classes
def extract_links_from_url(url):
    """
    Extracts all href and src links from a given URL's source code.

    Args:
        base_url (str): The URL from which to extract links.

    Returns:
        dict: Dictionary containing image links and external links under the parent page.
    """
    agg_js = {'images':[],'external_links':[]}
    response = SafeRequest().get_source_code(url=url)
    if response != None:
        soup = BeautifulSoup(response, 'html.parser')

        # Extract href attributes
        href_links = [a['href'] for a in soup.find_all(lambda tag: tag.has_attr('href'))]
        
        # Extract src attributes
        src_links = [a['src'] for a in soup.find_all(lambda tag: tag.has_attr('src'))]

        # Convert all links to absolute links
        absolute_links = [urljoin(url, link) for link in href_links + src_links]

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


def determine_values(url):
    # This is just a mockup. In a real application, you'd analyze the URL or its content.

    # Assuming a blog site
    if 'blog' in url:
        if '2023' in url:  # Assuming it's a current year article
            return ('weekly', '0.8')
        else:
            return ('monthly', '0.6')
    elif 'contact' in url:
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
        response = SafeRequest().get_source_code(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = [a['href'] for a in soup.find_all('a', href=True)]
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
def discover_classes_and_meta_images(base_url):
    """
    Discovers classes in the HTML content of the provided URL 
    that have associated href or src attributes. Also, fetches 
    image references from meta tags.

    Args:
        base_url (str): The URL from which to discover classes and meta images.

    Returns:
        tuple: A set of unique class names and a list of meta images.
    """
    response = SafeRequest().get_source_code(url=base_url)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        
        unique_classes = set()
        meta_images = []

        for tag in soup.find_all(lambda t: t.has_attr('href') or t.has_attr('src')):
            class_list = tag.get('class', [])
            unique_classes.update(class_list)

        for meta_tag in soup.find_all('meta'):
            if 'property' in meta_tag.attrs and meta_tag.attrs['property'] == 'og:image':
                content = meta_tag.attrs.get('content', '')
                if content:
                    meta_images.append(content)

        return unique_classes, meta_images

# Define or import required functions here, like get_all_website_links, determine_values, 
# discover_classes_and_meta_images, and extract_links_from_url.
def get_meta_info(url):
    response = SafeRequest().get_source_code(url=url)
    response # Raise exception if not a 2xx response

    soup = BeautifulSoup(response, 'html.parser')
    
    meta_info = {}
    
    # Fetch the title if available
    title_tag = soup.title
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

def generate_sitemap(domain):
    urls = get_all_website_links(domain)
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        string = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        
        for url in urls:
            string += f'  <url>\n    <loc>{url}</loc>\n'
            preprocess=[]
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

if __name__ == '__main__':
    domain = "https://uuvo.com"
    request_manager = SafeRequest(url=domain)
    generate_sitemap(domain)
