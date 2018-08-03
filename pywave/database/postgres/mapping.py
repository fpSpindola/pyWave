from sqlalchemy import Table, Column, Integer, String, Binary, ForeignKey, SmallInteger, MetaData, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()


class Songs(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    song_name = Column(String(250), nullable=False)
    fingerprinted = Column(SmallInteger, nullable=True)
    file_sha1 = Column(Binary(20), nullable=False)


class Fingerprints(Base):
    __tablename__ = 'fingerprints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(Binary(10), nullable=False, index=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    offset = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('hash', 'song_id', 'offset', name='uix_1'), )