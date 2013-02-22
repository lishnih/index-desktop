#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import os, shutil, logging
from sqlalchemy import create_engine


# Подразумеваем, что:
# Директория папки скрипта ~/scripts
# Директория данных ~/data
scriptname = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
dbname = scriptname.replace('pyside-', '')
db_uri = 'sqlite:///../../data/{}.sqlite'.format(dbname)

# При использовании mysql за название БД принимаем имя пользователя (~)
# dbname = os.path.basename(os.path.dirname(os.path.dirname(
#                           os.path.dirname(os.path.dirname(__file__)))))
# db_uri = 'mysql+oursql://root:54321@localhost/{}'.format(dbname)

engine = None


def initdb(DBSession, Base):
    global engine

    if not engine:
        engine = create_engine(db_uri)

        if engine.name == 'sqlite':
            filename = engine.url.database
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            if not os.path.isdir(dirname):
                logging.error(u'Невозможно создать директорию "{}"'.format(dirname))
                return

        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    return engine


def cleandb(engine):
    pass


def archivedb(engine):
    if engine.name == 'sqlite':
        filename = engine.url.database
        archivefile(filename)
    else:
        logging.warning(u"Для данного типа БД архивирование не предусмотрено: {}, пропускаем архивирование!".format(engine.name))


def archivefile(filename):
    if os.path.isfile(filename):
        timestamp = int(os.path.getmtime(filename))

        dirname   = os.path.dirname(filename)
        basename  = os.path.basename(filename)
        root, ext = os.path.splitext(basename)

        basename_new = u"{}_{}{}".format(root, timestamp, ext)
        dirname_new  = os.path.join(dirname, u"backup")
        if not os.path.exists(dirname_new):
            os.makedirs(dirname_new)
        filename_new = os.path.join(dirname_new, basename_new)
        shutil.copy(filename, filename_new)
