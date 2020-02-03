# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


logger = logging.getLogger()

# TODO Make all variables configurable

DATABASE_URL = 'course-picker.c7xxomx5jxvz.us-east-1.rds.amazonaws.com'

def get_engine(uri):
    logger.info("Connecting to database..")
    options = {
        "pool_recycle": 3600,
        "pool_size": 10,
        "pool_timeout": 30,
        "max_overflow": 30,
        "echo": True,
        "execution_options": {"autocommit": True},
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())
engine = get_engine(DATABASE_URL)


def init_session():
    db_session.configure(bind=engine)

    from app.model import Base

    Base.metadata.create_all(engine)
