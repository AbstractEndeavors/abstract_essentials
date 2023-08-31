import time
import datetime
import json
import os
import sys
 # Note: if this relavtive path doesn't work or produces errors try replacing it with an absolute path
home = os.getcwd()
par = str(os.getcwd()).replace(os.getcwd().split('\\')[-1],'\\variables')


import functions

print(functions.ti())
