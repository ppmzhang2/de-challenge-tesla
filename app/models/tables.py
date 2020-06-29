from datetime import datetime

import sqlalchemy as sa

from app.models.base import Base


class Events(Base):
    """table to store earthquake events
    """
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    mag = sa.Column(sa.Float)
    place = sa.Column(sa.String)
    time = sa.Column(sa.DateTime)
    updated = sa.Column(sa.DateTime)
    tz = sa.Column(sa.Integer)
    url = sa.Column(sa.String)
    detail = sa.Column(sa.String)
    felt = sa.Column(sa.Integer)
    cdi = sa.Column(sa.Float)
    mmi = sa.Column(sa.Float)
    alert = sa.Column(sa.String)
    status = sa.Column(sa.String)
    tsunami = sa.Column(sa.Integer)
    sig = sa.Column(sa.Integer)
    net = sa.Column(sa.String)
    code = sa.Column(sa.String)
    ids = sa.Column(sa.String)
    sources = sa.Column(sa.String)
    types = sa.Column(sa.String)
    nst = sa.Column(sa.Integer)
    dmin = sa.Column(sa.Float)
    rms = sa.Column(sa.Float)
    gap = sa.Column(sa.Float)
    magType = sa.Column(sa.String)
    type = sa.Column(sa.String)
    title = sa.Column(sa.String)
    longitude = sa.Column(sa.Float)
    latitude = sa.Column(sa.Float)
    depth = sa.Column(sa.Float)

    def __init__(self, mag: float, place: str, time: datetime,
                 updated: datetime, tz: int, url: str, detail: str, felt: int,
                 cdi: float, mmi: float, alert: str, status: str, tsunami: int,
                 sig: int, net: str, code: str, ids: str, sources: str,
                 types: str, nst: int, dmin: float, rms: float, gap: float,
                 magType: str, type: str, title: str, longitude: float,
                 latitude: float, depth: float):
        self.mag = mag
        self.place = place
        self.time = time
        self.updated = updated
        self.tz = tz
        self.url = url
        self.detail = detail
        self.felt = felt
        self.cdi = cdi
        self.mmi = mmi
        self.alert = alert
        self.status = status
        self.tsunami = tsunami
        self.sig = sig
        self.net = net
        self.code = code
        self.ids = ids
        self.sources = sources
        self.types = types
        self.nst = nst
        self.dmin = dmin
        self.rms = rms
        self.gap = gap
        self.magType = magType
        self.type = type
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.depth = depth
