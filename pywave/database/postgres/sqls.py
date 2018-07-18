from pywave.database.base import Database
from sqlalchemy.sql import text

# tables
FINGERPRINTS_TABLENAME = "fingerprints"
SONGS_TABLENAME = "songs"

# fields
FIELD_FINGERPRINTED = "fingerprinted"

# creates
CREATE_FINGERPRINTS_TABLE = """
        CREATE TABLE IF NOT EXISTS `%s` (
             `%s` binary(10) not null,
             `%s` mediumint unsigned not null,
             `%s` int unsigned not null,
         INDEX (%s),
         UNIQUE KEY `unique_constraint` (%s, %s, %s),
         FOREIGN KEY (%s) REFERENCES %s(%s) ON DELETE CASCADE
    ) ENGINE=INNODB;""" % (
    FINGERPRINTS_TABLENAME, Database.FIELD_HASH,
    Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
    Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
    Database.FIELD_SONG_ID, SONGS_TABLENAME, Database.FIELD_SONG_ID
)

CREATE_SONGS_TABLE = """
        CREATE TABLE IF NOT EXISTS `%s` (
            `%s` mediumint unsigned not null auto_increment,
            `%s` varchar(250) not null,
            `%s` tinyint default 0,
            `%s` binary(20) not null,
        PRIMARY KEY (`%s`),
        UNIQUE KEY `%s` (`%s`)
    ) ENGINE=INNODB;""" % (
    SONGS_TABLENAME, Database.FIELD_SONG_ID, Database.FIELD_SONGNAME, FIELD_FINGERPRINTED,
    Database.FIELD_FILE_SHA1,
    Database.FIELD_SONG_ID, Database.FIELD_SONG_ID, Database.FIELD_SONG_ID,
)

# inserts (ignores duplicates)
INSERT_FINGERPRINT = """
        INSERT IGNORE INTO %s (%s, %s, %s) values
            (UNHEX(%%s), %%s, %%s);
    """ % (FINGERPRINTS_TABLENAME, Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET)

INSERT_SONG = "INSERT INTO %s (%s, %s) values (%%s, UNHEX(%%s));" % (
    SONGS_TABLENAME, Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1)

# selects
SELECT = """
        SELECT %s, %s FROM %s WHERE %s = UNHEX(%%s);
    """ % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME, Database.FIELD_HASH)

SELECT_MULTIPLE = """
        SELECT HEX(%s), %s, %s FROM %s WHERE %s IN (%%s);
    """ % (Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET,
           FINGERPRINTS_TABLENAME, Database.FIELD_HASH)

SELECT_ALL = """
        SELECT %s, %s FROM %s;
    """ % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME)

SELECT_SONG = """
        SELECT %s, HEX(%s) as %s FROM %s WHERE %s = %%s;
    """ % (Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1, Database.FIELD_FILE_SHA1, SONGS_TABLENAME, Database.FIELD_SONG_ID)

SELECT_NUM_FINGERPRINTS = """
        SELECT COUNT(*) as n FROM %s
    """ % (FINGERPRINTS_TABLENAME)

SELECT_UNIQUE_SONG_IDS = """
        SELECT COUNT(DISTINCT %s) as n FROM %s WHERE %s = 1;
    """ % (Database.FIELD_SONG_ID, SONGS_TABLENAME, FIELD_FINGERPRINTED)

SELECT_SONGS = text(f"""SELECT {Database.FIELD_SONG_ID}, {Database.FIELD_SONGNAME}, {Database.FIELD_FILE_SHA1} as 
{Database.FIELD_FILE_SHA1} FROM {SONGS_TABLENAME} WHERE {FIELD_FINGERPRINTED} = 1""")

# drops
DROP_FINGERPRINTS = "DROP TABLE IF EXISTS %s;" % FINGERPRINTS_TABLENAME
DROP_SONGS = "DROP TABLE IF EXISTS %s;" % SONGS_TABLENAME

# update
UPDATE_SONG_FINGERPRINTED = """
        UPDATE %s SET %s = 1 WHERE %s = %%s
    """ % (SONGS_TABLENAME, FIELD_FINGERPRINTED, Database.FIELD_SONG_ID)

# delete
DELETE_UNFINGERPRINTED = """
        DELETE FROM %s WHERE %s = 0;
    """ % (SONGS_TABLENAME, FIELD_FINGERPRINTED)