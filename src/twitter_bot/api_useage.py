import os
import sys
import twitter
import tweepy
import time
from REST_api_calls import *
from tiny_db_calls import *
sys.path.append('./src')
from categorization_algorithm import *
from server.db_controller import *
from hashlib import *

api_key = os.environ['APIKEY']
api_secret = os.environ['APISECRET']
username = os.environ['TWITTERUSER']
password = os.environ['TWITTERPASS']

use_mongo = False


api = twitter.Api(consumer_key=username,
                  consumer_secret=password,
                  access_token_key=api_key,
                  access_token_secret=api_secret)

auth = tweepy.OAuthHandler(username, password)

# set access to user's access key and access secret
auth.set_access_token(api_key, api_secret)
api2 = tweepy.API(auth, wait_on_rate_limit=True,
                  wait_on_rate_limit_notify=True)

''' Returns a list of favorites in a Json format '''


def get_favorites(user, total=100, use_mongo=False):
    favs = []
    count = 0
    data = api2.get_user(user)
    created = data.created_at
    if not use_mongo:
        max_id = get_maximum_id(user, "favorite_tbl")
    else:
        max_id = get_max_id( "favorites", user)
    
    if max_id == None or max_id==-1:
        cur = tweepy.Cursor(api2.favorites, id=user, since=created).pages()
    else:
        cur = tweepy.Cursor(api2.favorites, id=user,
                            since_id=max_id).pages()

    for page in cur:
        if count >= total:
            break
        for entry in page:
            if count >= total:
                break
            if not search_value(entry._json["id"], user, table="favorite_tbl") and not use_mongo:
                save_value(entry._json, userid=user, table="favorite_tbl")
                count += 1
                print("ADDED FAVORITE")
            elif use_mongo:
                
                acc = get_account(user)
                
                if acc == None:
                    acc_info = {}
                    acc_info.update({"twitter_handle": user})
                    id_ = sha256(user.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user)

                    acc.favorite_tweets.append(generate_tweet(entry._json))
                    acc.save()
                    count+=1
                    continue

                acc.favorite_tweets.append(generate_tweet(entry._json))
                acc.save()
                
                count+=1
    print(f"ADDED {count} NEW FAVORITES")
    return favs


''' 
    Returns a list of favorites in a Json format.
    This method focuses on favorites with context.
    input:
        user = screen name of the user you would like to get their favorites from
        total (optional) = the total number of favorites you would like to retrieve. default=100
    output:
        a list of favorites that are specficially contextual. 
'''


def get_favorites_with_context(user, total=100, use_mongo=False):
    favs = []
    count = 0
    data = api2.get_user(user)
    created = data.created_at
    if not use_mongo:
        max_id = get_maximum_id(user, "favorite_with_context_tbl")
    else:
        max_id = get_max_id( "favorites_context", user)
    
    if max_id == None or max_id==-1:
        cur = tweepy.Cursor(api2.favorites, id=user, since=created).pages()
    else:
        cur = tweepy.Cursor(api2.favorites, id=user,
                            since_id=max_id).pages()

    for page in cur:
        if count >= total:
            break
        for entry in page:
            if count >= total:
                break
            if not search_value(entry._json["id"], user, table="favorite_tbl") and not use_mongo:
                save_value(entry._json, userid=user, table="favorite_tbl")
                count += 1
                print("ADDED FAVORITE")
            elif use_mongo:
                
                acc = get_account(user)
                
                if acc == None:
                    acc_info = {}
                    acc_info.update({"twitter_handle": user})
                    id_ = sha256(user.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user)
                    t = get_tweet_context(entry._json["id"])
                    if t != None:
                        acc.favorite_context.append(generate_context(t))
                        acc.save()
                    count+=1
                    continue
                
                t = get_tweet_context(entry._json["id"])
                if t != None:
                    acc.favorite_context.append(generate_context(t))
                    acc.save()
                
                count+=1


''' 
    Returns a list of followers
    Data Structure used: List
    Input: A string of the user's screen name
    Output: A list of strings with each followers' screen_name
'''


