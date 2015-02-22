#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Symbol Table for Setlan
Matteo Ferrando, 09-10285
"""

import Errors

class Symbol(object):
    """A symbol that goes inside the symbol table"""
    def __init__(self, data_type, var, value):
        self.name = var.value
        self.type = data_type
        self.value = value
        self.lexspan = var.lexspan

class SymbolTable(object):
    """A symbol table representation"""
    def __init__(self):
        self.scope = {}

    def __iter__(self):
        return iter(self.scope.values())

    def __nonzero__(self):
        if self.scope:
            return True
        else:
            return False

    def insert(self, dt, var, value):
        symbol = Symbol(dt, var, value)
        if self.contains(symbol.name):
            before = self.scope[symbol.name]
            message = "ERROR: variable '%s' of type '%s' at line %d, column %d has"
            message += " already been defined with type '%s' at line %d, column %d"
            bef_lin, bef_col = before.lexspan[0]
            aft_lin, aft_col = symbol.lexspan[0]
            data = (symbol.name, symbol.type, aft_lin, aft_col,
                    before.type, bef_lin, bef_col)
            Errors.static_error.append(message % data)
        else:
            self.scope[symbol.name] = symbol

    def delete(self, name):
        if self.contains(name):
            del self.scope[name]
        else:
            message = "ERROR: deleting non-existant '%s' in the symbol table"
            Errors.static_error.append(message % name)

    def update(self, name, value):
        if self.contains(name):
            self.scope[name].value = value
        else:
            message = "ERROR: updating non-existant '%s' in the symbol table"
            Errors.static_error.append(message % name)

    def contains(self, name):
        return name in self.scope

    def lookup(self, name):
        if self.contains(name):
            return self.scope[name]
        else:
            message = "ERROR: looking up non-existant '%s' in the symbol table"
            Errors.static_error.append(message % name)
