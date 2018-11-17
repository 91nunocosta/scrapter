from datetime import datetime, timedelta
from unittest import TestCase

import mongomock
import pymongo
from mongomock import MongoClient, ObjectId

from scrapter.mongo import MissingConfigurationParameter
from scrapter import mongo_updates_register
from scrapter.mongo_updates_register import MongoUpdatesRegister
from scrapter.updates_register import Crawl, CrawlStatus


class TestMongoUpdatesRegister(TestCase):

    @mongomock.patch(servers=(('mongodb', 27017),))
    def setUp(self):
        import scrapter
        scrapter.mongo_updates_register.MongoClient = mongomock.MongoClient
        config = {
            'MONGO_HOST': 'mongodb',
            'MONGO_PORT': 27017,
            'MONGO_DB': 'db'
        }
        self.register = scrapter.mongo_updates_register.MongoUpdatesRegister(config)
        self.register.open_db()

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_open_db(self):
        self.assertIsNotNone(self.register.database)
        self.assertEqual(self.register.database.name, 'db')
        self.assertEqual(self.register.database.client.host, 'mongodb')
        self.assertEqual(self.register.database.client.port, 27017)

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_cant_open_db_with_missing_configs(self):
        import scrapter
        scrapter.mongo.MongoClient = mongomock.MongoClient
        config = {
            'MONGO_HOST': 'mongodb',
            'MONGO_PORT': 27017,
        }
        register = scrapter.mongo_updates_register.MongoUpdatesRegister(config)
        with self.assertRaises(MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_DB' in str(cm.exception))
        config = {
            'MONGO_HOST': 'mongodb',
            'MONGO_DB': 'db',
        }
        register = MongoUpdatesRegister(config)
        with self.assertRaises(MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_PORT' in str(cm.exception))
        config = {
            'MONGO_PORT': 27017,
            'MONGO_DB': 'db'
        }
        register = MongoUpdatesRegister(config)
        with self.assertRaises(MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_HOST' in str(cm.exception))

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_start(self):
        start_date = datetime.now()
        _id = self.register.start('spider1')
        self.assertIsInstance(_id, ObjectId)
        registers = list(self.register.database['updates'].find())
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertListEqual(register['spiders'], ['spider1'])
        self.assertEqual(register['status'], CrawlStatus.STARTED.value)
        self.assertAlmostEqual(
            register['start'], start_date, delta=timedelta(seconds=1))

    def create_update(self):
        start_date = datetime(1, 1, 1)
        _id = self.register.database['updates'].insert_one({
            'spiders': ['spider1'],
            'status': CrawlStatus.STARTED.value,
            'start': start_date
        }).inserted_id
        self.register.database['updates'].insert_one({
            'spiders': ['spider2'],
            'status': CrawlStatus.STARTED.value,
            'start': datetime.now()
        })
        return _id, start_date

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_succeed(self):
        _id, start_date = self.create_update()
        end_date = datetime.now()
        self.register.succeed(_id)
        registers = list(self.register.database['updates'].find({'_id': _id}))
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertListEqual(register['spiders'], ['spider1'])
        self.assertEqual(register['status'], CrawlStatus.SUCCESS.value)
        self.assertAlmostEqual(
            register['start'], start_date, delta=timedelta(seconds=1))
        self.assertAlmostEqual(
            register['end'], end_date, delta=timedelta(seconds=1))

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_fail(self):
        _id, start_date = self.create_update()
        end_date = datetime.now()
        self.register.fail(_id)
        registers = list(self.register.database['updates'].find({'_id': _id}))
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertListEqual(register['spiders'], ['spider1'])
        self.assertEqual(register['status'], CrawlStatus.FAILED.value)
        self.assertAlmostEqual(
            register['start'], start_date, delta=timedelta(seconds=1))
        self.assertAlmostEqual(
            register['end'], end_date, delta=timedelta(seconds=1))

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_get_last(self):
        end_date = datetime(2018, 1, 1, 12)
        updates = [
            {
                'spiders': ['spider1', 'spider4', 'spider5'],
                'status': CrawlStatus.SUCCESS.value,
                'start': datetime(2018, 1, 1, 1),
                'end': end_date
            },
            {
                'spiders': ['spider1', 'spider3', 'spider4'],
                'status': CrawlStatus.SUCCESS.value,
                'start': datetime(2018, 1, 1, 2),
                'end': end_date
            },
            {
                'spiders': ['spider1', 'spider4'],
                'status': CrawlStatus.FAILED.value,
                'start': datetime(2018, 1, 1, 3),
                'end': end_date
            },
            {
                'spiders': ['spider1', 'spider2', 'spider3'],
                'status': CrawlStatus.STARTED.value,
                'start': datetime(2018, 1, 1, 4),
                'end': end_date
            },
            {
                'spiders': ['spider2', 'spider3', 'spider4'],
                'status': CrawlStatus.SUCCESS.value,
                'start': datetime(2018, 1, 1, 5),
                'end': end_date
            }
        ]
        self.register.database['updates'].insert_many(updates)
        last = self.register.last('spider1')
        self.assertListEqual(last.spiders, ['spider1', 'spider3', 'spider4'])
        self.assertEqual(last.status, CrawlStatus.SUCCESS)
        self.assertEqual(last.start, datetime(2018, 1, 1, 2))
        self.assertEqual(last.end, datetime(2018, 1, 1, 12))

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_get_last_without_no_succeed(self):
        last = self.register.last('spider1')
        self.assertIsNone(last)
