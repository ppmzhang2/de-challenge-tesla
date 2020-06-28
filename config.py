import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # path
    DB_DIR = ''.join([basedir, '/db'])
    APP_DB = ''.join([DB_DIR, '/app.db'])
    BAK_DB = ''.join([DB_DIR, '/app.db.bak'])
