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
    #data = twitterHandle
    nodes = [
        { "group": 'nodes', "data": { "id": 'n0', "label": 'n0', "visited": "false", "followers":100, "following":1000 ,"image":'https://live.staticflickr.com/1261/1413379559_412a540d29_b.jpg' }, "classes": 'center-center', },
    { "group": 'nodes', "data": { "id": 'n1', "label": 'n1', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n3', "label": 'n3', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n2', "label": 'n2', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n4', "label": 'n4', "visited": "false" }, "classes": 'center-center', },
    { "group": 'nodes', "data": { "id": 'n5', "label": 'n5', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n6', "label": 'n6', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n7', "label": 'n7', "visited": "false" }, "classes": 'center-center' },
    { "group": 'nodes', "data": { "id": 'n8', "label": 'n8', "visited": "false" }, "classes": 'center-center', },
    { "group": 'nodes', "data": { "id": 'n9', "label": 'n9', "visited": "false" }, "classes": 'center-center', }
    ]

    
    edges = [
    { "group": 'edges', "data": { "id": 'e0', "source": 'n0', "target": 'n1', "weight": 100, "visited": "false" } },
    
    { "group": 'edges', "data": { "id": 'e3', "source": 'n0', "target": 'n4', "weight": 150, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e4', "source": 'n4', "target": 'n2', "weight": 200, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e5', "source": 'n4', "target": 'n3', "weight": 100, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e6', "source": 'n3', "target": 'n5', "weight": 100, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e7', "source": 'n3', "target": 'n6', "weight": 300, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e8', "source": 'n2', "target": 'n7', "weight": 200, "visited": "false" } },
    { "group": 'edges', "data": { "id": 'e9', "source": 'n7', "target": 'n8', "weight": 200, "visited": "false" } },
    
    
    { "group": 'edges', "data": { "id": 'e10', "source": 'n4', "target": 'n9', "weight": 300, "visited": "false" } },
    ]

    
    #return data and load the page with the graph
    return render_template("graph.html", nodes = nodes, edges=edges)

accounts = [{"twitter_handle":"test","views":1,"image":"https://live.staticflickr.com/1261/1413379559_412a540d29_b.jpg", "name":"test" }
    ]

@app.route("/topSearches")
def topSearches():
    
    return render_template("topSearches.html", accounts = accounts)

@app.route("/topSearches/update",methods = ['POST'])
def updateSearches():
    if request.method == "POST":
        twitter_handle = request.form["twitter_handle"]
    for dict in accounts:
        if dict["twitter_handle"]== twitter_handle:
            dict["views"] +=1
    
