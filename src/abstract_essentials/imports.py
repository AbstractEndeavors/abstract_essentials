"""
abstract_essentials.imports
==============================
Re-exports of stdlib symbols that downstream packages import from this module
for back-compatibility (e.g. ``from abstract_essentials.imports import socket``).
"""
import os      # noqa: F401
import sys     # noqa: F401
import json    # noqa: F401
import socket  # noqa: F401
import logging # noqa: F401

__all__ = ["os", "sys", "json", "socket", "logging"]
