#!/usr/bin/env python
# coding=utf-8

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from index_desktop import __pkgname__, __description__, __version__

import sys
import os
from setuptools import setup, find_packages

py_version = sys.version_info[:2]
PY3 = py_version[0] == 3
if PY3:
    if py_version < (3, 3):
        raise RuntimeError('On Python 3, Index requires Python 3.3 or better')
else:
    if py_version < (2, 6):
        raise RuntimeError('On Python 2, Index requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
try:
    README = open(os.path.join(here, 'README.md')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''


if __name__ == '__main__':
    setup(
        name=__pkgname__,
        description=__description__,
        version=__version__,
        long_description=README,

        author='Stan',
        author_email='lishnih@gmail.com',
        url='http://github.com/lishnih/index-desktop',
        platforms=['any'],
        keywords=['PySide', 'indexing', 'reporting', 'documents'],

        packages=find_packages(),
#       include_package_data=True,
#       zip_safe=False,

        package_data={__pkgname__: []},

        scripts=[
            'scripts/run_index_desktop.py',
        ],

        install_requires=[
            'PySide',
        ],

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 3.3',
            'Topic :: Utilities',
        ],
    )
