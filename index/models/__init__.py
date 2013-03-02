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


class Dir(Base):                                # rev. 20120930
    __tablename__ = 'dirs'
    id = Column(Integer, primary_key=True)
    _sources_id = Column(Integer, ForeignKey('sources.id', onupdate='CASCADE', ondelete='CASCADE'))
    _source = relationship(Source, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя директории
    ndirs     = Column(Integer)                 # Кол-во поддиректорий
    nfiles    = Column(Integer)                 # Суммарное кол-во файлов
    volume    = Column(Integer)                 # Объём директории

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Директория '{}'>".format(self.name)


class File(Base):                               # rev. 20120928
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    _dirs_id = Column(Integer, ForeignKey('dirs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _dir = relationship(Dir, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя файла
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
    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя листа
    seq       = Column(Integer)                 # Номер листа в файле
    ncols     = Column(Integer)                 # Кол-во колонок в листе
    nrows     = Column(Integer)                 # Кол-во строк в листе
    visible   = Column(Integer)                 # Видимость листа
    sh        = Column(String)                  # Аттрибут для возможности передать переменную sh

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if self.sh:
            self.name  = self.sh.name
            self.ncols = self.sh.ncols
            self.nrows = self.sh.nrows
            self.visible = self.sh.visibility
            self.sh = None

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Таблица '{}' (файл: '{}')>".format(self.name, self._file.name)


class Doc(Base):                                # rev. 20121020
    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)

    name       = Column(String)                 # Номер документа
    doc_pre    = Column(String)
    doc_seq    = Column(Integer)
    doc_sign   = Column(String)
    type       = Column(String)
    date       = Column(Integer)                # Дата
    date_str   = Column(String)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.doc_pre, self.doc_seq])
            name_list = map(unicode, name_list)
            self.name = u"/".join(name_list)
            if self.doc_sign:
                self.name += ' ' + format(self.doc_sign)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Документ ({}) '{}' от '{}'>".format(self.type, self.name, self.date_str)


class Piece(Base):                              # rev. 20121020
    __tablename__ = 'pieces'
    id = Column(Integer, primary_key=True)

    name       = Column(String)                 # Наименование изделия
    piece_type = Column(String)
    piece_name = Column(String)
    piece_scheme = Column(String)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.piece_type, self.piece_name, self.piece_scheme])
            name_list = map(unicode, name_list)
            self.name = u" ".join(name_list)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Изделие '{}'>".format(self.name)


class Piece_entry(Base):                        # rev. 20121020
    __tablename__ = 'piece_entries'
    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate='CASCADE', ondelete='CASCADE'))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _pieces_id = Column(Integer, ForeignKey('pieces.id', onupdate='CASCADE', ondelete='CASCADE'))
    _piece = relationship(Piece, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name       = Column(String)                 # Наименование
    piece      = Column(String)
    object     = Column(String)                 # Объект
    scheme     = Column(String)                 # Схема
    mfr        = Column(String)                 # Производитель
    order      = Column(Integer)                # Заказ
    qnt        = Column(Float)                  # Кол-во
    meas       = Column(String)
    invoice    = Column(Integer)                # Т/н
    cert_type  = Column(String)                 # Сертификат
    cert       = Column(Integer)
    y          = Column(Integer)                # y

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            self.name = u"{} [{}]".format(self.piece, self.y)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Запись изделия '{}' (лист: '{}')>".format(self.name, self._sheet.name)


class Joint(Base):                              # rev. 20121015
    __tablename__ = 'joints'
    id = Column(Integer, primary_key=True)

    name        = Column(String)                # Номер стыка
#   joint_kind  = Column(String)
    joint_pre   = Column(String)
    joint_line  = Column(String)
    joint_seq   = Column(Integer)
#   joint_sign  = Column(String)
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


class Joint_entry(Base):                        # rev. 20121020
    __tablename__ = 'joint_entries'

    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate='CASCADE', ondelete='CASCADE'))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _joints_id = Column(Integer, ForeignKey('joints.id', onupdate='CASCADE', ondelete='CASCADE'))
    _joint = relationship(Joint, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name        = Column(String)                # Номер записи
    joint       = Column(String)
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
