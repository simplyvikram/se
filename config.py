db_username = 'vik_wv_hq_1'
db_password = 'vik_wv_hq_1'
database_name = 'vik_wv_hq_db_1'

class Config(object):
    pass

class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = '!!!!CHANGE ME!!!'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    DATABASE_URI = \
        'postgresql+psycopg2://%s:%s@localhost:5432/%s' % \
        (db_username, db_password, database_name)