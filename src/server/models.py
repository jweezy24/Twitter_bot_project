from flask_mongoengine import MongoEngine, connection
import datetime
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.queryset.base import CASCADE



#from server import db
import mongoengine as me
db:MongoEngine

class Group(me.Document):
    name = me.StringField(required = True)
    description = me.StringField()


class FollowingConnections(me.EmbeddedDocument):
    following = me.ReferenceField('Account')
    distance  = me.IntField()

class Account(me.Document):
    twitter_handle = me.StringField(required = True)
    name           = me.StringField()
    update_date    = me.DateField(default=datetime.datetime.utcnow)
    group_type     = me.ReferenceField(Group)
    connections    = me.ListField(EmbeddedDocumentField(FollowingConnections))





class Search(me.Document):
    search_handle = me.ReferenceField(Account, required=True, reverse_delete_rule=CASCADE)
    connections = me.ListField(EmbeddedDocumentField(FollowingConnections))
