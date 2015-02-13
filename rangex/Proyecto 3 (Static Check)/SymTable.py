#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Symbol Table for RangeX Language
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285
"""


# To set indentation automatically
def indent(level):
    return "    " * level


class SymTable(object):
    """Representation of a SymTable in the Symbol Table."""
    def __init__(self):
        self.scope = {}
        self.outer = None

    def __iter__(self):
        return iter(self.scope)

    def __str__(self):
        return self.tree_string(0)

    def __nonzero__(self):
        if self.outer:
            return True
        if self.scope:
            return True
        else:
            return False

    def tree_string(self, level):
        string = indent(level) + "SCOPE\n"
        for var in self.scope:
            sym = self.scope[var]
            string += indent(level + 1) + str(sym) + '\n'
        return string[:-1]

    def insert(self, key, data_type, protected=False):
        if not self.is_local(key):
            self.scope[key] = Symbol(key.lexspan, key.name,
                                     data_type, protected)
        else:
            print key.name + " already in scope"

    def delete(self, key):
        if key in self.scope:
            del self.scope[key]
        else:
            print "SymTable.delete: No '" + key.name + "' in scope"

    def update(self, key, data_type, value):
        if self.is_member(key):
            if key in self.scope:
                symbol = self.scope[key]

                if data_type == symbol.data_type:
                    symbol.value = value
                    self.scope[key] = symbol
                    return True
                else:
                    print "SymTable.update: Different data types"
                    return False
            else:
                return self.outer.update(key, data_type, value)
        else:
            print "SymTable.update: No " + key.name + " in scope"
            return False

    def is_member(self, key):
        if self.scope:
            if key in self.scope:
                return True
        if self.outer:
            return self.outer.is_member(key)
        return False

    def is_local(self, key):
        if self.scope:
            if key in self.scope:
                return True
        return False

    def find(self, key):
        if key in self.scope:
            return self.scope[key]
        else:
            if self.outer:
                return self.outer.find(key)
        print "SymTable.find: " + key.name + " not in scope"


class Symbol(object):
    """A Symbol of the Symbol Table"""
    def __init__(self, lexspan, name, data_type, protected, value=None):
        super(Symbol, self).__init__()
        self.lexspan = lexspan
        self.name = name
        self.data_type = data_type
        self.protected = protected
        self.value = value

    def __str__(self):
        if self.protected:
            protected = ", protected"
        else:
            protected = ""
        if self.value:
            value = " = " + self.value
        else:
            value = ""
        return self.name + value + ' : ' + self.data_type + protected
