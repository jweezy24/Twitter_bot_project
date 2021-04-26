from flask import Flask, render_template, url_for, flash, redirect, request

from flaskServer import app
import requests
import json
import math
home_Page = "home.html"
@app.route("/")
@app.route("/home")
def home():
    
    return render_template(home_Page)

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/graph", methods=['GET'])
def graph():
    twitterHandle = request.args['TwitterHandleInput']
    print(twitterHandle)
    #data = twitterHandle
    #get nodes from back end
    #
    try:
        user = requests.get(f"http://67.162.86.214:5000/user/{twitterHandle}")
        connections = requests.get(f"http://67.162.86.214:5000/map/{twitterHandle}")
        if connections.status_code != 200:
            print("Cant Find Account")
            flash('Cant Find Account')
            return render_template(home_Page)
        print(user.content)
        if connections.content != b'{\n  "results": "None"\n}\n' and user.content != b'{\n  "results": "None"\n}\n':

            data = connections.json()
            userData = user.json()
        
            mainNode = { "group": 'nodes', "data": { "id": twitterHandle, "label": twitterHandle, "visited": "false", "followers":userData['followers'], "following":userData['following'] ,"image":userData['image'] }, "classes": 'center-center', }
       
        
            
            newEdges = formatJsonEdgeData(twitterHandle,data)
            newNodes = formatJsonNodeData(data)
            newNodes.insert(0,mainNode)
        else:
            print("oops! No account Data")
            flash('oops! No account Data')
            return render_template(home_Page)
        #print(newEdges)
        #print(newNodes)
    except requests.exceptions.ConnectionError:
        print("oops! Backend-server is down")
        flash('oops! Backend-server is down')
        return render_template(home_Page)
    #
    
    #return data and load the page with the graph
    return render_template("graph.html", nodes = newNodes, edges=newEdges)

# accounts = [{"twitter_handle":"test","views":1,"image":"https://live.staticflickr.com/1261/1413379559_412a540d29_b.jpg", "name":"test" }
#     ]

@app.route("/topSearches")
def topSearches():
    #get searches from back end server
    try:
        users = requests.get("http://67.162.86.214:5000/top")
        data = users.json()
        print(users)
    except requests.exceptions.ConnectionError:
        print("oops! Backend-server is down")
        flash('oops! Backend-server is down')
        return render_template(home_Page)
    return render_template("topSearches.html", accounts = data)

# @app.route("/topSearches/update",methods = ['POST'])
# def updateSearches():
#     requests.post(f"http://67.162.86.214:5000/topUsers")
#     if request.method == "POST":
#         twitter_handle = request.form["twitter_handle"]
        
#         for dict in accounts:
#             if dict["twitter_handle"]== twitter_handle:
#                 dict["views"] +=1

@app.route("/graph/AdditionalNodes", methods=['GET'])
def graphAdditionalNodes():
    twitterHandle = request.args['twitter_handle']
    print(twitterHandle)
    connections = requests.get(f"http://67.162.86.214:5000/map/{twitterHandle}")
    print(connections)
    data = connections.json()
    newEdges = formatJsonEdgeData(twitterHandle,data)
    newNodes = formatJsonNodeData(data)
    #get nodes from back end
    return json.dumps(newNodes + newEdges)


def formatJsonEdgeData(source:str,jsonData:dict):
    edgeData = []
    edgeId = 1
    array = jsonData['results']
    color = "gray"
    for item in array:
        weight = calculateWeight({"x":item["x"], "y":item["y"]})
        if weight <=10:
            weight /=1000 
            weight += .2
            color = "#A3CE65"
        elif weight <=100:
            weight /= 1000
            weight +=.5
            color = "#5982DE"
        else:
            weight /= 1000
            weight +=1
            color = "#705DC2"
        dictionary = {"group": "edges", "data":
            { "id": str(edgeId), "source": source, "target": item["username"], "weight": weight,"color": color, "visited": "false" } 
            
        }
        
        edgeId +=1
        edgeData.append(dictionary)
    return edgeData

def formatJsonNodeData(data:dict): 
    nodeData = []
    array = data['results']
    for item in array:
        dict = {"group": 'nodes', "data": {
             "id": item["username"], "label": item["username"], "visited": "false", "followers":item["followers"], "following":item["following"] ,"image":item["profile_url"] 
             }
             , "classes": 'center-center',
            # "position": { 
            # "x": item['x'],
            # "y": item['y']
            # }
        }
        nodeData.append(dict)
    return nodeData

def calculateWeight(pos):
    return math.sqrt(math.pow(pos['x'],2)+math.pow(pos['y'],2))