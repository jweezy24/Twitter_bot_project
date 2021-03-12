''' 
    This file exists for local development.
    This is not meant to be the final database system we use for the application.
    Tinydb Documentation https://tinydb.readthedocs.io/en/latest/
 '''

import tinydb
import os



'''
This method saves the tweet to a local database to cache previously seen tweets to save API calls.
input:
    entry = dictionary value with tweet information.
output:
    a true or false value of saving the tweet was completed.
'''

def save_value(entry,userid="NA",table=""):
    #This should be replaced in the future. Currently is a cop out for a type check
    db_path = os.environ["TINYDB_PATH"]
    db = f"{userid}.json"
    db_path += db


    try:
        id = entry["id"]
    except Exception as e:
        print(e)
        return None
    
    if search_value(id,table=table):
        return False
    else:
        
        with tinydb.TinyDB(db_path) as tweets:
            if table == "":
                tweets.insert(entry)
            else:
                tbl = tweets.table(table)
                tbl.insert(entry)
        
        return True


''' 
This method will check to see if a value already exists in the database.
input:
    id = a string of the id the user wants to find within the local storage
    userid = A string of the user's screen name. This is to store tweets by user in multiple json files. 
output:
    a true or false value of saving the tweet was completed.
'''

def search_value(id,userid="NA", table=""):
    Entry = tinydb.Query()
    db_path = os.environ["TINYDB_PATH"]
    db = f"{userid}.json"
    db_path += db
    
    
    with tinydb.TinyDB(db_path) as tweets:
        if table == "":
            f = tweets.search(Entry.id == id)
        else:
            tbl = tweets.table(table)
            f = tbl.search(Entry.id == id)

    f = len(f) > 0

    if f:
        return True
    else:
        return False



''' 
This method will check to see if a value already exists in the database and returns the value.
input:
    id = a string of the id the user wants to find within the local storage
    userid = A string of the user's screen name. This is to store tweets by user in multiple json files. 
output:
    a true or false value of saving the tweet was completed.
'''

def get_value(id,userid="NA", table=""):
    Entry = tinydb.Query()
    db_path = os.environ["TINYDB_PATH"]
    db = f"{userid}.json"
    db_path += db
    
    
    with tinydb.TinyDB(db_path) as tweets:
        if table == "":
            f = tweets.search(Entry.id == id)
        else:
            tbl = tweets.table(table)
            f = tbl.search(Entry.id == id)

    f = len(f) > 0
    print(f)

    if f:
        return f
    else:
        return None



''' 
This method will return all of the saved favorites of a user.
input:
    user = The screen name of the user
    table = The type of data one would like to retrieve from the table. 
output:
    A list of all the saved favorites
'''

def get_all_favorites(user,table=""):
    db_path = os.environ["TINYDB_PATH"]
    db = f"{user}.json"
    db_path += db
    
    with tinydb.TinyDB(db_path) as tweets:
        q = tinydb.Query()

        if table == "":
            return tweets.search(q.screen_name == user)
        else:
            tbl = tweets.table(table)
            return tbl.all()


''' 
This method will return all of the rows of a table associated with a user.
input:
    user = The screen name of the user
    table = The type of data one would like to retrieve from the table. 
output:
    A list of all rows in table
'''

def get_all_table_entries(user,table=""):
    db_path = os.environ["TINYDB_PATH"]
    db = f"{user}.json"
    db_path += db
    
    with tinydb.TinyDB(db_path) as tweets:
        q = tinydb.Query()

        if table == "":
            return tweets.search(q.screen_name == user)
        else:
            tbl = tweets.table(table)
            return tbl.all()

def get_minimum_id(user,table):
    min_ = None
    is_string = False
    
    db_path = os.environ["TINYDB_PATH"]
    db = f"{user}.json"
    db_path += db

    with tinydb.TinyDB(db_path) as tweets:
        tbl = tweets.table(table)
        for entry in tbl:
            if min_ == None:
                if type(entry["id"]) == type(""):
                    min_ = int(entry["id"])
                    is_string = True
                elif type(entry["id"]) == type(1):
                    min_ = entry["id"]
                continue
            if is_string and min_ > int(entry["id"]):
                min_ = int(entry["id"])
            elif min_ > entry["id"]:
                min_ = entry["id"]

    return min_

def get_maximum_id(user,table):
    max_ = None
    is_string = False
    
    db_path = os.environ["TINYDB_PATH"]
    db = f"{user}.json"
    db_path += db

    with tinydb.TinyDB(db_path) as tweets:
        tbl = tweets.table(table)
        for entry in tbl:
            if max_ == None:
                if type(entry["id"]) == type(""):
                    max_ = int(entry["id"])
                    is_string = True
                elif type(entry["id"]) == type(1):
                    max_ = entry["id"]
                continue
            if is_string and max_ <  int(entry["id"]):
                max_ = int(entry["id"])
            elif max_ < entry["id"]:
                max_ = entry["id"]

    return max_
        
        

        