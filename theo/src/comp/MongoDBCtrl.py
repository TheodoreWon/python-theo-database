from theo.framework import Component, System
from theo.src.database.MongoDB import MongoDB


class MongoDBCtrl(Component):
    '''
    MongoDBCtrl is just interface Component to use MongoDB.

    If many points make new MongoDB and have connections to Mongo database,
        the database client could make a delay to open the connection
        because of the limitation of connection number.
    To avoid this issue, this component opens a connection and provices interfaces.

    Interfaces:
        Supported interfaces are same with the API of MongoDB.
        MongoDBCtrl is only for the connection control.

    Example:
        from theo.framework import System
        from theo.database import MongoDBCtrl

        System.register_component(MongoDBCtrl)
        System.startup_components()

        print(System.execute_interface('MongoDBCtrl', 'get_databases'))
    '''

    def initial(self):
        self.log.print('info', 'initial')

        self.mongodb = MongoDB()

        System.register_interface('MongoDBCtrl', 'get_databases', [0], self.get_databases)
        System.register_interface('MongoDBCtrl', 'get_collections', [1], self.get_collections)
        System.register_interface('MongoDBCtrl', 'is_database_exist', [1], self.is_database_exist)
        System.register_interface('MongoDBCtrl', 'is_collection_exist', [2], self.is_collection_exist)

        System.register_interface('MongoDBCtrl', 'drop_database', [1], self.drop_database)
        System.register_interface('MongoDBCtrl', 'drop_collection', [2], self.drop_collection)

        System.register_interface('MongoDBCtrl', 'insert', [3, 4], self.insert)
        System.register_interface('MongoDBCtrl', 'select', [2, 3, 4, 5], self.select)
        System.register_interface('MongoDBCtrl', 'keys', [2], self.keys)
        System.register_interface('MongoDBCtrl', 'get_range_filter', [3], self.get_range_filter)

    def get_databases(self):
        return self.mongodb.get_databases()

    def get_collections(self, database):
        return self.mongodb.get_collections(database)

    def is_database_exist(self, database):
        return self.mongodb.is_database_exist(database)

    def is_collection_exist(self, database, collection):
        return self.mongodb.is_collection_exist(database, collection)

    def drop_database(self, database):
        self.mongodb.drop_database(database)

    def drop_collection(self, database, collection):
        self.mongodb.drop_collection(database, collection)

    def insert(self, database, collection, data, unique_key=None):
        self.mongodb.insert(database, collection, data, unique_key)

    def select(self, database, collection, sorting_key=None, keys=None, range_filter=None):
        return self.mongodb.select(database, collection, sorting_key, keys, range_filter)

    def keys(self, database, collection):
        return self.mongodb.keys(database, collection)

    def get_range_filter(self, database, collection, key):
        return self.mongodb.get_range_filter(database, collection, key)
