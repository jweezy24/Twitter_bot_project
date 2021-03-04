
from flask import Flask, render_template, url_for, flash, redirect

from server import app, db
from server.models import Account, Grouping
from server.db_controller import *


@app.route("/")
@app.route("/home")
def home():#for testing
    account = {"twitter_handle":"test", "name" :"John Doe"}
    insert_account(account)
    for accounts in Account.objects:
        print(account)
    return None



    