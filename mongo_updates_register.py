from .updates_register import UpdatesRegister
from mongomock import MongoClient


class MissingConfigurationParameter(Exception):

    def __init__(self, parameter):
        super().__init__('{} parameter is missing in the configuration.'.format(parameter))


class MongoUpdatesRegister:

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB']

    def __init__(self, db_config):
        self.db_config = db_config
        self.database = None

    def open_db(self):
        self.__validate_db_config()
        client = MongoClient(
            host=self.db_config['MONGO_HOST'], port=self.db_config['MONGO_PORT'])
        self.database = client[self.db_config['MONGO_DB']]

    def __validate_db_config(self):
        for parameter in MongoUpdatesRegister.REQUIRED_PARAMETERS:
            if parameter not in self.db_config:
                raise MissingConfigurationParameter(parameter)

    def close_db(self):
        pass

    def start(self, spider):
        pass

    def fail(self, spider):
        pass

    def succeed(self, spider):
        pass

    def last(self, spider):
        pass
