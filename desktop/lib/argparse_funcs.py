#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-23

import os, argparse


class readable_file(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(values):
            raise argparse.ArgumentTypeError(u"FILE: '{0}' is not a valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(u"FILE: '{0}' is not a readable file".format(values))


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == '~':
            setattr(namespace, self.dest, values)
            return

        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(u"DIR: '{0}' is not a valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(u"DIR: '{0}' is not a readable dir".format(values))


class readable_file_or_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == '~':
            setattr(namespace, self.dest, values)
            return

        if not os.path.exists(values):
            raise argparse.ArgumentTypeError(u"DIR_or_FILE: '{0}' is not a valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(u"DIR_or_FILE: '{0}' is not a readable dir".format(values))


class readable_file_or_dir_list(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            if value[0] == '~':
                setattr(namespace, self.dest, values)
                continue

            if not os.path.exists(value):
                raise argparse.ArgumentTypeError(u"DIR_or_FILE: '{0}' is not a valid path".format(value))
            if os.access(value, os.R_OK):
                self.append_file(namespace, value)
            else:
                raise argparse.ArgumentTypeError(u"DIR_or_FILE: '{0}' is not a readable dir".format(value))

    def append_file(self, namespace, value):
        files_list = getattr(namespace, self.dest)
        if not files_list:
            files_list = []
        files_list.append(value)
        setattr(namespace, self.dest, files_list)
