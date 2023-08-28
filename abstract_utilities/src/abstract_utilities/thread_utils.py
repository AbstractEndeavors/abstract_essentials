"""
thread_utils.py - Thread Utilities Module

This module provides utility functions for working with threads in Python.

Usage:
    import abstract_utilities.thread_utils as thread_utils

Example:
    # Creating a thread
    my_thread = thread_utils.get_thread(target=my_function, args=(arg1, arg2), daemon=True)

    # Starting the thread
    thread_utils.start_thread(my_thread)

    # Verifying if a given object is a valid thread
    is_valid = thread_utils.verify_thread(my_thread)

    # Checking if a thread is alive
    if thread_utils.thread_alive(my_thread):
        print("Thread is alive")
    else:
        print("Thread is not alive")

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""

import threading
from .type_utils import T_or_F_obj_eq
def get_thread(target=None, args=(), daemon=True) -> threading.Thread:
    """
    Returns a threading.Thread object with the provided target function, arguments, and daemon status.

    Args:
        target: The target function for the thread to execute.
        args: The arguments to pass to the target function.
        daemon (bool): The daemon status of the thread.

    Returns:
        threading.Thread: A threading.Thread object.
    """
    return threading.Thread(target=target, args=args, daemon=daemon)

def start_thread(thread=None):
    """
    Starts the specified thread if it is valid.

    Args:
        thread (threading.Thread): The thread to start.
    """
    if verify_thread(thread):
        thread.start()

def verify_thread(thread=None) -> bool:
    """
    Checks if the given object is a valid threading.Thread object.

    Args:
        thread: The object to check.

    Returns:
        bool: True if the object is a threading.Thread object, False otherwise.
    """
    return T_or_F_obj_eq(type(thread), type(threading.Thread()))

def thread_alive(thread) -> bool:
    """
    Checks if the specified thread is currently alive.

    Args:
        thread (threading.Thread): The thread to check.

    Returns:
        bool: True if the thread is alive, False otherwise.
    """
    if verify_thread(thread):
        return thread.is_alive()
    return False
