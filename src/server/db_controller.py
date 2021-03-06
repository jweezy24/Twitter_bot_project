import mongoengine
import datetime
from server.models import *


def insert_account(data:dict):
    
    account = Account(twitter_handle=data['twitter_handle'])
    account.name = data['name']
    account.update_date = datetime.datetime.utcnow()
    # check if group_type is present and if not in database insert it 
    # not sure if this is what we whant though maybe we donr want it to add a new group
    if "group_type" in data:
        group = get_group(data['group_type'])
        if group is not None:
            account.group_type = group
        else:
            insert_group({'name':data['group_type']})
            account.group_type = get_group(data['group_type'])
    if "connections" in data:
        for connection in data['connections']:
            account.connections.append(generate_following_connection(connection))
    
    account.save()
    return account

def insert_group(data:dict):
    group = Group(name = data['name'])
    if  'description' in data:
        group.description = data['description']
    group.save()
    return group

def insert_accounts(data:list):
    for account in data:
        insert_account(account)

def get_group(name:str):
    try:
        return Group.objects(name = name).get()
        
    except mongoengine.errors.DoesNotExist:
        return None

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

    
    

def get_account(twitter_handle:str):
    try:
        return Account.objects(twitter_handle = twitter_handle).get()
    except mongoengine.errors.DoesNotExist:
        return None