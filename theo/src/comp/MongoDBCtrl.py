from theo.framework import Component, System
from theo.src.database.MongoDB import MongoDB


class MongoDBCtrl(Component):
    def initial(self):
        self.log.print('info', 'initial (related:{})'.format(self.related_components))

        self.db_handler = MongoDB()

        System.register_interface('MongoDBCtrl', 'get_databases', [0], self.get_databases)
        System.register_interface('MongoDBCtrl', 'get_collections', [1], self.get_collections)
        System.register_interface('MongoDBCtrl', 'is_database_exist', [1], self.is_database_exist)
        System.register_interface('MongoDBCtrl', 'is_collection_exist', [2], self.is_collection_exist)

        System.register_interface('MongoDBCtrl', 'drop_database', [1], self.drop_database)
        System.register_interface('MongoDBCtrl', 'drop_collection', [2], self.drop_collection)

        System.register_interface('MongoDBCtrl', 'save_data', [3, 4], self.save_data)
        System.register_interface('MongoDBCtrl', 'load_data', [2, 3, 4, 5], self.load_data)
        System.register_interface('MongoDBCtrl', 'get_keys', [2], self.get_keys)
        System.register_interface('MongoDBCtrl', 'get_range', [3], self.get_range)

    def get_databases(self):
        return self.db_handler.get_databases()

    def get_collections(self, database):
        return self.db_handler.get_collections(database)

    def is_database_exist(self, database):
        return self.db_handler.is_database_exist(database)

    def is_collection_exist(self, database, collection):
        return self.db_handler.is_collection_exist(database, collection)

    def drop_database(self, database):
        self.db_handler.drop_database(database)

    def drop_collection(self, database, collection):
        self.db_handler.drop_collection(database, collection)

    def save_data(self, database, collection, data, unique_key=None):
        self.db_handler.save_data(database, collection, data, unique_key)

    def load_data(self, database, collection, sorting_key=None, keys=None, range=None):
        return self.db_handler.load_data(database, collection, sorting_key, keys, range)

    def get_keys(self, database, collection):
        return self.db_handler.get_keys(database, collection)

    def get_range(self, database, collection, key):
        return self.db_handler.get_range(database, collection, key)
