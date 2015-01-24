#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the language Setlan
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------

class SetlanException(Exception):

    def __init__(self, error, *args, **kwargs):
        super(SetlanException, self).__init__(args,kwargs)
        self._error = error

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

class SetlanLexicalError(SetlanException):

    def __unicode__(self):
        string = "SetlanLexicalError: %s" % self._error
        return string

class SetlanValueError(SetlanException):

    def __unicode__(self):
        string = "SetlanValueError: %s" % self._error
        return string