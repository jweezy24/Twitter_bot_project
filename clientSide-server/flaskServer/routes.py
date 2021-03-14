from flask import Flask, render_template, url_for, flash, redirect, request
from flaskServer import app, db

@app.route("/")
@app.route("/home")
def home():
    
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/graph", methods=['GET'])
def graph():
    twitterHandle = request.args['TwitterHandleInput']
    print(twitterHandle)
    data = twitterHandle
    #return data and load the page with the graph
    return render_template("graph.html", data = data)