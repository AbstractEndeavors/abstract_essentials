#!/usr/bin/env python3
import openai
from dotenv import load_dotenv
import os
import getpass


def load_openai_key():
    """
    Loads the OpenAI API key for authentication.
    """
    openai.api_key = get_openai_key()

def get_env(path='/home/hmmm/envy_all.env', st='OPENAI_API_KEY'):
    """
    Retrieves the value of the specified environment variable.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable. Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The value of the environment variable.
    """
    load_dotenv(path)
    return os.getenv(st)

def get_openai_key(path='/home/hmmm/envy_all.env', st='OPENAI_API_KEY'):
    """
    Retrieves the OpenAI API key from the environment variables.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable containing the API key. Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The OpenAI API key.
    """
    key = get_env(path=path, st=st)
    openai.api_key = key

def getPass(path='/home/hmmm/envy_all.env', st='MY_PASSWORD'):
    """
    Retrieves the value of the specified environment variable.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable. Defaults to 'MY_PASSWORD'.

    Returns:
        str: The value of the environment variable.
    """
    return get_env(path=path, st=st)
