import asyncio
from functools import wraps
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.earthquake import all_features
from app.models.base import Base
from app.models.tables import Events
from config import Config

__all__ = ['Dao']


def session_factory(echo: bool):
    engine = create_engine('sqlite:///{0}'.format(Config.APP_DB), echo=echo)
    _SessionFactory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return _SessionFactory()


def _commit(fn):
    @wraps(fn)
    def helper(*args, **kwargs):
        res = fn(*args, **kwargs)
        args[0].session.commit()
        return res

    return helper


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Dao(metaclass=SingletonMeta):
    __slots__ = ['session']

    def __init__(self, echo=False):
        self.session = session_factory(echo)

    @_commit
    def reset_db(self) -> None:
        self.session.query(Events).delete()

    @_commit
    def bulk_save(self, objects: Iterable) -> None:
        """Perform a bulk save of the given sequence of objects

        :param objects: a sequence of mapped object instances
        :return:
        """
        self.session.bulk_save_objects(objects)

    def bulk_save_events(self, start_date, end_date):
        features = asyncio.run(all_features(start_date, end_date))
        self.bulk_save((Events(*i) for i in features))

    def count_events(self):
        return self.session.query(Events.id).count()
