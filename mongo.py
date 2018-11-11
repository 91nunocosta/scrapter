from pymongo import MongoClient


class MissingConfigurationParameter(Exception):

    def __init__(self, parameter):
        super().__init__('{} parameter is missing in the configuration.'.format(parameter))


class ConfiguredMongoMixin:

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB']

    def open_db(self):
        self.__validate_db_config()
        client = MongoClient(
            host=self.db_config['MONGO_HOST'], port=self.db_config['MONGO_PORT'])
        self.database = client[self.db_config['MONGO_DB']]

    def __validate_db_config(self):
        for parameter in ConfiguredMongoMixin.REQUIRED_PARAMETERS:
            if parameter not in self.db_config:
                raise MissingConfigurationParameter(parameter)
