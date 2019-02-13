import os
from os.path import join, abspath, dirname
from unittest import TestCase
from scrapter.run import execute

from pymongo import MongoClient

TEST_DIR = abspath(dirname(__file__))
PROJECT_DIR = join(join(TEST_DIR, 'project'), 'project')

MONGO_HOST="localhost"
MONGO_PORT=27017
MONGO_DB="items"

class TestScrapter(TestCase):

    def __get_db(self):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.database = client[MONGO_DB]

    def test(self):
        start_directory = os.getcwd()
        os.chdir(PROJECT_DIR)
        execute()
        os.chdir(start_directory)
        self.__get_db()
        print(self.database['items'].find({}))