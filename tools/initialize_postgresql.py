from pywave.database.postgres.singleton_db import PgDbSingleton

singletonInstance = PgDbSingleton(PgDbSingleton)

connection = singletonInstance.connect('root', 'Epilif23', 'pywave', 'localhost')






