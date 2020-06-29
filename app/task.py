import asyncio
import csv
import shutil
from datetime import datetime

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from app.earthquake import all_features
from app.models.dao import Dao
from config import Config

__all__ = ['Task']


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Task(metaclass=SingletonMeta):
    __slots__ = ['dao']

    def __init__(self):
        self.dao = Dao()

    def reset(self):
        shutil.rmtree(Config.APP_DB, ignore_errors=True)
        self.dao.reset_db()

    def save_to_db(self, start_date: str, end_date: str):
        dt_start = datetime.strptime(start_date, '%Y-%m-%d')
        dt_end = datetime.strptime(end_date, '%Y-%m-%d')
        features = asyncio.run(all_features(dt_start, dt_end))
        self.dao.bulk_save_events(features)

    @staticmethod
    def backup_db():
        shutil.rmtree(Config.BAK_DB, ignore_errors=True)
        shutil.copyfile(Config.APP_DB, Config.BAK_DB)

    def export_top_earthquakes(self):
        shutil.rmtree(Config.TOP_EQ, ignore_errors=True)
        records = self.dao.top_earthquakes(10)
        with open(Config.TOP_EQ, 'w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(records[0].keys())
            csv_writer.writerows(records)

    def plot_count_by_mag(self):
        shutil.rmtree(Config.PLOT_COUNT, ignore_errors=True)
        df = pd.DataFrame(self.dao.count_by_period())

        pp = PdfPages(Config.PLOT_COUNT)

        def helper(m: int):
            upper = str(m + 1) if m < 6 else 'inf'
            df_ = df.pipe(lambda d: d[d['magnitude'] == m]).groupby(
                'hour', as_index=False).agg({'counts': 'sum'})
            return df_.plot.bar(
                x='hour', rot=0,
                title=f'magnitude between {m} and {upper}').figure

        [pp.savefig(helper(i), dpi=300, transparent=True) for i in range(7)]
        pp.close()
