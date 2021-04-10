''' 
The purpose of this file is to migrate the .json data from the data directory to our mongodb.
We will still use tinydb as it make for a much easier local algorithm development, although for speed we should be using mongo on the server.
'''
import sys
sys.path.append('../../src')
from server.db_controller import *

def translate_to_mongo():
    