import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # path
    DB_DIR = ''.join([basedir, '/db'])
    APP_DB = ''.join([DB_DIR, '/app.db'])
    BAK_DB = ''.join([DB_DIR, '/app.db.bak'])
    TOP_EQ = ''.join([DB_DIR, '/top_earthquakes.csv'])
    PLOT_COUNT = ''.join([DB_DIR, '/count_plot.pdf'])
