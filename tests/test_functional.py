import os
import subprocess
from datetime import datetime, timedelta
from importlib import reload
from os.path import abspath, dirname, join
from unittest import TestCase
import pymongo

import twisted
from mongomock.helpers import DESCENDING
from pymongo import MongoClient
from twisted.internet import reactor

from scrapter.run import execute

TEST_DIR = abspath(dirname(__file__))
PROJECT_DIR = join(join(TEST_DIR, 'project'), 'project')

MONGO_HOST="localhost"
MONGO_PORT=27017
MONGO_DB="items"

class TestScrapter(TestCase):

    LAST_START = datetime(2018,1,1,0, 0, 0)
    LAST_END = datetime(2018,1,1,0, 0, 0)

    def __get_db(self):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.database = client[MONGO_DB]

    def setUp(self):
        self.start_directory = os.getcwd()
        os.chdir(PROJECT_DIR)
        self.__get_db()
        self.database['items'].drop()
        self.database['updates'].drop()

    def tearDown(self):
        os.chdir(self.start_directory)

    def __create_previous_update(self):
        self.database['updates'].insert_one({
            'spiders': [['example']],
            'status': 'success',
            'start': self.LAST_START,
            'end': self.LAST_END
        })
        self.database['items'].insert_one({
            'name': 'item1',
            'category': 'updated'
        })
        self.database['items'].insert_one({
            'name': 'item2',
            'category': 'non_updated'
        })

    def test_step(self):
        self.__create_previous_update()
        started = datetime.now()
        execute()
        ended = datetime.now()
        items = self.database['items'].find()
        self.assertEqual(items.count(), 3)
        updated_items = self.database['items'].find({'category': 'updated'})
        self.assertEqual(updated_items.count(), 1)
        updated_item = updated_items[0]
        self.assertEqual(updated_item['last'], self.LAST_START)
        self.assertAlmostEqual(updated_item['_updated'], started, delta=timedelta(seconds=1))
        updates = self.database['updates'].find().sort('start', pymongo.DESCENDING)
        self.assertEqual(updates.count(), 2)
        last_update = updates[0]
        self.assertEqual(last_update['spiders'], [['example']])
        self.assertAlmostEqual(last_update['start'], started, delta=timedelta(seconds=1))
        self.assertAlmostEqual(last_update['end'], ended, delta=timedelta(seconds=1))
        self.assertEqual(last_update['status'], 'success')
