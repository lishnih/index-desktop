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


class Task(Base):                               # rev. 20120905
    __tablename__ = 'tasks'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name      = Column(String(length=255))      # Имя задания
    type      = Column(String(length=255))      # Файл/директория
    source    = Column(String(length=255))      # Источник (имя файла)
#   created   = Column(Integer, default=datetime.utcnow)  # Время создания задания
#   updated   = Column(Integer, onupdate=datetime.utcnow) # Время обновления задания

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if   os.path.isdir(self.source):
            self.type = 'dir'
        elif os.path.isfile(self.source):
            self.type = 'file'        

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Задача '{}' (Источник {}: '{}')>".format(self.name, self.type, self.source)
        

class Dir(Base):                                # rev. 20120913
    __tablename__ = 'dirs'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _tasks_id = Column(Integer, ForeignKey('tasks.id', onupdate='CASCADE', ondelete='CASCADE'))
    _task = relationship(Task, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String(length=255))      # Имя директории
    ndirs     = Column(Integer)                 # Кол-во поддиректорий
    nfiles    = Column(Integer)                 # Суммарное кол-во файлов
    volume    = Column(Integer)                 # Объём директории

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Директория '{}'>".format(self.name)


class File(Base):                               # rev. 20120913
    __tablename__ = 'files'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _dirs_id = Column(Integer, ForeignKey('dirs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _dir = relationship(Dir, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String(length=255))      # Имя файла
    size      = Column(Integer)                 # Размер
    mtime     = Column(Integer)                 # Время модификации

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if os.path.isfile(self.name):
            statinfo   = os.stat(self.name)
            self.size  = statinfo.st_size
            self.mtime = statinfo.st_mtime

            if self._dir:
                if self._dir.nfiles is None:
                    self._dir.nfiles = 0
                if self._dir.volume is None:
                    self._dir.volume = 0

                self._dir.nfiles += 1
                self._dir.volume += self.size

            self.name  = os.path.basename(self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Файл '{}'>".format(self.name)


class Sheet(Base):                              # rev. 20120913
    __tablename__ = 'sheets'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String(length=255))      # Имя листа
    seq       = Column(Integer)                 # Номер листа в файле
    ncols     = Column(Integer)                 # Кол-во колонок в листе
    nrows     = Column(Integer)                 # Кол-во строк в листе
    visible   = Column(Integer)                 # Видимость листа

    def __init__(self, sh, **kargs):
        Base.__init__(self, **kargs)
        self.name  = sh.name
        self.ncols = sh.ncols
        self.nrows = sh.nrows
        self.visible = sh.visibility

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Таблица '{}' (файл: '{}')>".format(self.name, self._file.name)


class Report(Base):                             # rev. 20120921
    __tablename__ = 'reports'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name        = Column(String(length=255))    # Номер акта/заключения
    report_pre  = Column(String(length=255))
    report_seq  = Column(Integer)
    report_sign = Column(String(length=255))
    method      = Column(String(length=255))
    date        = Column(Integer)
    date_str    = Column(String(length=255))

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.report_pre, self.report_seq])
            name_list = map(unicode, name_list)
            self.name = u"/".join(name_list)
            if self.report_sign:
                self.name += ' ' + format(self.report_sign)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Заключение '{}'>".format(self.name)


class Joint(Base):                              # rev. 20120921
    __tablename__ = 'joints'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name        = Column(String(length=255))    # Номер стыка
#   joint_kind  = Column(String(length=255))
    joint_pre   = Column(String(length=255))
    joint_line  = Column(String(length=255))
    joint_seq   = Column(Integer)
#   joint_sign  = Column(String(length=255))
    diameter1   = Column(Integer)
    diameter2   = Column(Integer)
    thickness1  = Column(Float)
    thickness2  = Column(Float)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.joint_pre, self.joint_line, self.joint_seq])
            name_list = map(unicode, name_list)
            self.name = u"-".join(name_list)
#             if self.joint_sign:
#                 self.name += ' ' + format(self.joint_sign)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Стык '{}'>".format(self.name)


class Joint_entry(Base):                        # rev. 20120921
    __tablename__ = 'joint_entries'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate='CASCADE', ondelete='CASCADE'))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _reports_id = Column(Integer, ForeignKey('reports.id', onupdate='CASCADE', ondelete='CASCADE'))
    _report = relationship(Report, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _joints_id = Column(Integer, ForeignKey('joints.id', onupdate='CASCADE', ondelete='CASCADE'))
    _joint = relationship(Joint, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name        = Column(String(length=255))    # Номер записи
    joint       = Column(String(length=255))
    welders     = Column(String(length=255))
    method      = Column(String(length=255))
    d_w_th      = Column(String(length=255))
    defects     = Column(String(length=255))
    report      = Column(String(length=255))
    date        = Column(Integer)
    date_str    = Column(String(length=255))
    decision    = Column(String(length=255))
    y           = Column(Integer)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            self.name = u"{} [{}]".format(self.joint, self.y)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Запись стыка '{}' (лист: '{}')>".format(self.name, self._sheet.name)



if __name__ == '__main__':
    pass
