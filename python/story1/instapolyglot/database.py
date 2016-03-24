import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement


DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///instapolyglot.db')
engine = create_engine(DATABASE_URI)
session_builder = sessionmaker(bind=engine)
ModelBase = declarative_base()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {
            k: v for k, v in kwargs.items()
            if not isinstance(v, ClauseElement)
        }
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
