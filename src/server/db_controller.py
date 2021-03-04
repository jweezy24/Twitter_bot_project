import mongoengine
import datetime
from server.models import *


def insert_account(data:dict):
    
    account = Account(twitter_handle=data['twitter_handle'])
    account.name = data['name']
    account.update_date = datetime.datetime.utcnow()
    if "group_type" in data:
        account.group_type = Grouping.objects(name_exact=data["group_type"])
    
    account.save()