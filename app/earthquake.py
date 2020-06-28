import asyncio
import datetime
from collections import namedtuple
from datetime import date, timedelta, datetime
from math import floor
from typing import Tuple, List

import aiohttp

__all__ = ['Feature', 'fetch_features', 'all_features']

_BASE_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'

Feature = namedtuple('Feature', [
    'mag', 'place', 'time', 'updated', 'tz', 'url', 'detail', 'felt', 'cdi',
    'mmi', 'alert', 'status', 'tsunami', 'sig', 'net', 'code', 'ids',
    'sources', 'types', 'nst', 'dmin', 'rms', 'gap', 'magType', 'type',
    'title', 'longitude', 'latitude', 'depth'
])


def _date_range_gen(start_date: date, end_date: date,
                    days: int) -> Tuple[date, date]:
    delta = timedelta(days=days)
    n = floor((end_date - start_date) / delta)
    for i in range(n):
        yield start_date + delta * i, start_date + delta * (i + 1)
    yield start_date + delta * n, end_date


def _date_str(dt: datetime.date) -> datetime.date:
    """parse tweet "created_at" timestamp string

    :param dt: date object to parse
    :return: date string formatted as 'yyyy-mm-dd'
    """
    return dt.strftime('%Y-%m-%d')


def _parse_feature(dc: dict):
    return Feature(mag=dc['properties']['mag'],
                   place=dc['properties']['place'],
                   time=datetime.fromtimestamp(dc['properties']['time'] / 1e3),
                   updated=datetime.fromtimestamp(dc['properties']['updated'] /
                                                  1e3),
                   tz=dc['properties']['tz'],
                   url=dc['properties']['url'],
                   detail=dc['properties']['detail'],
                   felt=dc['properties']['felt'],
                   cdi=dc['properties']['cdi'],
                   mmi=dc['properties']['mmi'],
                   alert=dc['properties']['alert'],
                   status=dc['properties']['status'],
                   tsunami=dc['properties']['tsunami'],
                   sig=dc['properties']['sig'],
                   net=dc['properties']['net'],
                   code=dc['properties']['code'],
                   ids=dc['properties']['ids'],
                   sources=dc['properties']['sources'],
                   types=dc['properties']['types'],
                   nst=dc['properties']['nst'],
                   dmin=dc['properties']['dmin'],
                   rms=dc['properties']['rms'],
                   gap=dc['properties']['gap'],
                   magType=dc['properties']['magType'],
                   type=dc['properties']['type'],
                   title=dc['properties']['title'],
                   longitude=dc['geometry']['coordinates'][0],
                   latitude=dc['geometry']['coordinates'][1],
                   depth=dc['geometry']['coordinates'][2])


async def fetch_features(start_date: date, end_date: date) -> List[Feature]:
    start_dt_str = _date_str(start_date)
    end_dt_str = _date_str(end_date)
    url = _BASE_URL + f'&starttime={start_dt_str}&endtime={end_dt_str}'
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            resp.raise_for_status()
            seq = (await resp.json())['features']
    return [_parse_feature(dc) for dc in seq]


async def all_features(start_date: date,
                       end_date: date,
                       days: int = 10) -> List[Feature]:
    seq_range = _date_range_gen(start_date, end_date, days)
    coroutines = [
        fetch_features(start_date, end_date)
        for start_date, end_date in seq_range
    ]
    seq = await asyncio.gather(*coroutines)
    return [i for sub_seq in seq for i in sub_seq]
