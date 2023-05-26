from pathlib import Path
import os
import shutil
from tkinter import filedialog
import PySimpleGUI as sg
import time
from tkinter import filedialog, Tk
from tkinter.filedialog import askdirectory

def is_valid_path(path: str) -> bool:
    """Checks if the provided path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)

def is_file(path: str) -> bool:
    """Checks if the provided path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)

def browse_directory() -> str:
    """Opens a file dialog and returns the selected directory path.

    Returns:
        str: The selected directory path.
    """
    return filedialog.askdirectory()

def browse_files(initial_directory: str) -> tuple:
    """Opens a file dialog and returns the directory path and selected file name.

    Args:
        initial_directory (str): The initial directory path for the file dialog.

    Returns:
        tuple: A tuple containing the directory path and selected file name.
    """
    dir_path = browse_directory()
    filename = filedialog.askopenfilename(initialdir=dir_path, title="Select a File",
                                          filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    
    if filename in [(), '', None]:
        return dir_path, ''
    
    return dir_path, filename.split('/')[-1]

def update_global_variable(name: str, value) -> None:
    """Updates the global variable with the provided name and value.

    Args:
        name (str): The name of the global variable.
        value: The value to assign to the global variable.

    Returns:
        None
    """
    globals()[name] = value

def list_directory_contents(path: str) -> list:
    """Returns a list of directory contents or a list with a single file, if the path is a file.

    Args:
        path (str): The path of the directory or file.

    Returns:
        list: A list of directory contents or a list with a single file path.
    """
    if is_file(path):
        return [path]
    elif is_valid_path(path):
        return os.listdir(path)
    return [path]

def trunc(a: float, x: int) -> float:
    """
    Truncates a float number to a specific number of decimal places.

    Args:
        a (float): The number to truncate.
        x (int): The number of decimal places to retain.

    Returns:
        float: The truncated float number.
    """
    temp = str(a)
    for i in range(len(temp)):
        if temp[i] == '.':
            try:
                return float(temp[:i+x+1])
            except:
                return float(temp)
    return float(temp)

def update_prog(win, js: dict):
    """
    Updates a progress meter in a given window.

    Args:
        win: The window in which the progress meter resides.
        js (dict): A dictionary that includes progress meter details like keys, title, current and maximum progress, type, name, and action.
    """
    win[js['keys']].update(sg.one_line_progress_meter(js['title'], js['curr']+1, js['max'], js['type']+' : '+js['name'], js['action']))

def mkGb(k) -> float:
    """
    Converts a value to Gigabytes (GB).

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB.
    """
    return float(float(k)*(10**9))

def mkGbTrunk(k) -> float:
    """
    Converts a value to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(k), 5)

def mkGbTrunFroPathTot(k) -> float:
    """
    Fetches the file size from a path, converts it to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (str): The file path.

    Returns:
        float: The file size converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(s.path.getsize(k)), 5)

