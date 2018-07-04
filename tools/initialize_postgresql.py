from pywave.database.postgres.singleton_db import PgDbSingleton
from pywave.database.postgres.mapping import Base

connection, meta = PgDbSingleton().connect('postgres', 'Epilif23', 'pywave', 'localhost')

Base.metadata.create_all(connection)




