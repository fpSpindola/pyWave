import sqlalchemy

from pywave.database.base import Database


class PgDbSingleton(Database):

    instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(PgDbSingleton, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def connect(self, user, password, db, host='localhost', port=5432):
        """
        :param user:
        :param password:
        :param db:
        :param host:
        :param port:
        :return:
        """
        url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'

        conn = sqlalchemy.create_engine(url, client_encoding='utf8')

        meta = sqlalchemy.MetaData(bind=conn, reflect=True)

        return conn, meta

    def empty(self):
        pass

    def delete_unfingerprinted_songs(self):
        pass

    def get_num_songs(self):
        pass

    def get_num_fingerprints(self):
        pass

    def set_song_fingerprinted(self, sid):
        pass

    def get_songs(self):
        pass

    def get_song_by_id(self, sid):
        pass

    def insert(self, hash, sid, offset):
        pass

    def insert_song(self, song_name):
        pass

    def query(self, hash):
        pass

    def get_iterable_kv_pairs(self):
        pass

    def insert_hashes(self, sid, hashes):
        pass

    def return_matches(self, hashes):
        pass