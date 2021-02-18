from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'TwitterBotDB' ##needs different name
    ##username and password if needed
    ##host : ip,
    ##port : num
}

db = MongoEngine(app)