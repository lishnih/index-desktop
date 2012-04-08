#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import logging
from PySide import QtCore


# Функции обработки запускаем отдельным процессом
# (чтобы не замораживать Gui)
class Thread(QtCore.QThread):
    def __init__(self):
        super(Thread, self).__init__()

        # Таймер
        self.timer = QtCore.QTimer(self)
        self.interval = 1000
        self.update_func = None
        self.ending_func = None
        self.timer.timeout.connect(self.update)

        # Вывод
        self.message = ""


    def set_callback(self, update_func, ending_func=None):
        self.update_func = update_func
        self.ending_func = ending_func


    def update(self):
        if self.isRunning():
            self.secs += self.interval
            if self.update_func:
                self.update_func(self.secs)
        else:
            self.timer.stop()
            if self.ending_func:
                self.ending_func(self.secs, self.message)


    def start(self, func, *args):
        self.secs = 0
        self.timer.start(self.interval)

        self.func = func
        self.args = args
        super(Thread, self).start()


    def run(self):
        if self.func:
            try:
                self.message = self.func(*self.args)
            except Exception, e:
                error_str = u"Завершено с ошибкой: %s" % e
                logging.exception(error_str)
                self.message = error_str


th = Thread()
