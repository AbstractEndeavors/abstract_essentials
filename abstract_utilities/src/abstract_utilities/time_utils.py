"""
time_utils.py

This module provides utility functions for working with timestamps and time-related operations.

Usage:
    import abstract_utilities.time_utils as time_utils

Functions:
- get_sleep(sleep_timer): Pause the execution of the program for a specified duration.
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

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import time
from typing import Union
from datetime import datetime
def sleep_count_down(sleep_time):
    while sleep_time>float(0):
        sleep_time -= float(1)
        print(str(sleep_time)+" seconds till start")
        get_sleep(1)
def sleep_timer(last_time: Union[str, float], wait_limit: Union[float, int] = 0) -> None:
    """
    Pause execution for a specified amount of time, calculated based on time differences.

    Parameters:
    last_time (str or float): The reference time or timestamp.
    wait_limit (float or int, optional): The maximum wait time in seconds. Defaults to 0.

    Returns:
    None
    """
    curr_time = get_time_stamp()
    time_difference = curr_time - float(last_time)
    if time_difference < wait_limit:
        sleep_length = float(wait_limit - time_difference)
        get_sleep(sleep_timer=sleep_length)
def get_sleep(sleep_timer: Union[int, float] = 0):
    """
    Pause the execution of the program for a specified duration.

    This function pauses the program's execution for the given amount of time
    before continuing. The sleep duration can be specified in seconds as an integer
    or a floating-point number.

    Args:
        sleep_timer (int or float, optional): The duration in seconds to pause the execution.
            If not provided or set to 0, the function does nothing.

    Example:
        get_sleep(2)  # Pause the program for 2 seconds.
    """
    if isinstance(sleep_timer,int):
        sleep_timer=float(sleep_timer)
    if isinstance(sleep_timer,float):
        time.sleep(sleep_timer)
def get_time_stamp() -> float:
    """
    Returns the current timestamp in seconds.

    Returns:
        float: The current timestamp.
    """
    return datetime.now().timestamp()
def get_date_time_str(date_str,military_time_str):
    return f"{date_str} {military_time_str}"
def get_time_obj(date_time_str):
    return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
def get_current_year() -> int:
    """
    Get the current year.

    Returns:
        int: The current year as an integer.
    """
    now = datetime.now()
    current_year = now.year
    return current_year

def get_24_hr_start(now=get_time_stamp()) -> int:
    """
    Returns the timestamp for the start of the current day.

    Args:
        now (float): The timestamp. Defaults to the current timestamp.

    Returns:
        int: The timestamp for the start of the current day.
    """
    return int(now) - int(get_day_seconds())

def create_timestamp(date_str, military_time_str):
    """
    Converts a date string and military time string to a timestamp.

    Args:
        date_str (str): The date string in the format 'YYYY-MM-DD'.
        military_time_str (str): The military time string in the format 'HH:MM'.

    Returns:
        int: The timestamp corresponding to the date and time.
    """
    date_time_str = get_date_time_str(date_str,military_time_str)
    return int(get_time_obj(date_time_str).timestamp())

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
