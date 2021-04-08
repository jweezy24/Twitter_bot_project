import unittest
from mongoengine import connect, disconnect
import sys


#sys.path.append('.')
sys.path.append('./src')
#sys.path.insert(1, '../src/server/')

import server.db_controller as controller
import server.models as models

''' Verifies proper usage of db controller '''

class TestController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host="mongomock://localhost")

        

    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    def test_insert_group(self):
        group = {'name': "Gaming", 'description' : "test Gaming"}
        
        controller.insert_group(group)

        query = models.Group.objects(name = "Gaming").get()

        assert query.name == group['name']

    def test_create_account(self):
        controller.insert_account({"twitter_handle":"John21", "name" :"John Doe"})

        actual = models.Account.objects(twitter_handle = "John21").first()
        assert actual.twitter_handle == "John21"
        assert actual.name == "John Doe"
    
    def test_insert_accounts(self):
        accounts = [{"twitter_handle":"John2", "name" :"Johnny"},{"twitter_handle":"Jane231", "name" :"Jane"}]

        controller.insert_accounts(accounts)

        query1 = models.Account.objects(twitter_handle = "John2").get()
        query2 = models.Account.objects(twitter_handle = "Jane231").get()

        assert query1.name == "Johnny"
        assert query2.name == "Jane"

    def test_get_group(self):
        account = {"twitter_handle":"Jane4", "name" :"Jane Doe", 'group_type':'Politics'}
        
        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane4").get()

        assert query.group_type.name == 'Politics'

    def test_account_with_connection(self):
        account = {"twitter_handle":"Jane5", "name" :"Jane Doe", 'group_type':'Politics', 
        "connections": [{"following":{"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':'Politics'},'distance':10}]}

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane5").get()
        query2 = models.Account.objects(twitter_handle = "Jane6").get()

        assert query.connections[0].following.twitter_handle == "Jane6"
    
    #insert account or update if it exists
    def test_insert_account_update(self):
        account = {"twitter_handle":"Jane7", "name" :"Jane Doe", 'group_type':'Politics', 
        "connections": [{"following":{"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':'Politics'},'distance':10}]}
        
        controller.insert_account(account)

        account['name'] = 'Jane Smith'
        account['connections'].clear()
        account['connections'].append({"following":{"twitter_handle":"Jane4", "name" :"Jane Doe", 'group_type':'Politics'},'distance':5})

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane7").get()

        assert query.name == "Jane Smith"
        assert query.connections[0].following.twitter_handle == "Jane4"

    def test_find_previous_search(self):
        account = controller.insert_account({"twitter_handle":"John4", "name" :"John Doe", 'group_type':'Politics'})
        connection = controller.generate_following_connection({"following":{"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':'Politics'},'distance':10})
        
        search = models.Search(search_handle = account)
        search.connections.append(connection)
        search.date = account.update_date
        print(search.date)
        search.save()

        query = controller.find_previous_search(account.twitter_handle)
        print(query.date)
        assert query != None
        
        assert query.connections[0].following.twitter_handle == "Jane6"

    def test_create_search(self):
        account = controller.insert_account({"twitter_handle":"John55", "name" :"John Doe", 'group_type':'Politics', "connections": [{"following":{"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':'Politics'},'distance':10}]})
        
        controller.create_search(account)

        query = models.Search.objects(search_handle = account).get()

        assert query.search_handle.twitter_handle == account.twitter_handle
    