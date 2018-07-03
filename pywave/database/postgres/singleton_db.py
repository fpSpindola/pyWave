import sqlalchemy


class PgDbSingleton:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance

    def connect(self, user, password, db, host='localhost', port=5432):
        """
        :param user:
        :param password:
        :param db:
        :param host:
        :param port:
        :return:
        """
        url = f'postgresql+psycopg2://{user}:{password}@{host}{port}/{db}'

        conn = sqlalchemy.create_engine(url, client_encoding='utf8')

        meta = sqlalchemy.MetaData(bind=conn, reflect=True)

        return conn, meta