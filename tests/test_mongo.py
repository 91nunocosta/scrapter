from unittest import TestCase

import mongomock

from scrapter import mongo

class TestConfiguredMongoMixin(TestCase):

    @mongomock.patch(servers=(('mongo', 27017),))
    def test_can_open_db(self):
        import scrapter
        scrapter.mongo.MongoClient = mongomock.MongoClient
        db_config = {
            'MONGO_HOST': 'mongo',
            'MONGO_PORT': 27017,
            'MONGO_DB': 'db'
        }
        register = scrapter.mongo.ConfiguredMongoMixin()
        register.db_config = db_config
        register.open_db()
        self.assertIsNotNone(register.database)
        self.assertEqual(register.database.name, 'db')
        self.assertEqual(register.database.client.host, 'mongo')
        self.assertEqual(register.database.client.port, 27017)

    @mongomock.patch(servers=(('mongo', 27017),))
    def test_cant_open_db_with_missing_configs(self):
        import scrapter
        scrapter.mongo.MongoClient = mongomock.MongoClient
        db_config = {
            'MONGO_HOST': 'mongo',
            'MONGO_PORT': 27017,
        }
        register = scrapter.mongo.ConfiguredMongoMixin()
        register.db_config = db_config
        with self.assertRaises(scrapter.mongo.MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_DB' in str(cm.exception))
        db_config = {
            'MONGO_HOST': 'mongo',
            'MONGO_DB': 'db',
        }
        register = scrapter.mongo.ConfiguredMongoMixin()
        register.db_config = db_config
        with self.assertRaises(scrapter.mongo.MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_PORT' in str(cm.exception))
        db_config = {
            'MONGO_PORT': 27017,
            'MONGO_DB': 'db'
        }
        register = scrapter.mongo.ConfiguredMongoMixin()
        register.db_config = db_config
        with self.assertRaises(scrapter.mongo.MissingConfigurationParameter) as cm:
            register.open_db()
        self.assertTrue('MONGO_HOST' in str(cm.exception))
