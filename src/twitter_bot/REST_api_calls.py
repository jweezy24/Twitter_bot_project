import requests
import os
bear = os.environ["BEARER"]

def get_tweet_context(id):
    r = requests.get(f'https://api.twitter.com/2/tweets/{id}?tweet.fields=context_annotations,entities', headers={'Authorization' : f'Bearer {bear}'})
    print(r.json())