from src.extensions import db
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseDateTimeModel(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
