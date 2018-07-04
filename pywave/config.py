from pywave.database.postgres.singleton_db import PgDbSingleton
from pywave.database.base import get_database, Database


class Config:

    current = None

    def __init__(self, configs: dict):
        if configs['pywave'].get("db_type") == 'postgres':
            self.db = PgDbSingleton().connect(configs['pywave']['database']['user'],
                                              configs['pywave']['database']['password'],
                                              configs['pywave']['database']['db'],
                                              configs['pywave']['database']['host'],
                                              configs['pywave']['database']['port'])
        else:
            self.db = get_database(**configs.get('database'))
            self.db.setup()
