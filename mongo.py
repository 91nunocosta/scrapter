from pymongo import MongoClient

class MissingConfigurationParameter(Exception):

    def __init__(self, parameter):
        super().__init__('{} parameter is missing in the configuration.'.format(parameter))

class ConfiguredMongoMixin:

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB']

    def open_db(self, config):
        self.__validate_db_config(config)
        client = MongoClient(
            host=config['MONGO_HOST'], port=config['MONGO_PORT'])
        self.database = client[config['MONGO_DB']]

    def __validate_db_config(self, config):
        for parameter in ConfiguredMongoMixin.REQUIRED_PARAMETERS:
            if parameter not in config:
                raise MissingConfigurationParameter(parameter)
