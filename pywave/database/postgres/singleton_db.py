import sqlalchemy
from itertools import zip_longest

from sqlalchemy import update
from sqlalchemy.exc import ProgrammingError, IntegrityError
from pywave.database.postgres.mapping import Songs, Fingerprints
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from pywave.database.base import Database
from pywave.database.postgres import sqls



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
        song_fingerprinted = update(Songs).where(Songs.song_id==sid).values(fingerprinted=1)
        self.session.execute(song_fingerprinted)
        self.session.commit()

    def get_songs(self):

        songs = self.session.query(Songs).filter(Songs.fingerprinted==1).all()
        return songs

    def get_song_by_id(self, sid):
        song = self.session.query(Songs).filter(Songs.song_id == sid).scalar()
        return song if song else None

    def insert(self, hash, sid, offset):
        pass

    def insert_song(self, song_name, file_hash):

        song = Songs(song_name=song_name, file_sha1=file_hash.encode())
        self.session.add(song)
        self.session.commit()
        return song.song_id

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
                a_hash = item[0]
                a_songid = item[1]
                a_offset = item[2]
                fingerprint = Fingerprints(hash=a_hash, song_id=int(a_songid), offset=int(a_offset))
                try:
                    self.session.add(fingerprint)
                except ProgrammingError as e:
                    print(e)
                    continue
                except IntegrityError as e:
                    print(e)
                    continue
        self.session.commit()
        print('Done inserting hashes')

    def return_matches(self, hashes):
        """
        Return the (song_id, offset_diff) tuples associated with
        a list of (sha1, sample_offset) values.
        """
        # Create a dictionary of hash => offset pairs for later lookups
        mapper = {}
        for hash, offset in hashes:
            mapper[hash] = offset

        # Get an iteratable of all the hashes we need
        values = mapper.keys()
        for split_values in grouper(values, 1000):
            split_values = list(split_values)
            result = self.session.query(Fingerprints).filter(Fingerprints.hash.in_(split_values)).all()
            for each in result:
                yield (each.song_id, each.offset - mapper[each.hash])


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in zip_longest(fillvalue=fillvalue, *args))