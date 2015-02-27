#!/usr/bin/env python
# -*- coding: utf-8 -*-

####
#CI3725 - Etapa 1 - Análisis Lexicográfico
#Fabio, Castro, 10-10132
#Antonio, Scaramazza 11-10957
####


# Obtener identacion
def indent(level):
    return "    " * level


class SymTable(object):
    """Representacion de una tabla de simbolos en una tabla de simbolos"""
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

    def print_tree(self, level):
        string = ""
        for var in self.scope:
            sym = self.scope[var]
            string += indent(level+1) + sym.print_tree() + '\n'
        return string

    def print_symtab(self, level):
        string = ""
        for var in self.scope:
            sym = self.scope[var]
            string += indent(level+1) + str(sym) + '\n'
        return string

    def insert(self, key, data_type):
        if not self.is_local(key):
            self.scope[key] = Symbol(key.lexspan, key.name,
                                     data_type)
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
    """Simbolos de la tabla"""
    def __init__(self, lexspan, name, data_type, value=None):
        super(Symbol, self).__init__()
        self.lexspan = lexspan
        self.name = name
        self.data_type = data_type
        if(data_type == "INT"):
            self.value=0
        if(data_type == "SET"):
            self.value=[]
        if(data_type == "BOOL"):
            self.value = False

    def print_tree(self):
            return str(self.data_type).lower() + " " + self.name         

    def __str__(self):
        if self.value:
            value = " = " + self.value
        else:
            value = ""
        if self.data_type != "SET":
            return "Variable: " + self.name + ' | Type: ' + str(self.data_type).lower() + " | Value:" + str(self.value)
        else:
            string = "Variable: " + self.name + ' | Type: ' + str(self.data_type).lower() + " | Value:" + str("{") 
            for i in self.value:
                j+=1
                if j > 1:
                    string+=","
                string += str(i) 

            string +=str("}")
            return string
       