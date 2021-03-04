import unittest
from mongoengine import connect, disconnect
import server.db_controller as controller


''' Verifies proper usage of db controller '''

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    
    def test_insert_account(self):
        controller.insert_account()

        actual = Account.objects().first()
        assert actual.twitter_handle == "John21"
        assert actual.name == "John Doe"