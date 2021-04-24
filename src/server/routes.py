
from flask import Flask, render_template, url_for, flash, redirect

from server import app, db
from server.models import Account, Group
from server.db_controller import *


@app.route("/")
@app.route("/user/<thandle>")
def get_twitter_handle():#for testing
    u = get_account_pymongo(t_handle)
    if u == None:
        return None
    else:
        return u
    

@app.route("/map/<thandle>")
def get_user_map():#for testing
    u = distance_algorithm_calculation(t_handle)
    if u == None:
        return None
    else:
        return u
    