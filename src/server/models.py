from flask_mongoengine import MongoEngine, connection
import datetime
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.queryset.base import CASCADE
import mongoengine as me

db:MongoEngine

class Group(me.Document):
    name = me.StringField(required = True)
    description = me.StringField()

#this is the following
class FollowingConnections(me.EmbeddedDocument):
    following = me.ReferenceField('Account')
    distance  = me.IntField()
#followerConnections same as above
class FollowerConnections(me.EmbeddedDocument):
    follower = me.ReferenceField('Account')
    distance  = me.IntField()

#top_words
class Top_Words(me.EmbeddedDocument):
    word = me.StringField(required = True)
    count = me.IntField(required = True)
    
class Tweet(me.EmbeddedDocument):
    id = me.IntField(primary_key = True)
    created_at = me.DateField()
    text = me.StringField()


#used by context annotation
class Domain(me.EmbeddedDocument):
    id = me.IntField(primary_key = True)
    name = me.StringField()
    description = me.StringField()

#used by context annotation
class Entity(me.EmbeddedDocument):
    id = me.IntField(primary_key = True)
    name = me.StringField()
    description = me.StringField()

#used by context 
class Context_Annotation(me.EmbeddedDocument):
    domain = me.EmbeddedDocumentField(Domain)
    entity = me.EmbeddedDocumentField(Entity)

class Context(me.EmbeddedDocument):
    id = me.IntField(primary_key = True)
    text = me.StringField()
    context_annotations = me.EmbeddedDocumentListField(Context_Annotation)

#twitterAccount
class Account(me.Document):
    id                 = me.IntField(primary_key = True)
    twitter_handle     = me.StringField(required = True, unique = True)
    name               = me.StringField()
    update_date        = me.DateField(default=datetime.datetime.utcnow)
    group_type         = me.ReferenceField(Group)
    profile_image_url  = me.URLField()
    following          = me.EmbeddedDocumentListField(FollowingConnections)
    followers          = me.EmbeddedDocumentListField(FollowerConnections)
    top_words_positve  = me.EmbeddedDocumentListField(Top_Words)
    top_words_negative = me.EmbeddedDocumentListField(Top_Words)
    tweets             = me.EmbeddedDocumentListField(Tweet)
    tweets_context     = me.EmbeddedDocumentListField(Context)
    favorite_tweets    = me.EmbeddedDocumentListField(Tweet)
    favorite_context   = me.EmbeddedDocumentListField(Context)




#this might be usefull to look at old results
class Search(me.Document):
    search_handle = me.ReferenceField(Account, required=True, reverse_delete_rule=CASCADE)
    followers = me.ListField(EmbeddedDocumentField(FollowingConnections))
    following          = me.EmbeddedDocumentListField(FollowingConnections)
    top_words_positve  = me.EmbeddedDocumentListField(Top_Words)
    top_words_negative = me.EmbeddedDocumentListField(Top_Words)
    tweets             = me.EmbeddedDocumentListField(Tweet)
    tweets_context     = me.EmbeddedDocumentListField(Context)
    favorite_tweets    = me.EmbeddedDocumentListField(Tweet)
    favorite_context   = me.EmbeddedDocumentListField(Context)
    date = me.DateField(default=datetime.datetime.utcnow)
