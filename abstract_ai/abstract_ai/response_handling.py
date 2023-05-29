from .abstract_utilities.time_utils import get_time_stamp, date
from .abstract_utilities.path_utils import join_paths, mkdirs
import json
import os


def save_response(js: dict, response: dict, title: str = str(get_time_stamp())):
    """
    Saves the response JSON and generated text to a file.

    Args:
        js (dict): The input JSON dictionary.
        response (dict): The response dictionary.
        title (str, optional): The title for the file. Defaults to the current timestamp.

    Returns:
        str: The generated text.
    """
    generated_text = response.text
    try:
        js['response'] = response.json()
    except:
        print()
    try:
        generated_text = json.loads(js['response']['choices'][0]['message']['content'])
        if 'title' in generated_text:
            title = generated_text['title']
    except:
        print()
    path = mkdirs(join_paths(mkdirs(join_paths(mkdirs('response_data'), date())), js['model']))
    pen(join_paths(path, title + '.json'), json.dumps(js))
    return generated_text
