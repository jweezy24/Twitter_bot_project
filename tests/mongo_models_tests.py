import unittest
from mongoengine import connect, disconnect
from server.models import *


''' Verifies proper usage of models '''

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    
    def testAccount(self):
        user =  Account(twitter_handle= "John21")
        user.name = "John Doe"
        user.save()

        actual = Account.objects().first()
        assert actual.twitter_handle == "John21"
        assert actual.name == "John Doe"