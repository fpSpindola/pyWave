from sqlalchemy import Table, Column, Integer, String, Binary, ForeignKey, SmallInteger, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA

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

    hash = Column(Binary(20), primary_key=True, nullable=False, index=True, unique=True)
    song_id = Column(Integer, nullable=False, unique=True)
    offset = Column(Integer, nullable=False, unique=True)