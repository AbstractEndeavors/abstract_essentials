import os
def safe_join(*paths):
    paths = list(paths)
    paths = [path for path in paths if path]
    return os.path.join(*paths)
def raw_create_dirs(*paths):
    """Recursively create all directories along the given path."""
    full_path = os.path.abspath(safe_join(*paths))
    sub_parts = [p for p in full_path.split(os.sep) if p]

    current_path = "/" if full_path.startswith(os.sep) else ""
    for part in sub_parts:
        current_path = safe_join(current_path, part)
        os.makedirs(current_path, exist_ok=True)
    return full_path
def split_text(string: str) -> tuple:
    """
    Splits a string into its base name and extension and returns them as a tuple.

    Args:
        string (str): A string to be split, typically representing a file name.

    Returns:
        tuple: A tuple containing the base name and extension of the input string.
    """
    return os.path.splitext(string)
def get_ext(file_path: str) -> str:
    """
    Retrieves and returns the extension of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The extension of the file (including the dot).
    """
    if file_path and isinstance(file_path,str):
        return split_text(get_base_name(file_path))[-1]

def get_slash():
    """
    Returns the appropriate file path separator depending on the current operating system.
    """
    slash = '/'  # Assume a Unix-like system by default
    if slash not in get_current_path():
        slash = '\\'  # Use backslash for Windows systems
    return slash
def get_current_path():
    """
    Returns the current working directory.
    
    Returns:
        str: The current working directory.
    """
    return os.getcwd()

def get_home_folder():
    """
    Returns the path to the home directory of the current user.
    
    Returns:
        str: The path to the home directory.
    """
    return os.path.expanduser("~")
def get_file_name(file_path: str) -> str:
    """
    Retrieves and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file (without extension).
    """
    return split_text(get_base_name(file_path))[0]
def get_abs_name_of_this():
    """
    Returns the absolute name of the current module.

    Returns:
        Path: The absolute name of the current module.
    """
    return os.path.abspath(__name__)
def sanitize_filename(name: str):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
    name (str): Filename to sanitize.
    
    Returns:
    str: Sanitized filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)
def get_base_name(file_path: str) -> str:
    """
    Extracts and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file.
    """
    return os.path.basename(file_path)
def get_file_name(file_path: str) -> str:
    """
    Retrieves and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file (without extension).
    """
    return split_text(get_base_name(file_path))[0]

mkdirs=raw_create_dirs
makedirs = mkdirs
__all__ = [
    "mkdirs", "makedirs", "raw_create_dirs",
    "safe_join","get_home_folder",
    "get_current_path","get_slash",
    "get_ext","split_text",
    "get_base_name",
    "sanitize_filename",
    "get_abs_name_of_this",
    "get_file_name",
]
