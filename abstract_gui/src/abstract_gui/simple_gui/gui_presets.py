from .gui_template import single_call, get_gui_fun
from abstract_utilities.path_utils import get_current_path

def get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path()):
    """
    Function to get a browser GUI based on the type specified.

    Parameters:
    type (str): The type of GUI window to display. Defaults to 'Folder'.
    title (str): The title of the GUI window. Defaults to 'Directory'.

    Returns:
    dict: Returns the results of single_call function on the created GUI window.
    """
    if type.lower() not in 'folderdirectory':
        type='File'
    else:
        type = 'Folder'
    if title == None:
        title = f'Please choose a {type.lower()}'
    window = get_gui_fun('Window',{"title":f'{type} Explorer', "layout":[[get_gui_fun('Text',{"text":title})],
                                                                         [get_gui_fun('Input'), get_gui_fun(f'{type}Browse',{**args,"initial_folder":initial_folder})],
                                                                         [get_gui_fun('OK'), get_gui_fun('Cancel')]]
                                   }
                         )
    return single_call(window)['Browse']


def update_progress(win:str='progress_window',st:str='bar',progress:(int or float)=0):
    """
    Function to update a progress bar in a GUI window.

    Parameters:
    win (str): The name of the window containing the progress bar. Defaults to 'progress_window'.
    st (str): The key of the progress bar element to update. Defaults to 'bar'.
    progress (int or float): The current progress to update the progress bar with. Defaults to 0.
    """
    win[st].update_bar(progress)


def get_progress_bar(max_value:int=100, size:tuple=(30,10),key:str='bar'):
    """
    Function to get a progress bar GUI element.

    Parameters:
    max_value (int): The maximum value of the progress bar. Defaults to 100.
    size (tuple): The size of the progress bar. Defaults to (30,10).
    key (str): The key to assign to the progress bar. Defaults to 'bar'.

    Returns:
    object: Returns a progress bar GUI element.
    """
    return get_gui_fun('ProgressBar',{"max_value":max_value, "size":size, "key":key})


def fancy_progress(title:str="My 1-line progress meter",initial_value:int=0,max_value:int=1000):
    """
    Function to display a fancy progress meter in a GUI window.

    Parameters:
    title (str): The title of the progress meter. Defaults to "My 1-line progress meter".
    initial_value (int): The initial value of the progress meter. Defaults to 0.
    max_value (int): The maximum value of the progress meter. Defaults to 1000.
    """
    import PySimpleGUI as sg
    GRAPH_SIZE = (300 , 300)          
    CIRCLE_LINE_WIDTH, LINE_COLOR = 20, 'yellow'
    TEXT_FONT = 'Courier'
    TEXT_HEIGHT = GRAPH_SIZE[0]//4
    TEXT_LOCATION = (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//2)
    TEXT_COLOR = LINE_COLOR

    for i in range(initial_value,max_value):
        if not get_gui_fun("one_line_progress_meter",{"title":title,"current_value":f"{i+1}","max_value":max_value,"text":'meter key',"text":'MY MESSAGE1',"text":'MY MESSAGE 2',"orientation":'v'}):
            print('Hit the break')
            break

