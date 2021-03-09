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
