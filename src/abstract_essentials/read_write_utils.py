"""
abstract_essentials.read_write_utils
======================================
Local-only file read / write helpers.

The originals supported remote SSH execution; those code paths are dropped.
Callers that passed remote options via **kwargs are unaffected — the kwargs
are accepted but ignored.
"""
import os


def write_to_file(contents, file_path, **kwargs):
    """Overwrite *file_path* with *contents*, creating parent directories."""
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(contents))
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed writing: {file_path}") from e


def read_from_file(file_path=None, **kwargs):
    """Read and return the text contents of *file_path*."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


__all__ = ["write_to_file", "read_from_file"]
