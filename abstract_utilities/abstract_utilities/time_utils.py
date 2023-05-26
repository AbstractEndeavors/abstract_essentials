"""
time_utils.py

This module provides utility functions for working with timestamps and time-related operations.

Functions:
- get_time_stamp() -> float: Returns the current timestamp in seconds.
- get_milisecond_time_stamp() -> float: Returns the current timestamp in milliseconds.
- get_day(now=get_time_stamp()) -> str: Returns the current day of the week.
- get_time(now=get_time_stamp()) -> str: Returns the current time.
- get_date(now=get_time_stamp()) -> str: Returns the current date.
- save_last_time(now=get_time_stamp()) -> str: Saves the last timestamp to a file.
- get_day_seconds() -> float: Returns the number of seconds in a day.
- get_week_seconds() -> float: Returns the number of seconds in a week.
- get_hour_seconds() -> float: Returns the number of seconds in an hour.
- get_minute_seconds() -> float: Returns the number of seconds in a minute.
- get_second() -> float: Returns the value of one second.
- get_24_hr_start(now=get_time_stamp()) -> int: Returns the timestamp for the start of the current day.
"""

import time
from datetime import datetime

def get_time_stamp() -> float:
    """
    Returns the current timestamp in seconds.

    Returns:
        float: The current timestamp.
    """
    return datetime.now().timestamp()

# ... rest of the functions with docstrings

def get_24_hr_start(now=get_time_stamp()) -> int:
    """
    Returns the timestamp for the start of the current day.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        int: The timestamp for the start of the current day.
    """
    return int(now) - int(get_day_seconds())

import time
from datetime import datetime

def get_time_stamp():
    """
    Returns the current timestamp in seconds.

    Returns:
        float: The current timestamp.
    """
    return datetime.now().timestamp()

def get_milisecond_time_stamp():
    """
    Returns the current timestamp in milliseconds.

    Returns:
        float: The current timestamp in milliseconds.
    """
    return datetime.now().timestamp() * 1000

def get_day(now=get_time_stamp()):
    """
    Returns the current day of the week.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current day of the week.
    """
    return datetime.fromtimestamp(now).strftime("%A")

def get_time(now=get_time_stamp()):
    """
    Returns the current time.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current time.
    """
    return str(datetime.fromtimestamp(now))[10:]

def get_date(now=get_time_stamp()):
    """
    Returns the current date.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The current date.
    """
    return str(datetime.fromtimestamp(now))[:10]

def save_last_time(now=get_time_stamp()):
    """
    Saves the last timestamp to a file.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        str: The filename where the timestamp is saved.
    """
    return pen(str(now), 'last.txt')

def get_day_seconds():
    """
    Returns the number of seconds in a day.

    Returns:
        float: The number of seconds in a day.
    """
    return float(24 * 60 * 60)

def get_week_seconds():
    """
    Returns the number of seconds in a week.

    Returns:
        float: The number of seconds in a week.
    """
    return float(7 * 24 * 60 * 60)

def get_hour_seconds():
    """
    Returns the number of seconds in an hour.

    Returns:
        float: The number of seconds in an hour.
    """
    return float(60 * 60)

def get_minute_seconds():
    """
    Returns the number of seconds in a minute.

    Returns:
        float: The number of seconds in a minute.
    """
    return float(60)

def get_second():
    """
    Returns the value of one second.

    Returns:
        float: The value of one second.
    """
    return float(1)

def get_24_hr_start(now=get_time_stamp()):
    """
    Returns the timestamp for the start of the current day.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        int: The timestamp for the start of the current day.
    """
    return int(now) - int(get_day_seconds())
# Function: get_time_stamp
# Function: get_milisecond_time_stamp
# Function: get_day
# Function: get_time
# Function: get_date
# Function: save_last_time
# Function: get_day_seconds
# Function: get_week_seconds
# Function: get_hour_seconds
# Function: get_minute_seconds
# Function: get_second
# Function: get_24_hr_start
