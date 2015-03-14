#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the language Setlan
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from lib.singleton import Singleton


class SetlanException(Exception):

    def __init__(self, error, *args, **kwargs):
        super(SetlanException, self).__init__(args,kwargs)
        self._error = error

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class SetlanInputNotDefinedException(SetlanException):

    def __unicode__(self):
        string = "SetlanInputNotDefinedException: %s" % self._error
        return string


class SetlanTokensNotDefinedException(SetlanException):

    def __unicode__(self):
        string = "SetlanTokensNotDefinedException: %s" % self._error
        return string


class SetlanLexicalErrors(SetlanException):

    def __init__(self, errors, *args, **kwargs):
        error = "Lexical errors were found:"
        super(SetlanLexicalErrors, self).__init__(error, args, kwargs)
        self._errors = errors

    def __unicode__(self):
        string = "SetlanLexicalErrors: %s" % self._error
        for error in self._errors:
            string += "\n\t%s" % error
        return string


class SetlanLexicalError(SetlanException):

    def __unicode__(self):
        string = "SetlanLexicalError: %s" % self._error
        return string


class SetlanValueError(SetlanException):

    def __unicode__(self):
        string = "SetlanValueError: %s" % self._error
        return string


class SetlanSyntaxError(SetlanException):

    def __unicode__(self):
        string = "SetlanSyntaxError: %s" % self._error
        return string


class SetlanScopeError(SetlanException):

    def __unicode__(self):
        string = "SetlanScopeError: %s" % self._error
        return string


class SetlanTypeError(SetlanException):

    def __unicode__(self):
        string = "SetlanTypeError: %s" % self._error
        if "undefined" in string:
            string += " This is probably due to a previous static error "
            string += "(undefined variable or type error)."
        return string


class SetlanReadOnlyModificationError(SetlanException):

    def __unicode__(self):
        string = "SetlanReadOnlyModificationError: %s" % self._error
        return string


@Singleton
class SetlanStaticErrors(SetlanException):

    def __init__(self):
        self._error = "Static check time errors were found:"
        self._errors = []

    def __unicode__(self):
        string = "SetlanStaticErrors: %s" % self._error
        for error in self._errors:
            string += "\n\t%s" % error
        return string

    def add_error(self, error):
        if not "undefined" in error._error:
            self._errors.append(error)

    def has_errors(self):
        return (self._errors is not None) and self._errors


class SetlanZeroDivisionError(SetlanException):

    def __unicode__(self):
        string = "SetlanZeroDivisionError: %s" % self._error
        return string


class SetlanOverflowError(SetlanException):

    def __unicode__(self):
        string = "SetlanOverflowError: %s" % self._error
        return string


class SetlanEmptySetError(SetlanException):

    def __unicode__(self):
        string = "SetlanEmptySetError: %s" % self._error
        return string