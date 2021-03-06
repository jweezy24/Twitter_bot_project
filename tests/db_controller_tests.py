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
    
    
    def test_insert_account(self):
        controller.insert_account({"twitter_handle":"John21", "name" :"John Doe"})

        actual = models.Account.objects().first()
        assert actual.twitter_handle == "John21"
        assert actual.name == "John Doe"