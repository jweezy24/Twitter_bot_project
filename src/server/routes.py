
from flask import Flask, render_template, url_for, flash, redirect

from server import app, db
from server.models import Account, Group
from server.db_controller import *
import sys
sys.path.append("./src/twitter_bot/")
from categorization_algorithm import *


@app.route("/")
@app.route("/user/<thandle>")
def get_twitter_handle(thandle):#for testing
    u = get_account_pymongo(thandle)
    if u == None:
        return "None"
    else:
        increment_counter(u)
        return {
            'id': u['twitter_handle'],
            'followers' : u['total_followers'],
            'following' : u['total_following'],
            'image' : u['profile_image_url'] 
        }
    

@app.route("/map/<thandle>")
def get_user_map(thandle):#for testing
    u = distance_algorithm_calculation(thandle)
    if u == None:
        return "None"
    else:
        return {"results":u}

        
@app.route("/top")
def get_top_requests():#for testing
    #u_list = get_top_requested()
    u == None
    if u == None:
        return "None"
    else:
        return {"results":u}
    