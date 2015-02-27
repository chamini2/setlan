#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################


# Funcion que hace la tabulacion en la impresion
def indent(level):
    return "    " * level

class Table(object):
    def __init__(self):
        self.scope = {}
        self.outer = None

    def __iter__(self):
        return iter(self.scope)

    def __str__(self):
        return self.print_tree(0)

    def __nonzero__(self):
        if self.outer:
            return True
        if self.scope:
            return True
        else:
            return False

    def print_tree(self, level):
        self.vInt = 0
        self.vBool = False
        self.vSet = {}

        string = indent(level) + "SCOPE\n"
        for var in self.scope:
            sym = self.scope[var]
            string += indent(level + 1) + str(sym) 
            aux = len(str(sym)) -2
            if (str(sym)[aux] == "N"):
                string += " | value : "+str(self.vInt)+'\n'
            elif (str(sym)[aux] == "O"):
                string += "| value : "+str(self.vBool)+'\n'
            elif (str(sym)[aux] == "E"):
                string += " | value : "+str(self.vSet)+'\n'
      #  string += indent(level) + "END_SCOPE\n"
        return string[:-1]

    def insert(self, key, data_type, protected=False):
        if not self.is_local(key):
            self.scope[key] = Symbol(key.lexspan, key.name,
                                     data_type, protected)
        else:
            print key.name + " ya fue tomada en el scope"

    def delete(self, key):
        if key in self.scope:
            del self.scope[key]
        else:
            print "Table.delete: No '" + key.name + "' en el scope"

    def update(self, key, data_type, value):
        if self.is_member(key):
            if key in self.scope:
                symbol = self.scope[key]

                if data_type == symbol.data_type:
                    symbol.value = value
                    self.scope[key] = symbol
                    return True
                else:
                    print "Table.update: Different data types"
                    return False
            else:
                return self.outer.update(key, data_type, value)
        else:
            print "Table.update: No " + key.name + " in scope"
            return False

    def contains(self, key):
        return self.scope[key]

    def is_local(self, key):
        if self.scope:
            if key in self.scope:
                return True
        return False

    def lookup(self, key):
        if key in self.scope:
            return self.scope[key]
        else:
            if self.outer:
                return self.outer.lookup(key)
        print "Table.lookup: " + key.name + " no esta en scope"


class Symbol(object):
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
        return "Variable : "+self.name + " | type "+value + ' : ' + self.data_type + protected
