from re import A, search
from typing import Dict
import mongoengine
import datetime
import json
from pymongo import MongoClient
import time
from hashlib import *
from server.models import *


#return account if it exists else return None
def get_account(twitter_handle:str):
    try:
        return Account.objects(twitter_handle = twitter_handle).get()
    except mongoengine.errors.DoesNotExist as e:
        print(e)
        return None

#return account if it exists else return None
def get_account_pymongo(twitter_handle:str):
    with MongoClient('localhost', 27017) as client:
        db = client['TwitterBotDB']
        collection = db['account']
        x = collection.find({"twitter_handle" : twitter_handle})
        results = []
        for result in x:
            results.append(result)
    
    return results[0]

def get_account_by_id_pymongo(id_:str):
    with MongoClient('localhost', 27017) as client:
        db = client['TwitterBotDB']
        collection = db['account']
        x = collection.find({"_id" : id_})
        results = []
        for result in x:
            results.append(result)
    
    return results[0]

def increment_counter(user):
    with MongoClient('localhost', 27017) as client:
        db = client['TwitterBotDB']
        collection = db['account']
        db.collection.update(
            { "twitter_handle": user },
            { "$inc": { "requested": -2}})


def get_max_id(val,username):
    acc = get_account(username)
    if acc != None:
        if val == "tweets":
            m = -1
            for i in acc.tweets:
                if int(i.id) > m:
                    m = int(i.id)
            return m
        elif val == "tweets_context":
            m = -1
            for i in acc.tweets_context:
                if int(i.id) > m:
                    m = int(i.id)
            return m
        elif val == "favorites":
            m = -1
            for i in acc.favorite_tweets:
                if int(i.id) > m:
                    m = int(i.id)
            return m
        elif val == "favorites_context":
            m = -1
            for i in acc.favorite_context:
                if int(i.id) > m:
                    m = int(i.id)
            return m
    else:
        return -1 
def insert_account(data:dict, tinydb=False):
    
    account = get_account(data['twitter_handle'])
    if account is None:
        account = Account(id = data['id'],twitter_handle=data['twitter_handle'])
    
    if "name" not in data:
        account.name = data['twitter_handle']
    else:
        account.name = data['name']
    account.update_date = datetime.datetime.utcnow()
    # check if group_type is present and if not in database insert it 
    # not sure if this is what we whant though maybe we dont want it to add a new group
    if "profile_image_url" in data:
        account.profile_image_url = data['profile_image_url']
    if "group_type" in data:
        group = get_group(data['group_type']['name'])
        if group is not None:
            account.group_type = group
        else:
            insert_group(data['group_type'])
            account.group_type = get_group(data['group_type'])
    if ("following" in data or "followers" in data) and not tinydb:
        if len(account.following) > 0 or len(account.followers) > 0: 
            create_search(account)
            clear_account(account)
    #insert following connections after creating them if account already has connections we create a search to store the old search
    if "following" in data:
        for connection in data['following'].keys():
            if not tinydb:
                account.following.append(generate_following_connection(connection))
            else:
                c = FollowingConnections()
                user_ = data['following'][connection]["id"]
                acc_info = {}
                acc_info.update({"twitter_handle": user_})
                id_ = sha256(user_.encode("utf-8")).hexdigest()
                acc_info.update({"id": id_})
                insert_account(acc_info)

                acc = get_account(user_)
                c.following = acc
                c.distance = 0
                print(c.following.twitter_handle)
                account.following.append(c)
    
    if "followers" in data:
        for connection in data['followers']:
            if not tinydb:
                account.followers.append(generate_follower_connection(connection))
            else:
                c = FollowerConnections()
                user_ = connection
                acc_info = {}
                acc_info.update({"twitter_handle": user_})
                id_ = sha256(user_.encode("utf-8")).hexdigest()
                acc_info.update({"id": id_})
                insert_account(acc_info)

                acc = get_account(user_)
                c.follower = acc
                c.distance = 0
                account.followers.append(c)

    if "top_words_positive" in data:
        for word in data['top_words_positive']:
            account.top_words_positive.append(generate_top_word(word))
    if "top_words_negative" in data:
        for word in data['top_words_negative']:
            account.top_words_negative.append(generate_top_word(word))
    if "tweets" in data:
        t = data['tweets']
        if type(t) == type([]):
            for tweet in t:
                account.tweets.append(generate_tweet(tweet))
        if type(t) == type({}):
            for key in t.keys():
                tweet = t[key]
                account.tweets.append(generate_tweet(tweet))
    if "favorite_tbl" in data:
        t = data['favorite_tbl']
        if type(t) == type([]):
            for tweet in t:
                account.favorite_tweets.append(generate_tweet(tweet))
        if type(t) == type({}):
            for key in t.keys():
                tweet = t[key]
                account.favorite_tweets.append(generate_tweet(tweet))
    if "tweets_context" in data:
        t = data['tweets_context']
        if type(t) == type([]):
            for tweet in t:
                account.tweets_context.append(generate_context(tweet))
        if type(t) == type({}):
            for key in t.keys():
                tweet = t[key]
                account.tweets_context.append(generate_context(tweet))    
    if "favorites_context" in data:
        t = data['favorites_context']
        if type(t) == type([]):
            for tweet in t:
                account.favorite_context.append(generate_context(tweet))
        if type(t) == type({}):
            for key in t.keys():
                tweet = t[key]
                account.favorite_context.append(generate_context(tweet))
    if "favorite_context" in data:
        t = data['favorite_context']
        if type(t) == type([]):
            for tweet in t:
                account.favorite_context.append(generate_context(tweet))
        if type(t) == type({}):
            for key in t.keys():
                tweet = t[key]
                account.favorite_context.append(generate_context(tweet))            
    
    account.save()
        
    return account

