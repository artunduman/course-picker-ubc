# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import enum

logger = logging.getLogger()

# TODO Make all variables configurable

DATABASE_URL = ''  # TODO change it and make configurable
Base = declarative_base()


class DatabaseAccess:
    def __init__(self, session=None, engine=None):
        self.session = session or sessionmaker()
        self.engine = engine or self._create_engine(DATABASE_URL)

    @staticmethod
    def _create_engine(uri):
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

    def init_session(self):
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)


class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    fullname = Column(String, unique=True)

    def __repr__(self):
        return "<Professor(fullname='%s')>" % (
            self.fullname
        )


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    campus = Column(String)
    year = Column(Integer)
    session = Column(String)
    subject = Column(String)  # CPSC
    code = Column(String)     # 313
    detail = Column(String)
    section = Column(String)
    title = Column(String)
    professor = Column(String)
    enrolled = Column(Integer)
    avg = Column(Float)
    std_dev = Column(Float)
    high = Column(Float)
    low = Column(Float)
    professor_id = Column(Integer, ForeignKey('professors.id'))

    def __repr__(self):
        return "<Grade(campus='%s', year='%s', session='%s', subject='%s', code='%s', detail='%s', " \
               "section='%s', title='%s', professor='%s', enrolled='%s', avg='%s', std_dev='%s', high='%s', " \
               "low='%s')>" % (
                self.campus,
                self.year,
                self.session,
                self.subject,
                self.code,
                self.detail,
                self.section,
                self.title,
                self.professor,
                self.enrolled,
                self.avg,
                self.std_dev,
                self.high,
                self.low
                )
