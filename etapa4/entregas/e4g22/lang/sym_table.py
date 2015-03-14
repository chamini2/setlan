#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# sym_table.py
#
# Setlan Symbol Table and data type representations.
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from config import SetlanConfig

from exceptions import (SetlanScopeError, SetlanStaticErrors)

from type import Type

class VariableInfo(object):
    """Container for the information stored for each variable in a SymTable."""
    def __init__(self, type_class, *args, **kwargs):
        super(VariableInfo, self).__init__()
        self._type = type_class
        self._value = kwargs.get('value', None)
        self._read_only = kwargs.get('read_only', False)

    def __str__(self):
        string = "{ type : '%s', value : '%s' }" % (
            self._type,
            str(self._value)
            )
        return string

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def getType(self):
        return self._type

    def setType(self, type_class):
        self._type = type_class

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def isReadOnly(self):
        return self._read_only

    def canAssign(self, type_class):
        return self._type.canBeAssigned(type_class)

    def isInt(self):
        return self._type.isInt()

    def isBool(self):
        return self._type.isBool()

    def isSet(self):
        return self._type.isSet()


class SymTable(SetlanConfig):
    """
    Setlan language symbol table. Represents a context and
    ensures the proper checking of names scope.
    """

    def __init__(self, father=None, scope=None, *args, **kwargs):
        """
        Params:
            scope  :
                type : dictionary
                        keys   : names of variables.
                        values : type class of the variables.
            father :
                type: SymTable father of this SymTable.
        """
        super(SymTable, self).__init__(args, kwargs)
        if scope is None : self._scope = {}
        else: self._scope = scope
        self._children = []
        if father is not None: father._birth(self)
        self._father = father

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._print(0)

    def getFather(self):
        return self._father

    def _format_entry(self, name, info):
        value = info.getValue()
        if info.getType().isSet():
            if isinstance(value, set):
                string = "{"
                if value:
                    first = True
                    for elem in value:
                        if first:
                            first = not first
                            string += str(elem)
                        else:
                            string += ", " + str(elem)
                string += "}"
                value = string
        string = "Variable: %s | Type: %s | Value: %s" % (
            name, str(info.getType()), str(value)
            )
        return string

    def _print(self, level):
        string = "%sScope:" % self._get_indentation(level)
        if self._scope is not None and self._scope:
            string += "\n%sVariables:" % self._get_indentation(level+1)
            for name, info in self._scope.iteritems():
                string += "\n%s%s" % (
                    self._get_indentation(level+2),
                    self._format_entry(name, info)
                    )
        if self._children is not None and self._children:
            string += "\n%sChildren:" % self._get_indentation(level+1)
            for symtable in self._children:
                string += "\n%s" % symtable._print(level+2)
        string += "\n%sEnd of Scope" % self._get_indentation(level)
        return string
        
    def _birth(self, child):
        """
        Creates the reference from the father to its children
        """
        self._children.append(child)

    def insert(self, name, type_class, position, *args, **kwargs):
        """
        Adds a new symbol to this SymTable
        """
        if name in self._scope:
            error  = "In line %d, column %d, " % position
            error += "variable '%s' was already defined." % name
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))
        value = None
        if kwargs.get('read_only', False):
            value = VariableInfo(type_class, read_only=True)
        else:
            value = VariableInfo(type_class)
        value.setValue(kwargs.get('value', type_class.getDefault()))
        self._scope[name] = value

    def delete(self, name, position):
        """
        Deletes a symbol from this SymTable (WHY IS THIS NECESSARY???)
        """
        if name in self._scope:
            del self._scope[name]
        elif self._father is not None:
            self._father.delete(name, position)
        else:
            error  = "In line %d, column %d, " % position
            error += "trying to delete variable '%s' from the current " % name
            error += "scope, but it has not been defined."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))

    def update(self, name, value, position):
        """
        Updates the value of a symbol in this SymTable
        """
        if name in self._scope:
            previous = self._scope[name]
            previous.setValue(self.checkOverflow(value, position))
            self._scope[name] = previous
        elif self._father is not None:
            self._father.update(name, value, position)
        else:
            error  = "In line %d, column %d, " % position
            error += "trying to update variable '%s' from the current " % name
            error += "scope, but it has not been defined."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))

    def contains(self, name):
        """
        Checks if a given name is in this SymTable.
        """
        if name in self._scope:
            return True
        elif self._father is not None:
            return self._father.contains(name)
        else:
            return False

    def lookup(self, name, position):
        """
        Retrieves the type and value associated with a given name if it is in
        this SymTable, otherwise, raise a SetlanScopeError exception. 
        """
        if name in self._scope:
            return self._scope[name]
        elif self._father is not None:
            return self._father.lookup(name, position)
        else:
            error  = "In line %d, column %d, " % position
            error += "trying to use variable '%s', " % name
            error += "but it has not been defined in current scope."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))
            return VariableInfo(Type(position=position))






