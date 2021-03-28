from re import A
import unittest
from mongoengine import connect, disconnect, document
import mongoengine

from mongoengine.connection import _get_db
import sys

from mongoengine.errors import DoesNotExist
from mongoengine.queryset.transform import query
sys.path.append('./src')
from server.models import *


''' Verifies proper usage of models '''

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginecontrollertest', host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        db = _get_db()
        #db.connnection.drop_database('mongoenginetest')

        disconnect()
    
    
    def test_account(self):
        user =  Account(id = 1, twitter_handle= "John21")
        user.name = "John Doe"
        user.save()

        query = Account.objects(twitter_handle = user.twitter_handle).first()

        assert query.twitter_handle == "John21"
        assert query.name == user.name
        #self.assertEqual(actual.twitter_handle, "John21")
    
    def test_grouping(self):
        group1 = Group(name = "Gaming")
        group1.description = 'test gaming group'

        group1.save()
        
        query = Group.objects(name = "Gaming").get()
        
        assert query.name == group1.name

    def test_Non_Existant_User(self):
        self.assertRaises( mongoengine.errors.DoesNotExist, Account.objects(twitter_handle = "Jane").get)

        
        

    def test_account_grouping(self):
        group1 = Group(name = "Political")
        group1.description = 'test second group'

        group1.save()

        account =  Account(id = 2,twitter_handle= "John3")
        account.name = "John"
        account.group_type = group1
        
        account.save()

        query = Account.objects(twitter_handle = "John3").get()

        assert query.group_type.name == group1.name
        assert query.name == "John"


    def test_FollowingConnections(self):
        #create account
        account = Account(id = 3, twitter_handle= "Steve3")
        account.name = 'Steve'
        account.save()

        #create second account
        account2 = Account(id = 4, twitter_handle= "Jane3")
        account2.name = 'Jane'
        account2.save()
        
        #create connection for account to account2
        following = FollowingConnections(following = account2)
        following.distance = 10
        
        #append connection to account connections list
        account.following.append(following)
        account.save()
        #query account
        query_account = Account.objects(twitter_handle = 'Steve3').get()

        assert query_account.following[0].distance == 10
        assert query_account.following[0].following == account2

    def test_FollowerConnections(self):
        #create account
        account = Account(id = 3, twitter_handle= "Steve3")
        account.name = 'Steve'
        account.save()

        #create second account
        account2 = Account(id = 4, twitter_handle= "Jane3")
        account2.name = 'Jane'
        account2.save()
        
        #create connection for account to account2
        follower = FollowerConnections(follower = account2)
        follower.distance = 10
        
        #append connection to account connections list
        account.followers.append(follower)
        account.save()
        #query account
        query_account = Account.objects(twitter_handle = 'Steve3').get()

        assert query_account.followers[0].distance == 10
        assert query_account.followers[0].follower == account2

    def test_Search(self):
        #create account
        account = Account(id = 5,twitter_handle= "Steve1")
        account.name = 'Steve'
        account.save()

        #create second account
        account2 = Account(id = 6, twitter_handle= "Jane2")
        account2.name = 'Jane'
        account2.save()
        
        #create connection for account to account2
        following = FollowingConnections(following = account2)
        following.distance = 10

        #create search
        search = Search(search_handle = account)
        search.following.append(following)
        search.save()
        
        #query account
        query_account = Account.objects(twitter_handle = "Steve1").get()
        #query search with account query
        query_search = Search.objects(search_handle = query_account).get()

        #test
        assert query_search.search_handle == account
        assert query_search.following[0].distance == 10
        

    def test_top_words(self):
        account = Account(id = 7,twitter_handle= "Steve2")
        account.name = 'Steve'
        
        pos = Top_Word()
        pos.word = "test"
        pos.value = 5

        neg = Top_Word()
        neg.word = "twitter"
        neg.value = 20

        account.top_words_positive.append(pos)
        account.top_words_negative.append(neg)

        account.save()

        #query account
        query_account = Account.objects(twitter_handle = "Steve2").get()

        #test
        assert query_account.top_words_positive[0].word == pos.word
        assert query_account.top_words_positive[0].value == 5
        assert query_account.top_words_negative[0].word == neg.word
        assert query_account.top_words_negative[0].value == 20

    #test tweets/favorite tweets embedded document 
    def test_tweets(self):
        account = Account(id = 8,twitter_handle= "Steve4")
        account.name = 'Steve'
        
        tweet = Tweet(id = 1)
        tweet.text = "Whats up"

        account.tweets.append(tweet)
        

        account.save()

        #query account
        query_account = Account.objects(twitter_handle = "Steve4").get()

        #test
        assert query_account.tweets[0] == tweet
        
    def test_context(self):
        account = Account(id = 9,twitter_handle= "Steve5")
        account.name = 'Steve'
        
        context = Context(id = 1)
        context.text = "test"

        domain = Domain(id = 1)
        domain.name = "test2"
        domain.description = "testing"

        entity = Entity(id = 1)
        entity.name = "test2"
        entity.description = "testing"

        contextAnnotation = Context_Annotation()
        contextAnnotation.domain = domain
        contextAnnotation.entity = entity

        context.context_annotations.append(contextAnnotation)

        account.tweets_context.append(context)
        

        account.save()

        #query account
        query_account = Account.objects(twitter_handle = "Steve5").get()

        #test
        assert query_account.tweets_context[0] == context
        assert query_account.tweets_context[0].context_annotations[0] == contextAnnotation
        