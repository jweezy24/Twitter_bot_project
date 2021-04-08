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
        user =  Account(twitter_handle= "John21")
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

        account =  Account(twitter_handle= "John3")
        account.name = "John"
        account.group_type = group1
        
        account.save()

        query = Account.objects(twitter_handle = "John3").get()

        assert query.group_type.name == group1.name
        assert query.name == "John"


    def test_FollowingConnections(self):
        #create account
        account = Account(twitter_handle= "Steve3")
        account.name = 'Steve'
        account.save()

        #create second account
        account2 = Account(twitter_handle= "Jane3")
        account2.name = 'Jane'
        account2.save()
        
        #create connection for account to account2
        following = FollowingConnections(following = account2)
        following.distance = 10

        #append connection to account connections list
        account.connections.append(following)

        #query account
        query_account = Account.objects(twitter_handle = 'Steve3').get()

        assert query_account

    def test_Search(self):
        #create account
        account = Account(twitter_handle= "Steve1")
        account.name = 'Steve'
        account.save()

        #create second account
        account2 = Account(twitter_handle= "Jane2")
        account2.name = 'Jane'
        account2.save()
        
        #create connection for account to account2
        following = FollowingConnections(following = account2)
        following.distance = 10

        #create search
        search = Search(search_handle = account)
        search.connections.append(following)
        search.save()
        
        #query account
        query_account = Account.objects(twitter_handle = "Steve1").get()
        #query search with account query
        query_search = Search.objects(search_handle = query_account).get()

        #test
        assert query_search.search_handle == account
        assert query_search.connections[0].distance == 10
        