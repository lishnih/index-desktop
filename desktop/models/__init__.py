#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class Task(Base):                               # rev. 20130224
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Имя задачи
    status    = Column(Integer)                 # Состояние
    img       = Column(String)                  # Изображение
    pos_x     = Column(Integer)                 # Позиция
    pos_y     = Column(Integer)
    count     = Column(Integer)                 # Кол-во элементов в задаче
    method    = Column(String)                  # Метод, которым будут обрабатываться данные
    created   = Column(Integer, default=datetime.utcnow)  # Время создания задания
    updated   = Column(Integer, onupdate=datetime.utcnow) # Время обновления задания

#     def __init__(self, **kargs):
#         Base.__init__(self, **kargs)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Задача '{}' (Состояние {})>".format(self.name, self.status)


class Source(Base):                             # rev. 20130224
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    _tasks_id = Column(Integer, ForeignKey('tasks.id', onupdate='CASCADE', ondelete='CASCADE'))
    _task = relationship(Task, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя файла
    type      = Column(String)                  # Файл/директория
    status    = Column(Integer)                 # Состояние
    method    = Column(String)                  # для пакета index
    indexed   = Column(Integer, default=datetime.utcnow)  # Время последней индексации

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if   os.path.isdir(self.name):
            self.type = 'dir'
        elif os.path.isfile(self.name):
            self.type = 'file'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Источник '{}' <{}> (Состояние {})>".format(self.name, self.type, self.status)


class Option(Base):                             # rev. 20130223
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    _tasks_id = Column(Integer, ForeignKey('tasks.id', onupdate='CASCADE', ondelete='CASCADE'))
    _task = relationship(Task, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _source_id = Column(Integer, ForeignKey('sources.id', onupdate='CASCADE', ondelete='CASCADE'))
    _source = relationship(Source, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя параметра
    type      = Column(String)                  # Тип
    status    = Column(Integer)                 # Состояние
    value     = Column(Integer)                 # Значение

#     def __init__(self, **kargs):
#         Base.__init__(self, **kargs)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Параметр '{}' <{}>='{}' (Состояние {})>".format(self.name, self.type, self.value, self.status)
