import pymongo


class MongoDB:
    """
    MongoDB supports the functionality to control the Mongo database.

    Methods:
        Mongo(check_connection=False) : connecting Mongo database client

        databases = get_databases() : getting databases
        collections = get_collections(database) : getting collections of argument database
        is_exist = is_database_exist(database) : check a existence of argument database
        is_exist = is_collection_exist(database, collection) : check a existence of argument collection

        drop_database(database) : droping argument database
        drop_collection(database, collection) : droping argument collection

        save_data(database, collection, data, unique_key=None) : saving argument data in the database
        data = load_data(database, collection, sorting_key=None, keys=None, range=None) : loading data from the database
        keys = get_keys(database, collection) : getting the keys of the first datum in the database
        range = get_range(database, collection, key) : getting range of the value for argument key

    Arguments:
        range (range dictionary): key, min(option), max(option)

    Example:
        mongodb = MongoDB(check_connection=True)
        print(mongodb.get_databases())
    """

    def __init__(self, check_connection=False):
        if not isinstance(check_connection, bool):
            raise AssertionError(
                '[theo.framework.MongoDB] error: check_connection(type:{}) should be bool.'.format(
                    type(check_connection)))

        self.client = pymongo.MongoClient()

        if check_connection:
            try:
                self.client.admin.command('ismaster')
            except pymongo.errors.ServerSelectionTimeoutError:
                self.client = None
                raise AssertionError('[theo.database.MongoDB] The client is not ready.')

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def get_databases(self):
        return list(self.client.database_names())

    def get_collections(self, database):
        return list(self.client[database].collection_names())

    def is_database_exist(self, database):
        return True if database in self.client.database_names() else False

    def is_collection_exist(self, database, collection):
        self.validate_mongodb(database, collection)

        return True if collection in self.client[database].collection_names() else False

    def drop_database(self, database):
        self.client.drop_database(database)

    def drop_collection(self, database, collection):
        self.validate_mongodb(database, collection)

        self.client[database].drop_collection(collection)

    def save_data(self, database, collection, data, unique_key=None):
        self.validate_mongodb(database, collection)

        if self.is_collection_exist(database, collection):
            if unique_key is None:
                try:
                    self.client[database][collection].insert_many(data)
                except pymongo.errors.BulkWriteError:
                    raise AssertionError(
                        '[theo.framework.MongoDB] error: Fail to save data, because of the duplication.')

            else:
                for datum in data:
                    self.client[database][collection].find_one_and_update(
                        {unique_key: datum[unique_key]}, {'$set': datum}, upsert=True)
        else:
            if unique_key is not None:
                self.client[database][collection].create_index([(unique_key, pymongo.ASCENDING)], unique=True)

            try:
                self.client[database][collection].insert_many(data)
            except pymongo.errors.BulkWriteError:
                raise AssertionError('[theo.framework.MongoDB] error: Fail to save data, because of the duplication.')

    def load_data(self, database, collection, sorting_key=None, keys=None, range=None):
        self.validate_mongodb(database, collection)
        self.validate_range(range)

        if not self.is_collection_exist(database, collection):
            return list()

        range_condition = dict()

        if range is not None:
            if 'min' in range:
                range_condition['$gte'] = range.get('min')

            if 'max' in range:
                range_condition['$lte'] = range.get('max')

        cursor = self.client[database][collection].find(
            sort=None if sorting_key is None else [(sorting_key, pymongo.ASCENDING)],
            projection=self.get_projection(keys),
            filter=None if range is None else {range.get('key'): range_condition})

        return list(cursor)

    def get_keys(self, database, collection):
        self.validate_mongodb(database, collection)

        return list() if not self.is_collection_exist(database, collection) \
            else list(self.client[database][collection].find_one(projection=self.get_projection()).keys())

    def get_range(self, database, collection, key):
        self.validate_mongodb(database, collection)

        if not self.is_collection_exist(database, collection):
            return None

        start = self.client[database][collection].find_one(
            projection=self.get_projection([key]), sort=[(key, pymongo.ASCENDING)])
        end = self.client[database][collection].find_one(
            projection=self.get_projection([key]), sort=[(key, pymongo.DESCENDING)])

        if start is None or end is None or key not in start or key not in end:
            return None

        return {'key': key, 'start': start[key], 'end': end[key]}

    @staticmethod
    def get_projection(keys=None):
        projection = {'_id': False}

        if keys is None:
            keys = {}

        for key in keys:
            projection[key] = True

        return projection

    """
    Internal validation functions
    """
    @staticmethod
    def validate_mongodb(database, collection):
        if not isinstance(database, str):
            raise AssertionError(
                '[theo.database.MongoDB] error: database(type:{}) should be str.'.format(type(database)))

        if not isinstance(collection, str):
            raise AssertionError(
                '[theo.database.MongoDB] error: collection(type:{}) should be str.'.format(type(collection)))

    @staticmethod
    def validate_range(range):
        if range is not None:
            if not isinstance(range, dict):
                raise AssertionError(
                    '[theo.database.MongoDB] error: range(type:{}) should be dict.'.format(type(range)))

            if not ('key' in range and ('min' in range or 'max' in range)):
                raise AssertionError(
                    '[theo.database.MongoDB] error: range(keys:{}) does not have key or min, max.'.format(
                        list(filter.keys())))
