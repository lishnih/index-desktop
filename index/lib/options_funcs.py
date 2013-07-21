#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-23

import os, pickle, logging


def load_entry(filename):
    entry = {}
    with open(filename, 'rb') as f:
        try:
            entry = pickle.load(f)
        except Exception as e:
            logging.error(filename)
            logging.error(e)

    return entry


def get_options(datadir=None, method=None):
    if datadir and method:
        filename = os.path.join(datadir, "{0}.pickle".format(method))
        options = load_entry(filename)
    else:
        options = {}

    return options
