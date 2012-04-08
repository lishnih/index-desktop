#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.event import listen


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Task(Base):                       # rev. 20120408
    __tablename__ = 'tasks'
    id        = Column(Integer, primary_key=True)

    name      = Column(String)          # Имя задания
    type      = Column(String)          # Файл/директория
    source    = Column(String)          # Источник (имя файла)
    created   = Column(Integer, default=datetime.utcnow())  # Время создания задания
    updated   = Column(Integer, onupdate=datetime.utcnow)   # Время обновления задания

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if   os.path.isdir(self.source):
            self.type = 'dir'
        elif os.path.isfile(self.source):
            self.type = 'file'        

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Задача '{}' ['{}' ({})]".format(self.name, self.source, self.type)
        

class Dir(Base):                        # rev. 20120408
    __tablename__ = 'dirs'
    id        = Column(Integer, primary_key=True)
    _tasks_id = Column(Integer, ForeignKey('tasks.id', onupdate="CASCADE", ondelete="CASCADE"))

    name      = Column(String)          # Имя директории
    dirs      = Column(Integer)         # Кол-во поддиректорий
    nfiles    = Column(Integer)         # Суммарное кол-во файлов
    volume    = Column(Integer)         # Объём директории

    task = relationship(Task, backref=backref('dirs', cascade='all, delete, delete-orphan'))

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Директория '{}'".format(self.name)


class File(Base):                       # rev. 20120408
    __tablename__ = 'files'
    id        = Column(Integer, primary_key=True)
    _dirs_id  = Column(Integer, ForeignKey('dirs.id', onupdate="CASCADE", ondelete="CASCADE"))

    name      = Column(String)          # Имя файла
    size      = Column(Integer)         # Размер
    mtime     = Column(Integer)         # Время модификации
    nsheets   = Column(Integer)         # Кол-во листов

    dir = relationship(Dir, backref=backref('files', cascade='all, delete, delete-orphan'))

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if os.path.isfile(self.name):
            statinfo   = os.stat(self.name)
            self.size  = statinfo.st_size
            self.mtime = statinfo.st_mtime

            self.name  = os.path.basename(self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Файл '{}'".format(self.name)


class Sheet(Base):                      # rev. 20120408
    __tablename__ = 'sheets'
    id        = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))

    name      = Column(String)          # Имя листа
    seq       = Column(Integer)         # Номер листа в файле
    cols      = Column(Integer)         # Кол-во колонок в листе
    rows      = Column(Integer)         # Кол-во строк в листе
    visible   = Column(Integer)         # Видимость листа

    file = relationship(File, backref=backref('sheets', cascade='all, delete, delete-orphan'))

    def __init__(self, sh=None, **kargs):
        Base.__init__(self, **kargs)
        if sh:
            self.name = sh.name
            self.cols = sh.ncols
            self.rows = sh.nrows
            self.visible = sh.visibility

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Таблица '{}'".format(self.name)


class Joint(Base):                      # rev. 20120408
    __tablename__ = 'joints'
    id        = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate="CASCADE", ondelete="CASCADE"))

    name      = Column(String)          # Номер стыка (общий)
    y         = Column(Integer)
    date      = Column(String)
    date_str  = Column(String)
    t         = Column(String)
    d1        = Column(String)
    d2        = Column(String)
    th1       = Column(String)
    th2       = Column(String)
    gost      = Column(String)
    wt        = Column(String)
    kp        = Column(String)
    type      = Column(String)
    seq       = Column(Integer)
    elem1     = Column(String)
    elem2     = Column(String)
    code1     = Column(String)
    code2     = Column(String)
    sn1       = Column(String)
    sn2       = Column(String)
    len1      = Column(String)
    len2      = Column(String)
    scheme    = Column(String)

    sheet = relationship(Sheet, backref=backref('joints', cascade='all, delete, delete-orphan'))

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if isinstance(self.seq, float):
            self.seq = int(self.seq)
        self.name = u'{}/{}/{}'.format(self.kp, self.type, self.seq)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Стык '{}'".format(self.name)



if __name__ == '__main__':
    pass
