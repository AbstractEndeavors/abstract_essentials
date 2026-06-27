"""
abstract_essentials.utils
============================
Path and filesystem helpers (local only).

SSH/remote code paths have been dropped; **kwargs accepted for back-compat.
"""
import os


# ---------------------------------------------------------------------------
# predicates
# ---------------------------------------------------------------------------

def is_file(path, *args, **kwargs):
    """True if *path* is an existing local file."""
    if path:
        return os.path.isfile(path)
    return False


def is_dir(path, *args, **kwargs):
    """True if *path* is an existing local directory."""
    if path:
        return os.path.isdir(path)
    return False


# ---------------------------------------------------------------------------
# path decomposition
# ---------------------------------------------------------------------------

def join_path(directory, basename):
    return os.path.join(directory, basename)


def get_safe_basename(path=None):
    if path:
        return os.path.basename(str(path))
    return None


def get_safe_dirname(path=None):
    if path:
        return os.path.dirname(str(path))
    return None


def get_safe_splitext(path=None, basename=None):
    basename = basename or get_safe_basename(path=path)
    if basename:
        filename, ext = os.path.splitext(str(basename))
        return filename, ext
    return None, None


def get_file_parts(path):
    """
    Decompose *path* into a dict of components.

    Keys: file_path, dirname, basename, filename, ext,
          dirbase, parent_dirname, parent_dirbase, super_dirname, super_dirbase.
    """
    if not path:
        return None
    path = str(path)
    basename = get_safe_basename(path)
    filename, ext = get_safe_splitext(basename=basename)

    dirname = get_safe_dirname(path)
    dirbase = get_safe_basename(dirname)

    parent_dirname = get_safe_dirname(dirname)
    parent_dirbase = get_safe_basename(parent_dirname)

    super_dirname = get_safe_dirname(parent_dirname)
    super_dirbase = get_safe_basename(super_dirname)

    return {
        "file_path":      path,
        "dirname":        dirname,
        "basename":       basename,
        "filename":       filename,
        "ext":            ext,
        "dirbase":        dirbase,
        "parent_dirname": parent_dirname,
        "parent_dirbase": parent_dirbase,
        "super_dirname":  super_dirname,
        "super_dirbase":  super_dirbase,
    }


def get_home_dir(path=None):
    """Return the home directory as a string."""
    return os.path.expanduser("~")


# ---------------------------------------------------------------------------
# directory creation
# ---------------------------------------------------------------------------

def safe_join(*paths):
    """os.path.join that silently drops falsy components."""
    paths = [p for p in paths if p]
    return os.path.join(*paths)


def raw_create_dirs(*paths):
    """Recursively create every directory along the joined path and return it."""
    full_path = os.path.abspath(safe_join(*paths))
    sub_parts = [p for p in full_path.split(os.sep) if p]

    current_path = "/" if full_path.startswith(os.sep) else ""
    for part in sub_parts:
        current_path = safe_join(current_path, part)
        os.makedirs(current_path, exist_ok=True)
    return full_path


makedirs = raw_create_dirs


def get_directory(directory):
    """Return *directory*, creating it (and parents) if absent."""
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
    return directory


# ---------------------------------------------------------------------------
# listing / collection
# ---------------------------------------------------------------------------

def get_dirlist(directory):
    """
    Return the contents of *directory*.

    The directory is created if missing.  If *directory* is actually a file,
    a single-element list with its basename is returned.
    """
    path = get_directory(directory)
    if not path:
        return path
    if is_dir(path):
        return os.listdir(path)
    if is_file(path):
        return [os.path.basename(path)]
    return []


def get_files(directory):
    """Recursively collect every file path under *directory*."""
    file_list = []
    for root, _dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def get_files_and_dirs(*args, recursive=True, include_files=True, **kwargs):
    """
    Return ``(dirs, files)`` collected from one or more directories.

    Args:
        *args:          directories to scan (defaults to cwd).
        recursive:      walk subdirectories when True.
        include_files:  include files in the result when True.

    Remote/SSH kwargs are accepted but ignored.
    """
    directories = [a for a in args if a] or [os.getcwd()]
    dirs, files = [], []
    for directory in directories:
        if not os.path.isdir(directory):
            continue
        if recursive:
            for root, dnames, fnames in os.walk(directory):
                for d in dnames:
                    dirs.append(os.path.join(root, d))
                if include_files:
                    for fn in fnames:
                        files.append(os.path.join(root, fn))
        else:
            for name in os.listdir(directory):
                full = os.path.join(directory, name)
                if os.path.isdir(full):
                    dirs.append(full)
                elif include_files and os.path.isfile(full):
                    files.append(full)
    return dirs, files


__all__ = [
    "is_file", "is_dir", "join_path",
    "get_safe_basename", "get_safe_dirname", "get_safe_splitext",
    "get_file_parts", "get_home_dir",
    "safe_join", "raw_create_dirs", "makedirs", "get_directory",
    "get_dirlist", "get_files", "get_files_and_dirs",
]
