from abstract_webtools import URLManager,SafeRequest,SoupManager,LinkManager,VideoDownloader
url = "thedailydialectics.com"
link_manager = LinkManager(url=url)
all_desired_html_components = link_manager.find_all_desired_links(tag='a',attr='href',strict_order_tags=False,attr_value_desired=None,attr_value_undesired=['phantomjs'],associated_data_attr=["data-title",'alt','title'],get_img=["data-title",'alt','title'])
print(all_desired_html_components)
