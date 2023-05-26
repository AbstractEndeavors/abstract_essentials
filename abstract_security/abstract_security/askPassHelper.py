#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import getpass
load_dotenv()
def getPass():
    return os.getenv('MY_PASSWORD')
print(getPass())