def get_followers(user, mongo=False):
    names = []
    count = 0
    twitter_followers = get_followers_REST(user)
    if not mongo:
        current_followers = get_all_table_entries(user, "followers")
    else:
        u = get_account(user)
        if u != None:
            current_followers = u.followers
        else:
            current_followers = []

    print(f"Table size = {len(current_followers)} Twitter record = {len(twitter_followers)}")
    if len(current_followers) != len(twitter_followers):
        if not mongo:
            for follower in current_followers:
                name = follower["id"]
                if name not in twitter_followers:
                    print(f"Removed {name}")
                    if not mongo:
                        remove_from_table(user, "followers", name)

            for entry in twitter_followers:
                cached_entry = {"id": entry}
                if not search_value(cached_entry["id"], user, table="followers"):
                    print(f"Saved Followers {entry}")
                    if not mongo:
                        save_value(cached_entry, userid=user, table="followers")
        else:

            if u != None:
                final_list = []
                for user_ in twitter_followers:
                    connection = FollowerConnections()
                    acc_info = {}
                    acc_info.update({"twitter_handle": user_})
                    id_ = sha256(user_.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user_)
                    connection.follower = acc
                    connection.distance = 0
                    final_list.append(connection)
                u.followers = final_list
                u.save()

            else:
                acc_info = {}
                acc_info.update({"twitter_handle": user})
                id_ = sha256(user.encode("utf-8")).hexdigest()
                acc_info.update({"id": id_})
                insert_account(acc_info)
                u = get_account(user)
                final_list = []

                for user_ in twitter_followers:
                    connection = FollowerConnections()
                    acc_info = {}
                    acc_info.update({"twitter_handle": user_})
                    id_ = sha256(user_.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user_)
                    connection.follower = acc
                    connection.distance = 0
                    final_list.append(connection)
                u.follwers = final_list
                u.save()
    

def get_following(user, mongo=False):
    names = []
    count = 0
    twitter_followers = get_following_REST(user)
    u = None
    if not mongo:
        current_followers = get_all_table_entries(user, "following")
    else:
        u = get_account(user)
        if u != None:
            current_followers = u.following
        else:
            current_followers = []


    if len(current_followers) != len(twitter_followers):
        if not mongo:
            for follower in current_followers:
                name = follower["id"]
                if name not in twitter_followers:
                    print(f"Removed {name}")
                    remove_from_table(user, "following", name)

            for entry in twitter_followers:
                cached_entry = {"id": entry}
                if not search_value(cached_entry["id"], user, table="following"):
                    print(f"Saved Following {entry}")
                    save_value(cached_entry, userid=user, table="following")
        else:
            if u != None:
                final_list = []
                for user_ in twitter_followers:
                    connection = FollowingConnections()
                    acc_info = {}
                    acc_info.update({"twitter_handle": user_})
                    id_ = sha256(user_.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user_)
                    connection.following = acc
                    connection.distance = 0
                    final_list.append(connection)
                u.following = final_list
                u.save()

            else:
                acc_info = {}
                acc_info.update({"twitter_handle": user})
                id_ = sha256(user.encode("utf-8")).hexdigest()
                acc_info.update({"id": id_})
                insert_account(acc_info)
                u = get_account(user)
                final_list = []

                for user_ in twitter_followers:
                    connection = FollowingConnections()
                    acc_info = {}
                    acc_info.update({"twitter_handle": user_})
                    id_ = sha256(user_.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user_)
                    connection.following = acc
                    connection.distance = 0
                    final_list.append(connection)
                u.following = final_list
                u.save()


'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we are going to examine
Output: a list of tweets of that user.
'''


def retrieve_all_tweets(user, max_id=-1, total=100, use_mongo=False):

    data = api2.get_user(user)
    created = data.created_at
    favs = []
    count = 0
    if not use_mongo:
        max_id = get_maximum_id(user, "tweets")
    else:
        max_id = get_max_id( "tweets", user)
    
    if max_id == None or max_id==-1:
        cur = tweepy.Cursor(api2.user_timeline, id=user, since=created).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,
                            since_id=max_id).pages()
    print(use_mongo)
    count = 0

    for page in cur:
        if count >= total:
                break
        for entry in page:
            if count >= total:
                break

            if not search_value(entry._json["id"], user, table="tweets") and not use_mongo:
                print(f"Saved Tweet")
                
                save_value(entry._json, userid=user, table="tweets")
                count += 1
            
            elif use_mongo:
                
                acc = get_account(user)
                
                if acc == None:
                    acc_info = {}
                    acc_info.update({"twitter_handle": user})
                    id_ = sha256(user.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)

                    acc = get_account(user)

                    acc.tweets.append(generate_tweet(entry._json))
                    acc.save()
                    count+=1
                    continue

                acc.tweets.append(generate_tweet(entry._json))
                acc.save()
                
                count+=1

    print(f"Saved {count} Tweets from {user}")


'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we want to give context to.
TODO: We can remove the intial api call and iterate through the user's tweet ids list.
'''


