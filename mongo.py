from pymongo import MongoClient


class MissingConfigurationParameter(Exception):

    def __init__(self, parameter):
        super().__init__('{} parameter is missing in the configuration.'.format(parameter))


class ConfiguredMongoMixin:

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB']

    def open_db(self):
        self.__validate_config()
        client = MongoClient(
            host=self.config['MONGO_HOST'], port=self.config['MONGO_PORT'])
        self.database = client[self.config['MONGO_DB']]

    def __validate_config(self):
        for parameter in ConfiguredMongoMixin.REQUIRED_PARAMETERS:
            if parameter not in self.config:
                raise MissingConfigurationParameter(parameter)
