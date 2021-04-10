import unittest
from mongoengine import connect, disconnect
import sys


#sys.path.append('.')
sys.path.append('../src')
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
        controller.insert_account({"id":1 ,"twitter_handle":"John21", "name" :"John Doe"})

        actual = models.Account.objects(twitter_handle = "John21").first()
        assert actual.twitter_handle == "John21"
        assert actual.name == "John Doe"
    
    def test_insert_accounts(self):
        accounts = [{"id":2,"twitter_handle":"John2", "name" :"Johnny"},{"id":3,"twitter_handle":"Jane231", "name" :"Jane"}]

        controller.insert_accounts(accounts)

        query1 = models.Account.objects(twitter_handle = "John2").get()
        query2 = models.Account.objects(twitter_handle = "Jane231").get()

        assert query1.name == "Johnny"
        assert query2.name == "Jane"

    def test_get_account(self):
        account = models.Account(id = 7, twitter_handle = "John84")
        account.name = "johnnyboy"
        account.save()
        query = models.Account.objects(twitter_handle = "John84").get()

        assert query.name == "johnnyboy"
        

    def test_get_group(self):
        account = {"id":4, "twitter_handle":"Jane4", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}}
        
        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane4").get()
        group = controller.get_group("Politics")
        assert group.description == "test"

    def test_account_with_following(self):
        account = {"id":13,"twitter_handle":"Jane12", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}, 
        "following": [{"following":{"id":18,"twitter_handle":"Jane11", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':10}]}

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane12").get()
        #query2 = models.Account.objects(twitter_handle = "Jane11").get()

        assert query.following[0].following.twitter_handle == "Jane11"
        assert query.following[0].distance == 10
    
    def test_account_with_follower(self):
        account = {"id":5,"twitter_handle":"Jane5", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}, 
        "followers": [{"follower":{"id":6,"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':10}]}

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane5").get()
        #query2 = models.Account.objects(twitter_handle = "Jane6").get()

        assert query.followers[0].follower.twitter_handle == "Jane6"
        assert query.followers[0].distance == 10
    
    #insert account or update if it exists
    def test_insert_account_update(self):
        account = {"id": 9,"twitter_handle":"Jane7", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}, 
        "following": [{"following":{"id":9,"twitter_handle":"Jane9", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':10}]}
        
        controller.insert_account(account)

        account['name'] = 'Jane Smith'
        account['following'].clear()
        account['following'].append({"following":{"id":8,"twitter_handle":"Jane4", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':5})

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "Jane7").get()

        assert query.name == "Jane Smith"
        assert query.following[0].following.twitter_handle == "Jane4"

    def test_find_previous_searchs(self):
        account = controller.insert_account({"id":10,"twitter_handle":"John4", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}})
        connection = controller.generate_following_connection({"following":{"id":6,"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':10})
        
        search = models.Search(search_handle = account)
        search.following.append(connection)
        search.date = account.update_date
        print(search.date)
        search.save()

        query = controller.find_previous_searchs(account.twitter_handle)
        print(query[0].date)
        assert query != None
        
        assert query[0].following[0].following.twitter_handle == "Jane6"

    def test_create_search(self):
        account = controller.insert_account({"id":11,"twitter_handle":"John55", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}, "connections": [{"following":{"twitter_handle":"Jane6", "name" :"Jane Doe", 'group_type':{"name":'Politics', "description": "test"}},'distance':10}]})
        
        controller.create_search(account)

        query = models.Search.objects(search_handle = account).get()

        assert query.search_handle.twitter_handle == account.twitter_handle
    

    def test_top_words(self):
        account = controller.insert_account({"id":20,"twitter_handle":"John21", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}, 
                                            "top_words_positive":[{"word": "test_pos", "value": 11}],
                                            "top_words_negative":[{"word": "test_neg", "value": 20}]
                                            })

        controller.insert_account(account)

        query = models.Account.objects(twitter_handle = "John21").get()

        assert query.top_words_positive[0].value == 11
        assert query.top_words_negative[0].value == 20
        assert query.top_words_negative[0].word == "test_neg"
        assert query.top_words_positive[0].word == "test_pos"

    def test_tweets(self):
        account = controller.insert_account({"id":21,"twitter_handle":"John22", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}, 
                                            "tweets":[{"id":1, "created_at": "Wed Sep 13 08:32:55 +0000 2017", "text": "test"}],
                                            "favorite_tweets":[{"id":1, "created_at": "Wed Sep 13 08:32:55 +0000 2017", "text": "test2"}]
                                            })
        

        query = models.Account.objects(twitter_handle = "John22").get()

        assert query.tweets[0].text == "test"
        assert query.tweets[0].id == 1
        assert query.favorite_tweets[0].text == "test2"
        assert query.favorite_tweets[0].id == 1

    def test_tweets_context(self):
        account = controller.insert_account({"id":22,"twitter_handle":"John22", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}, 
                                            "tweets_context":[{"id":1, "text": "test", "context_annotations": [{"domain":{"id":2, "name":'Politics', "description" :"test"}, "entity":{"id":1, "name":'Politics', "description" :"test"}}]}],
                                            "favorite_context":[{"id":1, "text": "test2", "context_annotations": [{"domain":{"id":2, "name":'Politics', "description" :"test"}, "entity":{"id":1, "name":'Politics', "description" :"test"}}]}]
                                            })
        

        query = models.Account.objects(twitter_handle = "John22").get()

        assert query.tweets_context[0].text == "test"
        assert query.tweets_context[0].id == 1
        assert query.favorite_context[0].text == "test2"
        assert query.favorite_context[0].id == 1
        assert query.favorite_context[0].context_annotations[0].domain.name == "Politics"
        assert query.favorite_context[0].context_annotations[0].domain.id == 2
        assert query.tweets_context[0].context_annotations[0].domain.name == "Politics"
        assert query.tweets_context[0].context_annotations[0].domain.id == 2

    def test_tweets_full(self):
        account = controller.insert_account({"id":22,"twitter_handle":"John22", "name" :"John Doe", 'group_type':{"name":'Politics', "description": "test"}, 
                                            "tweets_context":[{"id":1, "text": "test", "context_annotations": [{"domain":{"id":1, "name":'Politics', "description" :"test"}, "entity":{"id":1, "name":'Politics', "description" :"test"}}]}],
                                            "favorite_context":[{"id":1, "text": "test2", "context_annotations": [{"domain":{"id":1, "name":'Politics', "description" :"test"}, "entity":{"id":1, "name":'Politics', "description" :"test"}}]}],
                                            "tweets":[{"id":1, "created_at": "Wed Sep 13 08:32:55 +0000 2017", "text": "test"}],
                                            "favorite_tweets":[{"id":1, "created_at": "Wed Sep 13 08:32:55 +0000 2017", "text": "test2"}],
                                            "top_words_positive":[{"word": "test_pos", "value": 11}],
                                            "top_words_negative":[{"word": "test_neg", "value": 20}]
                                            })
        

        query = models.Account.objects(twitter_handle = "John22").get()

        assert query.tweets_context[0].text == "test"
        assert query.tweets_context[0].id == 1
        assert query.favorite_context[0].text == "test2"
        assert query.favorite_context[0].id == 1
        assert query.tweets[0].text == "test"
        assert query.tweets[0].id == 1
        assert query.favorite_tweets[0].text == "test2"
        assert query.favorite_tweets[0].id == 1
        assert query.top_words_positive[0].value == 11
        assert query.top_words_negative[0].value == 20
        assert query.top_words_negative[0].word == "test_neg"
        assert query.top_words_positive[0].word == "test_pos"


if __name__ == "__main__":
    unittest.main()