from sqlalchemy import Table, Column, Integer, String, Binary, ForeignKey, SmallInteger, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()


class Songs(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    song_name = Column(String(250), nullable=False)
    fingerprinted = Column(SmallInteger, nullable=False)
    file_sha1 = Column(Binary(20), nullable=False)


class Fingerprints(Base):
    __tablename__ = 'fingerprints'

    hash = Column(Binary(10), primary_key=True, nullable=False, index=True, unique=True)
    song_id = Column(Integer, ForeignKey("songs.song_id"), nullable=False, unique=True)
    offset = Column(Integer, nullable=False, unique=True)