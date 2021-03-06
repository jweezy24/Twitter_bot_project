from flask_mongoengine import MongoEngine, connection
import datetime
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.queryset.base import CASCADE



#from server import db
import mongoengine as me
db:MongoEngine

class Grouping(me.Document):
    name = me.StringField(required = True)
    description = me.StringField()


class FollowingConnections(me.EmbeddedDocument):
    following_id = me.ReferenceField('Account')
    distance     = me.IntField()

class Account(me.Document):
    twitter_handle = me.StringField(required = True)
    name           = me.StringField()
    update_date    = me.DateField(default=datetime.datetime.utcnow)
    group_type     = me.ReferenceField(Grouping)
    connections    = me.ListField(EmbeddedDocumentField(FollowingConnections))





class Search(me.Document):
    searched_id = me.ReferenceField(Account, required=True, reverse_delete_rule=CASCADE,)
    search_handle = me.StringField()
    connections = me.ListField(EmbeddedDocumentField(FollowingConnections))
