# -*- coding: utf-8 -*-
'''
Created on 16/2/2015

@author: David Klie
@author : Gustavo Benzecri
'''
symbol_err=[]
from copy import deepcopy
def tab(level):
    return('    '*level)
class SymbolTableStack(object):

    def __init__(self):
        self.scope = 0
        self.table_stack = []

    def add_symbol_table(self,table):
        # Crea una tabla de simbolos y se agrega a la pila de tablas
        # Aumenta el alcance por 1
        self.table_stack.insert(0, table)
        self.scope+=1
        
    def delete_symbol_table(self):
        # Borra la ultima tabla agregada de la pila de tablas
        # Baja el alcance por 1
        # Se imprime la tabla antes de destruirse
        self.scope-=1
        return self.table_stack.pop(0)
        
class SymbolTable(object):
    
    default={
        'int': 0,
        'set': set(),
        'bool': False
    }
    
    def __init__(self):
        self.table = {} # Empty dictionary
        
    def insert(self, identifier, type_var,line_col, value = None,iterator=False):
        if not identifier in self.table:
            if not value:
                value=SymbolTable.default.get(type_var)
                if value==None:
                    symbol_err.append('ERROR: type must be bool, set or int')
                else:
                    self.table[identifier]=[type_var,deepcopy(value)]
            else:
                self.table[identifier]=[type_var,depcopy(value)]
            if iterator:
                self.table[identifier]+=[iterator]
        else:
            symbol_err.append('ERROR at line %s column %s in USING statement: variable %s is already defined'\
            %(line_col[0],line_col[1],identifier))

    def delete(self, identifier):
        del self.table[identifier]
    
    def update(self, identifier, updated_value):
        if (identifier in self.table):
            self.table[identifier][1]=updated_value
    
    def contains(self, identifier):
        return identifier in self.table
    
    def lookup(self, identifier):
        return self.table.get(identifier)
    
    def showTable(self,level):
        string=tab(level)+'SCOPE\n'
        for i in self.table.items():
            string+='%sVariable: %s | Type: %s | Value: %s\n' % (tab(level+1),i[0],i[1][0],i[1][1])
        return string
            
    