def generate_tweet(data:dict):
    tweet = Tweet(id = str(data['id']))
    tweet.created_at = data['created_at']
    tweet.text = data['text']
    return tweet

def generate_top_word(data:dict):
    top_word = Top_Word()
    top_word.word = data['word']
    top_word.value = data['value']
    return top_word

def generate_context(data:dict):
    context = Context(id = str(data['id']))
    context.text = data['text']
    if 'context_annotations' in data:
        for annotation in data['context_annotations']:
            print(annotation)
            context.context_annotations.append(generate_context_annotation(annotation))
    return context

def generate_context_annotation(data:dict):
    context_annotation = Context_Annotation()
    context_annotation.domain = generate_domain(data['domain'])
    context_annotation.entity = generate_entity(data['entity'])
    return context_annotation

def generate_domain(data:dict):
    domain = Domain(id = str(data['id']))
    domain.name = data['name']
    if 'description' in data:
        domain.description = data['description']
    return domain

def generate_entity(data:dict):
    entity = Entity(id = str(data['id']))
    entity.name = data['name']
    if 'description' in data:
        entity.description =data['description']
    return entity

def clear_account(account):
    account.following.clear()
    account.followers.clear()
    account.top_words_positive.clear()
    account.top_words_negative.clear()
    account.tweets.clear()
    account.favorite_tweets.clear()
    account.favorite_context.clear()
    account.tweets_context.clear()

def update_account(account:Account, data:dict):
    account.name = data['name']
    account.update_date = datetime.datetime.utcnow()

#add the group into the database and returns if it worksTODO
def insert_group(data:dict):
    group = Group(name = data['name'])
    if  'description' in data:
        group.description = data['description']
    group.save()
    return group

#insert an list of accounts
def insert_accounts(data:list):
    for account in data:
        insert_account(account)

#return group if it exists else return None
def get_group(name:str):
    try:
        return Group.objects(name = name).get()
        
    except mongoengine.errors.DoesNotExist:
        return None

#used by insert account to create the following connections if it doesnt exist it inserts the account this is recursive
def generate_following_connection(data:dict):
    connection = FollowingConnections()
    following = get_account(data['following']['twitter_handle'])
    if following is not None:
        connection.following = following
    else:
        following = insert_account(data['following'])
        connection.following = following
    connection.distance = data['distance']
    return connection

#used by insert account to create the following connections if it doesnt exist it inserts the account this is recursive
def generate_follower_connection(data:dict):
    connection = FollowerConnections()
    follower = get_account(data['follower']['twitter_handle'])
    if follower is not None:
        connection.follower = follower
    else:
        follower = insert_account(data['follower'])
        connection.follower = follower
    connection.distance = data['distance']
    return connection

def create_search(account:Account):
    search = Search(search_handle = account)
    search.following = account.following
    search.followers = account.followers
    search.top_words_positve = account.top_words_positive
    search.top_words_negative = account.top_words_negative
    search.tweets = account.tweets
    search.tweets_context = account.tweets_context
    search.favorite_tweets = account.favorite_tweets
    search.favorite_context = account.favorite_context
    search.date = account.update_date
    search.save()

def find_previous_searchs(twitter_handle:str):
    try:
        account = get_account(twitter_handle)
        return Search.objects(search_handle = account)
    except mongoengine.errors.DoesNotExist:
        return None

def create_context_annotation(data:Dict):
    print(data)