#!/usr/bin/env python
# ------------------------------------------------------------
# type.py
#
# Setlan type representation classes
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from config import SetlanConfig

class Type(SetlanConfig):

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = None

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return True
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return True

    def __hash__(self):
        """
        Override the default hash behavior (that returns the id or the object)
        """
        dictionary = {
            "class" : self.__class__,
            "default" : self._default
        }
        return hash(tuple(sorted(dictionary.items())))

    def __unicode__(self):
        return "undefined"

    def __str__(self):
        return self.__unicode__()

    def getPosition(self):
        return self._position

    def getDefault(self):
        return self._default

    def canBeAssigned(self, value):
        return False

    def print_ast(self, level):
        string = "%s%s\n" % (
            self._get_indentation(level),
            self
            )
        return string

    def canBeAssigned(self, type_class):
        return self == type_class

    def isInt(self):
        return False

    def isBool(self):
        return False

    def isSet(self):
        return False


class IntegerType(Type):

    def __init__(self, *args, **kwargs):
        super(IntegerType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = 0

    def __unicode__(self):
        return "Integer"

    def isInt(self):
        return True


class BooleanType(Type):

    def __init__(self, *args, **kwargs):
        super(BooleanType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = False

    def __unicode__(self):
        return "Boolean"

    def isBool(self):
        return True


class SetType(Type):

    def __init__(self, *args, **kwargs):
        super(SetType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = set([])

    def __unicode__(self):
        return "Set"

    def isSet(self):
        return True