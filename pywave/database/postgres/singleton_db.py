import sqlalchemy
from itertools import zip_longest
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm import sessionmaker
from pywave.database.base import Database
from pywave.database.postgres import sqls, mapping


class PgDbSingleton(Database):

    instance = None

    def __init__(self, *options):
        super().__init__()
        self.database = self.instance.connect(*options)[0]
        self.session = sessionmaker(bind=self.database)()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(PgDbSingleton, cls).__new__(cls)
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
        data = self.database.execute(sqls.SELECT_SONGS)
        if data:
            return data.fetchall()

    def get_song_by_id(self, sid):
        pass

    def insert(self, hash, sid, offset):
        pass

    def insert_song(self, song_name, file_hash):

        song_table = mapping.Songs(song_name=song_name, file_sha1=file_hash.encode())
        self.session.add(song_table)
        asd = self.session.commit()
        return asd

        # insert_song_query = f"""INSERT INTO {sqls.SONGS_TABLENAME} (song_name, file_sha1) values ('{song_name}', '{file_hash}');"""
        # cur = self.database.execute(sqlalchemy.text(insert_song_query))
        # return cur.lastrowid

    def query(self, hash):
        pass

    def get_iterable_kv_pairs(self):
        pass

    def insert_hashes(self, sid, hashes):
        values = []
        for hash, offset in hashes:
            values.append((hash, sid, offset))

        for split_values in grouper(values, 1000):
            for item in list(split_values):
                a_hash = item[0].encode()
                a_songid = item[1]
                a_offset = item[2]
                fingerprint_data = mapping.Fingerprints(hash=a_hash, song_id=int(a_songid), offset=int(a_offset))
                try:
                    self.session.add(fingerprint_data)
                    self.session.commit()
                except ProgrammingError as e:
                    print(e)
                    continue
                except IntegrityError as e:
                    print(e)
                    continue
        print('Done inserting hashes')

    def return_matches(self, hashes):
        pass


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in zip_longest(fillvalue=fillvalue, *args))