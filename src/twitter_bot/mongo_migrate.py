''' 
The purpose of this file is to migrate the .json data from the data directory to our mongodb.
We will still use tinydb as it make for a much easier local algorithm development.
Although, for speed we should be using mongo on the server.
'''
import sys
import os
import json
sys.path.append('./src')
from hashlib import sha256
from server.db_controller import *
from tiny_db_calls import *

def translate_to_mongo():
    
    tables = ["favorti_tbl", "favorites_context", "followers", "tweets", "tweets_context"]
    users = []
    for root, dirs, files in os.walk("./src/data", topdown=False):
        for f in files:
            if ".json.json" in f:
                os.remove(f"./src/data/{f}")
            if ".json" in f:
                f = f"./src/data/{f}"
                if os.path.exists(f):
                    users.append(f)

    for user in users:
        print(user)
        with open(user,"r") as f:
            data = str(f.read())
            if len(data) > 0:
                data = json.loads(data)
                name = user.split(".")[0]
                data.update({"twitter_handle": name})
                id_ = sha256(name.encode("utf-8")).hexdigest()
                data.update({"id": id_})
                insert_account(data)
            else:
                continue
            
translate_to_mongo()