def lsDir(x) -> list:
    """
    Lists the contents of a directory or the file name if it's a file.

    Args:
        x (str): The path to the directory or file.

    Returns:
        list: A list containing the contents of a directory or a file name.
    """
    if isFile(x):
        return [x.split('/')[-1]]
    elif isPath(x):
        return os.listdir(x)
    return [x.split('/')[-1]

def join_paths(path1: str, path2: str) -> str:
    """Joins two paths.

    Args:
        path1 (str): The first path.
        path2 (str): The second path.

    Returns:
        str: The joined path.
    """
    return os.path.join(path1, path2)

def get_source_and_destination_paths() -> None:
    """Prompts the user to select the source and destination paths and updates the corresponding global variables.

    Returns:
        None
    """
    source_dir, source_file = browse_files('What is the initial folder or document?', os.getcwd())
    update_global_variable('source_files', list_directory_contents(join_paths(source_dir, source_file)))
    update_global_variable('source_path', source_dir)
    dest_dir, dest_file = browse_files('Input the destination path', os.getcwd())
    update_global_variable('destination_files', list_directory_contents(join_paths(dest_dir, dest_file)))
    update_global_variable('destination_path', dest_dir)

def get_abs_path_of_this() -> Path:
    """
    Returns the absolute path of the current file.

    Returns:
        Path: The absolute path of the current file.
    """
    return Path(__file__).absolute()

def get_abs_name_of_this() -> Path:
    """
    Returns the absolute name of the current module.

    Returns:
        Path: The absolute name of the current module.
    """
    return Path(__name__).absolute()

def get_here() -> str:
    """
    Returns the current working directory.

    Returns:
        str: The current working directory.
    """
    return os.getcwd()

def create_paths(ls: list) -> str:
    """
    Creates a path by joining multiple path components.

    Args:
        ls (list): The list of path components.

    Returns:
        str: The created path.
    """
    y = create_path(ls[0], ls[1])
    for k in range(2, len(ls)):
        y = create_path(y, ls[k])
    return y

def create_path(x: str, y: str) -> str:
    """
    Creates a path by joining two path components.

    Args:
        x (str): The first path component.
        y (str): The second path component.

    Returns:
        str: The created path.
    """
    return os.path.join(x, y)

def createFolds(ls: list) -> None:
    """
    Creates multiple directories.

    Args:
        ls (list): The list of directory paths to create.
    """
    for k in range(len(ls)):
        mkdirs(ls[k])

def mkdirs(path: str) -> str:
    """
    Creates a directory and any necessary intermediate directories.

    Args:
        path (str): The directory path to create.

    Returns:
        str: The created directory path.
    """
    os.makedirs(path, exist_ok=True)
    return path

def crPa(x: str, y: str) -> str:
    """
    Creates a path by joining two path components.

    Args:
        x (str): The first path component.
        y (str): The second path component.

    Returns:
        str: The created path.
    """
    return os.path.join(str(x), str(y))

def is_file(x: str) -> bool:
    """
    Checks if a path corresponds to a file.

    Args:
        x (str): The path to check.

    Returns:
        bool: True if the path corresponds to a file, False otherwise.
    """
    return os.path.isfile(crPa(home, x))

def exists(x: str) -> bool:
    """
    Checks if a path exists.

    Args:
        x (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    try:
        x = reader(x)
        return True
    except:
        return False

def file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at the specified path.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def dir_exists(path: str) -> bool:
    """
    Checks if a directory exists at the specified path.

    Args:
        path (str): The path to the directory.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(path)

def progress_bar_callback(n: int, block_size: int, total_size: int) -> None:
    """
    Updates a progress bar based on the number of blocks processed.

    Args:
        n (int): The number of blocks processed.
        block_size (int): The size of each block.
        total_size (int): The total size of the file being processed.
    """
    PySimpleGUI.ProgressBar(total_size, 'horizontal', n * block_size, 'green')

def copy_file_or_directory(src_path: str, dst_path: str) -> None:
    """
    Copies a file or a directory from a source path to a destination path.

    Args:
        src_path (str): The path of the source file or directory.
        dst_path (str): The path of the destination file or directory.
    """
    if os.path.isfile(src_path):
        file_size = os.path.getsize(src_path)
        # Open the source and destination files
        with open(src_path, 'rb') as src_file, open(dst_path, 'wb') as dst_file:
            # Copy the contents of the source file to the destination file in chunks of 64KB
            while True:
                buf = src_file.read(64 * 1024)
                if not buf:
                    break
                dst_file.write(buf)
                # Update the progress bar with the number of bytes written so far
                updateProg(window, {'title':'transfers', 'keys':'-PBAR-', 'curr':mkGbTrunFroPathTot(dst_path),
                                    'max':mkGbTrunFroPathTot(file_size), 'type':'file', 'name':dst_path.split('/')[-1],
                                    'action':'copying'})
    elif os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path)

def get_size(path: str) -> int:
    """
    Calculates the size of a file or a directory.

    Args:
        path (str): The path of the file or directory.

    Returns:
        int: The size of the file or directory in bytes.
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fp = os.path.join(dirpath, file)
            try:
                total_size += os.path.getsize(fp)
            except:
                total_size += 0
    return total_size

def get_total_size(folder_path: str) -> int:
    """
    Calculates the total size of a directory and its subdirectories.

    Args:
        folder_path (str): The path of the directory.

    Returns:
        int: The total size of the directory and its subdirectories in bytes.
    """
    total_size = 0
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            total_size += get_size(item_path)
    return total_size
