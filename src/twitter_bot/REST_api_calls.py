import requests
import os
import json
import time
bear = os.environ["BEARER"]

def get_tweet_context(ids):
    string = ''

    '''
    If the variable ids is a list we create a string of comma separated ids.
    '''
    if type(ids) == type([]):
        for id in ids:
            string += f"{id},"
        string=string[:len(string)-2]
        
        r = requests.get(f'https://api.twitter.com/2/tweets?ids={string}&tweet.fields=context_annotations', headers={'Authorization' : f'Bearer {bear}'})
        
    elif type(ids) == type("") or type(ids) == type(1):
        r = requests.get(f'https://api.twitter.com/2/tweets/{ids}?&tweet.fields=context_annotations', headers={'Authorization' : f'Bearer {bear}'})

    else:
        r = None


    if r and "data" in r.json() and "context_annotations" in r.json()["data"]:
        return r.json()["data"]
    elif r and "errors" in r.json():
        print(r.json())
        time.sleep(900)
        return get_tweet_context(ids)
    else:
        print(r.json())
        return None

def get_followers_REST(user):
    r1 = requests.get(f'https://api.twitter.com/2/users/by/username/{user}', headers={'Authorization' : f'Bearer {bear}'})

    if r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_followers_REST(user)
    elif r1.status_code == 429:
        time.sleep(900)
        return get_followers_REST(user)
    elif r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_followers_REST(user)
    
    print(f"Part 1 {r1}")

    id = r1.json()["data"]["id"]
    r1 = requests.get(f'https://api.twitter.com/2/users/{id}/followers?&user.fields=name&max_results=1000', headers={'Authorization' : f'Bearer {bear}'})
    
    print(f"Part 2 {r1}")
    names = []
    if r1 and "data" in r1.json():
        for entry in r1.json()["data"]:
            names.append(entry["username"])
        return names
    elif r1.status_code == 429:
        time.sleep(900)
        return get_followers_REST(user)
    elif r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_followers_REST(user)


def get_following_REST(user):
    r1 = requests.get(f'https://api.twitter.com/2/users/by/username/{user}', headers={'Authorization' : f'Bearer {bear}'})
    
    if r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_following_REST(user)
    elif r1.status_code == 429:
        time.sleep(900)
        return get_following_REST(user)
    elif r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_following_REST(user)

    print(f"Part 1 {r1}")
    id = r1.json()["data"]["id"]
    r1 = requests.get(f'https://api.twitter.com/2/users/{id}/following?user.fields=name&max_results=1000', headers={'Authorization' : f'Bearer {bear}'})

    print(f"Part 2 {r1}")
    names = []
    if r1 and "data" in r1.json():
        for entry in r1.json()["data"]:
            names.append(entry["username"])
        return names
    elif r1.status_code == 429:
        time.sleep(900)
        return get_following_REST(user)
    elif r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_following_REST(user)

def get_profile_picture(user):
    r1 = requests.get(f"https://api.twitter.com/2/users/by/username/{user}?user.fields=profile_image_url", headers={'Authorization' : f'Bearer {bear}'})

    if r1 and "data" in r1.json():
        return r1.json()["data"]["profile_image_url"]
    elif r1 and "errors" in r1.json():
        print(r1.json())
        time.sleep(900)
        return get_profile_picture(user)


if __name__ == "__main__":
    print(get_profile_picture("jack_west24"))