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
    MARGIN = timedelta(seconds=5)

    def __get_db(self):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.database = client[MONGO_DB]

    def setUp(self):
        self.start_directory = os.getcwd()
        os.chdir(PROJECT_DIR)
        self.__get_db()
        self.items = self.database['items']
        self.updates = self.database['updates']
        self.items.drop()
        self.updates.drop()

    def tearDown(self):
        os.chdir(self.start_directory)

    def __create_previous_update(self):
        self.updates.insert_one({
            'spiders': [['example', 'example2']],
            'status': 'success',
            'start': self.LAST_START,
            'end': self.LAST_END
        })
        self.items.insert_one({
            'name': 'old_item',
            'index': 1
        })
        self.items.insert_one({
            'name': 'updated_item',
            'index': 1
        })
        self.items.insert_one({
            'name': 'updated_item',
            'index': 2
        })

    def test_step(self):
        self.__create_previous_update()
        started = datetime.now()
        execute()
        ended = datetime.now()
        items = self.items.find()
        self.assertEqual(items.count(), 4)
        old_item = self.items.find({'name': 'old_item'})[0]
        updated_item = self.items.find({'name': 'updated_item', 'index': 1})[0]
        non_updated_item = self.items.find({'name': 'updated_item', 'index': 2})[0]
        new_item = self.items.find({'name': 'new_item'})[0]
        self.assertNotIn('_updated', old_item)
        self.assertEqual(updated_item['last'], self.LAST_START)
        self.assertAlmostEqual(updated_item['_updated'], started, delta=self.MARGIN)
        self.assertNotIn('_updated', non_updated_item)
        self.assertAlmostEqual(new_item['_updated'], started, delta=self.MARGIN)
        updates = self.updates.find().sort('start', pymongo.DESCENDING)
        self.assertEqual(updates.count(), 2)
        last_update = updates[0]
        self.assertEqual(last_update['spiders'], [['example', 'example2']])
        self.assertAlmostEqual(last_update['start'], started, delta=self.MARGIN)
        self.assertAlmostEqual(last_update['end'], ended, delta=self.MARGIN)
        self.assertEqual(last_update['status'], 'success')
