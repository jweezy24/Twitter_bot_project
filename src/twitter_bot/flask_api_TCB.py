import flask

app = Flask(__name__)

@app.route('/<username>/followers')
def get_followers(name=None):
    if name == None:
        return 'No user given'
    else:
        return name