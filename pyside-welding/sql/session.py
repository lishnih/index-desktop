#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10


db_uri = 'sqlite:///../../data/welding.sqlite'


# DBSession
from sqlalchemy.orm import scoped_session, sessionmaker
# from zope.sqlalchemy import ZopeTransactionExtension
# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DBSession = scoped_session(sessionmaker())

# Engine
from sqlalchemy import create_engine
engine = create_engine(db_uri)


# Создаём таблицы
from model import metadata
metadata.create_all(engine)


# Биндим БД к сессии
DBSession.configure(bind=engine)
