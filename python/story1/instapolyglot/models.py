from sqlalchemy import Column, String

from .database import ModelBase


class Picture(ModelBase):
    __tablename__ = 'pictures'

    id = Column(String, primary_key=True)
    link = Column(String, nullable=False)
    low_resolution = Column(String)
    thumbnail = Column(String)
    standard_resolution = Column(String)
