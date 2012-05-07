#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from sqlalchemy import create_engine

from models import DBSession, Base


# Подразумеваем, что:
# Директория папки скрипта ~/scripts
# Директория данных ~/data
db_uri = 'sqlite:///../../data/welding.sqlite'


def initdb():
    engine = create_engine(db_uri)

    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
