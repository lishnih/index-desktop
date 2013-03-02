#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import os, shutil, logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def initDb(db_uri=None, session=None, base=None):
    if not db_uri:
        db_uri = getDefaultDb()
    if not session:
        session = scoped_session(sessionmaker())

    engine = create_engine(db_uri)

    if engine.name == 'sqlite':
        filename = engine.url.database
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if not os.path.isdir(dirname):
            logging.error(u'Невозможно создать директорию "{}"'.format(dirname))
            return

    session.configure(bind=engine)
    if base:
        base.metadata.create_all(engine)

    return session


def getDefaultDb():
    dbname = "index"
    home = os.path.expanduser("~")
    db_path = os.path.join(os.path.expanduser("~"), "{}.sqlite".format(dbname))
    db_uri = 'sqlite:///{}'.format(db_path)
#   db_uri = 'mysql+oursql://root:54321@localhost/{}'.format(dbname)

    return db_uri


def cleanDb(engine):
    pass


def archiveDb(engine):
    if engine.name == 'sqlite':
        filename = engine.url.database
        archivefile(filename)
    else:
        logging.warning(u"Для данного типа БД архивирование не предусмотрено: {}, пропускаем архивирование!".format(engine.name))


def archiveFile(filename):
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
