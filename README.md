# theo-database

It is the database to control databases easy.

MongoDB is consist of methods what control MongoDB.

I am likely waiting a any kind of contribution.


# Theo series

Framework : pip install theo-framework, https://github.com/TheodoreWon/python-theo-framework  
Database : pip install theo-database, https://github.com/TheodoreWon/python-theo-database  
Message : pip install theo-message, https://github.com/TheodoreWon/python-theo-message  
Internet : pip install theo-message, https://github.com/TheodoreWon/python-theo-internet  
Trade : pip install theo-trade, https://github.com/TheodoreWon/python-theo-trade


# How to use

Install the framework  
> pip install theo-database

Print docstrings  
> from theo.database import MongoDB, MongoDBCtrl  
> print(MongoDB.&#95;&#95;doc&#95;&#95;)  
> print(MongoDBCtrl.&#95;&#95;doc&#95;&#95;)

Simple example
> ''' import theo-database, MongoDB '''  
> from theo.database import MongoDB  
> mongodb = MongoDB(check_connection=True)  

> ''' print databases '''  
> databases = mongodb.get_databases()  
> print('databases:{}'.format(databases))  
>> databases:['Athena', 'admin', 'config', 'local']  

> ''' print collections '''  
> for database in databases:  
>     collections = mongodb.get_collections(database)  
>     print('database({}) collections:{}'.format(database, collections))  
>> database(admin) collections:['system.version']  
>> database(config) collections:['system.sessions']  
>> database(local) collections:['startup_log']  

> ''' print existence '''  
> print('theo-database/example exist:{}'.format(mongodb.is_database_exist('theo-database')))  
> print('theo-database/example exist:{}'.format(mongodb.is_collection_exist('theo-database', 'example')))  
>> theo-database/example exist:False  
>> theo-database/example exist:False  

> ''' save and load data '''  
> mongodb.save_data('theo-database', 'example', [{'text': 'Hello, theo-database.'}, {'text': 'Thank you for using.'}])  
> print('theo-database/example exist:{}'.format(mongodb.is_database_exist('theo-database')))  
> print('theo-database/example exist:{}'.format(mongodb.is_collection_exist('theo-database', 'example')))  
> print(mongodb.load_data('theo-database', 'example'))  
>> theo-database/example exist:True  
>> theo-database/example exist:True  
>> [{'text': 'Hello, theo-database.'}, {'text': 'Thank you for using.'}]  

> ''' drop collection '''  
> mongodb.drop_collection('theo-database', 'example')  
> print('theo-database/example exist:{}'.format(mongodb.is_database_exist('theo-database')))  
> print('theo-database/example exist:{}'.format(mongodb.is_collection_exist('theo-database', 'example')))  
>> theo-database/example exist:False  
>> theo-database/example exist:False  


# How to setup the MongoDB

Step 1. Download  
> Open the website, https://www.mongodb.com/  
> Find and click the 'Get MongoDB' button from top of the page  
> Select 'Server' of the list Cloud, Server, Tools  
> Check the environment, Version, OS, Package and click the 'Download' button  

Step 2. Install  
> Execute the installer what is downloaded  
> Follow the install steps and un-check 'Install MongoDB Compass'  

Step 3. Set the MongoDB as the service in Windows  
> Make new folder like C:\Users\wonta\mongodb  
> Run cmd (command prompt) as Administrator  
> Go to the MongoDB location like C:\Program Files\MongoDB\Server\4.0\bin  
> Enter the command 'mongod --remove'  
> Enter the command 'mongod --dbpath=C:\Users\wonta\mongodb --logpath=C:\Users\wonta\mongodb\log.txt --install'  
> Restart the windows


# Authors

Theodore Won - Owner of this project


# License

This project is licensed under the MIT License - see the LICENSE file for details


# Versioning

Basically, this project follows the 'Semantic Versioning'. (https://semver.org/)  
But, to notify new feature, I added several simple rules at the Semantic Versioning.  
I would like to call 'Theo Versioning'.

- Version format is MAJOR.MINOR.PATCH  
- MAJOR version is increased when API is changed or when new feature is provided.  
  - New feature does not affect a interface.  
  - But, to notify new feature, New feature makes MAJOR version up.  
  - Before official version release (1.0.0), MAJOR is kept 0 and MINOR version is used.  
- MINOR version is up when the API is added. (New functionality)  
- PATCH version is lifted when bug is fixed, test code is uploaded, comment or document or log is updated.  