def save_all_tweets_context(user, max_id=-1,total=100,use_mongo=False):

    data = api2.get_user(user)
    created = data.created_at
    favs = []
    count = 0
    if not use_mongo:
        max_id = get_maximum_id(user, "tweets_context")
    else:
        max_id = get_max_id( "tweets_context", user)

    if max_id == None or max_id == -1:
        cur = tweepy.Cursor(api2.user_timeline, id=user, since=created).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,
                            since_id=max_id).pages()

    for page in cur:
        if count >= total:
                break
        for entry in page:
            if count >= total:
                break

            if not search_value(entry._json["id"], user, table="tweets_context") and not use_mongo:
                save_value(entry._json, userid=user, table="tweets_context")
            elif use_mongo:
                
                acc = get_account(user)
                
                if acc == None:
                    acc_info = {}
                    acc_info.update({"twitter_handle": user})
                    id_ = sha256(user.encode("utf-8")).hexdigest()
                    acc_info.update({"id": id_})
                    insert_account(acc_info)
                    
                    acc = get_account(user)

                    print(entry._json["id"])
                    t = get_tweet_context(entry._json["id"])
                    print(t)
                    if t != None:
                        acc.tweets_context.append(generate_context(t))
                        acc.save()
                    count+=1
                    continue

                t = get_tweet_context(entry._json["id"])
                print(t)
                if t != None:
                    acc.tweets_context.append(generate_context(t))
                    acc.save()
                print("SAVED CONTEXT WITH TWEET MONGO")
                
                count+=1

''' 
Checks to see if a user is private. If so we cannot gather data and it causes timeouts.
Verifying a private user earlier
'''


def is_private(user):
    u = api2.get_user(user)
    return u.protected

def init_user(user, update=False):
    acc = get_account(user)
    if acc == None:
        acc_info = {}
        acc_info.update({"twitter_handle": user})
        id_ = sha256(user.encode("utf-8")).hexdigest()
        acc_info.update({"id": id_})
        twitter_followers = get_followers_REST(user)
        twitter_following = get_following_REST(user)
        profile_pic = get_profile_picture(user)
        acc_info.update({"total_followers": len(twitter_followers)})
        acc_info.update({"total_following": len(twitter_following)})
        acc_info.update({"profile_image_url": profile_pic})
        insert_account(acc_info)
        print(f"added {user}")

    elif update and acc != None:
        twitter_followers = get_followers_REST(user)
        twitter_following = get_following_REST(user)
        profile_pic = get_profile_picture(user)
        acc.total_followers = len(twitter_followers)
        print( len(twitter_followers))
        print( twitter_followers)
        acc.total_following = len(twitter_following)
        acc.profile_image_url = profile_pic
        acc.save()
        print(f"updated {user}")
    
    elif "total_followers" not in dir(acc) or "total_following" not in dir(acc) or "profile_image_url" not in dir(acc):
        twitter_followers = get_followers_REST(user)
        twitter_following = get_following_REST(user)
        profile_pic = get_profile_picture(user)
        acc.total_followers = len(twitter_followers)
        print( len(twitter_followers))
        print( twitter_followers)
        acc.total_following = len(twitter_following)
        acc.profile_image_url = profile_pic
        acc.save()


def build_user_web(user, mongo=False):
    print(f"Creating user web for {user}")
    u = get_account(user)
    init_user(user)
    get_followers(user, mongo=mongo)
    followers = u.followers 
    get_following(user, mongo=mongo)
    following = u.following

    print(f"CHECKING {user}")
    retrieve_all_tweets(user,use_mongo=mongo)
    print(f"Got Tweets for {user}")
    save_all_tweets_context(user, use_mongo=mongo)
    print(f"Got Tweets with context for {user}")
    get_favorites(user, use_mongo=mongo)
    print(f"Got favorites for {user}")
    get_favorites_with_context(user, use_mongo=mongo)
    print(f"Got favorites with context for {user}")

    print(f"{user} is Following {following}")
    print(f"{user} is Followed by {followers}")

    for people in followers:
        people = people.follower.twitter_handle
        if not is_private(people):
            init_user(people, update=True)
            print(f"CHECKING {people}")
            retrieve_all_tweets(people,use_mongo=mongo)
            print(f"Got Tweets for {people}")
            save_all_tweets_context(people, use_mongo=mongo)
            print(f"Got Tweets with context for {people}")
            get_favorites(people, use_mongo=mongo)
            print(f"Got favorites for {people}")
            get_favorites_with_context(people, use_mongo=mongo)
            print(f"Got favorites with context for {people}")
        else:
            print("Private user.")

    for people in following:
        people = people.following.twitter_handle
        if not is_private(people):
            init_user(people, update=True)
            print(f"CHECKING {people}")
            retrieve_all_tweets(people,use_mongo=mongo)
            print(f"Got Tweets for {people}")
            save_all_tweets_context(people, use_mongo=mongo)
            print(f"Got Tweets with context for {people}")
            get_favorites(people, use_mongo=mongo)
            print(f"Got favorites for {people}")
            get_favorites_with_context(people, use_mongo=mongo)
            print(f"Got favorites with context for {people}")
        else:
            print("Private user.")


if __name__ == "__main__":
    # Below average twitter account in size
    # build_user_web('jack_west24',mongo=True)
    # Normal twitter account with consistant activity
    build_user_web('alittl3ton13', mongo=True)
    # Very little activity and size
    build_user_web('gubaladavid', mongo=True)
    # Large activity and size
    build_user_web('theneedledrop', mongo=True)
