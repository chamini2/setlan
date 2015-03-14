#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# config.py
#
# Global Setlan minor configuration parameters.
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------

from exceptions import (SetlanValueError, SetlanOverflowError)

class SetlanConfig(object):
    """Global configuration for Setlan language structures"""

    VERSION = '0.3'

    PROMPT = '>>> '

    SUCCESS = 0
    ERR_BAD_USAGE = 1
    ERR_BAD_FILENAME = 2
    ERR_IO_ERROR = 3
    ERR_LEXICOGRAPHICAL_ERROR = 4
    ERR_VALUE_ERROR = 5
    ERR_INPUT_NOT_PROVIDED = 6
    ERR_LANG_LEX_MODULE_NOT_PROVIDED = 7
    ERR_SYNTAX_ERROR = 8
    ERR_STATIC_ERROR = 9
    ERR_SCOPE_ERROR = 10
    ERR_TYPE_ERROR = 11
    ERR_ZERO_DIVISION = 12
    ERR_OVERFLOW = 13
    ERR_EMPTY_SET = 14
    ERR_KEYBOARD_INTERRUPT = 15

    SPACE = "    "

    def __init__(self, *args, **kwargs):
        super(SetlanConfig, self).__init__()

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def _get_indentation(self, level):
        return level * self.SPACE

    def _execute(self):
        print "%s%s: Not Implemented" % (self.getIndent(level), self.__class__.__name__)

    def _evaluate(self):
        print "%s%s: Not Implemented" % (self.getIndent(level), self.__class__.__name__)
        return None

    def str2bool(self, v):
        string = v.strip().lower()
        if string in ("yes", "true", "t", "y", "1"):
            return True
        elif string in ("no", "false", "f", "n", "0"):
            return False
        else:
            return None

    def str2int(self, v):
        try:
            integer = int(v)
        except ValueError as ve:
            return None
        return integer

    def checkOverflow(self, integer, position):
        overflow = False
        error = ""
        if integer < -2147483648:
            overflow = True
            error += "In line %d, column %d, " % position
            error += "integer is less than -2147483648. Setlan supports only "
            error += "32 bit signed integers."
        elif integer > 2147483647:
            overflow = True
            error += "In line %d, column %d, " % position
            error += "integer is greater than 2147483647. Setlan supports "
            error += "only 32 bit signed integers."
        if overflow:
            raise SetlanOverflowError(error)
        return integer