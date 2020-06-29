import asyncio
import shutil
from datetime import date

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

    def save_to_db(self, start_date: date, end_date: date):
        features = asyncio.run(all_features(start_date, end_date))
        self.dao.bulk_save_events(features)
