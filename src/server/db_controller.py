from re import search
from typing import Dict
import mongoengine
import datetime
from server.models import *


#return account if it exists else return None
def get_account(twitter_handle:str):
    try:
        return Account.objects(twitter_handle = twitter_handle).get()
    except mongoengine.errors.DoesNotExist:
        return None

def insert_account(data:dict):
    
    account = get_account(data['twitter_handle'])
    if account is None:
        account = Account(id = data['id'],twitter_handle=data['twitter_handle'])
    
    account.name = data['name']
    account.update_date = datetime.datetime.utcnow()
    # check if group_type is present and if not in database insert it 
    # not sure if this is what we whant though maybe we dont want it to add a new group
    if "group_type" in data:
        group = get_group(data['group_type'])
        if group is not None:
            account.group_type = group
        else:
            insert_group({'name':data['group_type']})
            account.group_type = get_group(data['group_type'])
    if "following" in data or "followers" in data:
        if len(account.following) > 0 or len(account.followers) > 0: 
            create_search(account)
            account.following.clear()
            account.followers.clear()
    #insert following connections after creating them if account already has connections we create a search to store the old search
    if "following" in data:
        for connection in data['following']:
            account.following.append(generate_following_connection(connection))
    if "followers" in data:
        for connection in data['followers']:
            account.followers.append(generate_follower_connection(connection))
    
    account.save()
        
    return account

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