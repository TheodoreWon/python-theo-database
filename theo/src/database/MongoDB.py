import pymongo


class MongoDB:
    """
    MongoDB supports the functionality to control the Mongo database.

    Methods:
        Mongo() : connecting Mongo database client

        databases = get_databases() : getting databases
        collections = get_collections(database) : getting collections of argument database
        is_exist = is_database_exist(database) : check a existence of argument database
        is_exist = is_collection_exist(database, collection) : check a existence of argument collection

        drop_database(database) : droping argument database
        drop_collection(database, collection) : droping argument collection

        insert(database, collection, list, unique_key=None) : saving argument data in the database
        list = select(database, collection, sorting_key=None, keys=None, range_filter=None) : loading data
            range_filter (dict): key, min(option), max(option)
        keys = keys(database, collection) : getting the keys of the first datum in the database
        range_filter = get_range_filter(database, collection, key) : getting range of the value for argument key

    Example:
        mongodb = MongoDB()
        print(mongodb.get_databases())
    """

    def __init__(self):
        try:
            self.client = pymongo.MongoClient()
            self.client.admin.command('ismaster')
        except Exception as error:
            print(f'error: {error} / MongoDB()')
            self.client = None

    def __del__(self):
        try:
            if self.client:
                self.client.close()
        except Exception as error:
            print(f'error: {error} / del mongodb')

    def get_databases(self):
        try:
            return self.client.database_names()
        except Exception as error:
            print(f'error: {error} / mongodb.get_databases()')
            return list()

    def get_collections(self, database):
        try:
            return self.client[database].collection_names()
        except Exception as error:
            print(f'error: {error} / mongodb.get_collections(database:{database}/{type(database)})')
            return list()

    def is_database_exist(self, database):
        try:
            return True if database in self.client.database_names() else False
        except Exception as error:
            print(f'error: {error} / mongodb.is_database_exist(database:{database}/{type(database)})')
            return False

    def is_collection_exist(self, database, collection):
        try:
            return True if collection in self.client[database].collection_names() else False
        except Exception as error:
            print(f'error: {error} / mongodb.is_collection_exist(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)})')
            return False

    def drop_database(self, database):
        try:
            self.client.drop_database(database)
        except Exception as error:
            print(f'error: {error} / mongodb.drop_database(database:{database}/{type(database)})')

    def drop_collection(self, database, collection):
        try:
            self.client[database].drop_collection(collection)
        except Exception as error:
            print(f'error: {error} / mongodb.drop_collection(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)})')

    def insert(self, database, collection, data, unique_key=None):
        try:
            if collection not in self.client[database].collection_names() and unique_key:
                self.client[database][collection].create_index([(unique_key, pymongo.ASCENDING)], unique=True)

            if collection in self.client[database].collection_names() and unique_key:
                for element in data:
                    self.client[database][collection].find_one_and_update(
                        {unique_key: element[unique_key]}, {'$set': element}, upsert=True)
            else:
                self.client[database][collection].insert_many(data)
        except Exception as error:
            print(f'error: {error} / mongodb.insert(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)},')
            print(f'                                   unique_key:{unique_key}/{type(unique_key)},',
                  f'data:{data}/{type(data)}')

    def select(self, database, collection, sorting_key=None, keys=None, range_filter=None):
        try:
            if collection not in self.client[database].collection_names():
                return list()

            find_filter = dict()
            if range_filter and 'min' in range_filter:
                find_filter['$gte'] = range_filter['min']
            if range_filter and 'max' in range_filter:
                find_filter['$lte'] = range_filter['max']

            return list(self.client[database][collection].find(
                        sort=[(sorting_key, pymongo.ASCENDING)] if sorting_key else None,
                        projection=self.get_projection(keys),
                        filter={range_filter['key']: find_filter} if range_filter else None))
        except Exception as error:
            print(f'error: {error} / mongodb.select(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)},')
            print(f'                                sorting_key:{sorting_key}/{type(sorting_key)},',
                  f'keys:{keys}/{type(keys)}')
            return None

    def keys(self, database, collection):
        try:
            return None if collection not in self.client[database].collection_names() \
                else list(self.client[database][collection].find_one(projection=self.get_projection()).keys())
        except Exception as error:
            print(f'error: {error} / mongodb.keys(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)})')
            return None

    def get_range_filter(self, database, collection, key):
        try:
            if collection not in self.client[database].collection_names():
                return None

            start = self.client[database][collection].find_one(
                projection=self.get_projection([key]), sort=[(key, pymongo.ASCENDING)])
            end = self.client[database][collection].find_one(
                projection=self.get_projection([key]), sort=[(key, pymongo.DESCENDING)])

            if not start or not end or key not in start or key not in end:
                return None

            return {'key': key, 'min': start[key], 'max': end[key]}
        except Exception as error:
            print(f'error: {error} / mongodb.range_filter(database:{database}/{type(database)},',
                  f'collection:{collection}/{type(collection)}, key:{key}/{type(key)})')
            return None

    @staticmethod
    def get_projection(keys=None):
        try:
            projection = {'_id': False}

            if keys:
                for key in keys:
                    projection[key] = True

            return projection
        except Exception as error:
            print(f'error: {error} / MongoDB.get_projection(keys:{keys}/{type(keys)})')
