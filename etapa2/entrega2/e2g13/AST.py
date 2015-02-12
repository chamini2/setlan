# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
'''

class Expre:
    
    def get_indent_number(self,level):
        return level * 4
    
    def get_ident_str(self,level):
        return self.get_indent_number(level) * r" "
    
    def print_with_indent(self,cad,level):
        print self.get_ident_str(level) + cad
        
class Program(Expre):
    
    def __init__(self, statement):
        self.type = "PROGRAM"
        self.statement = statement
        
    def print_tree(self,level = 0):
        self.print_with_indent(self.type, level)
        self.statement.print_tree(level + 1)

class Scan(Expre):
    
    def __init__(self,id_):
        self.type = 'SCAN'
        self.var_to_read = id_
    
    def print_tree(self , level):
        self.print_with_indent(self.type,level)
        self.var_to_read.print_tree(level + 1)
    
class Assign(Expre):
    
    def __init__(self, identifier,expresion):
        self.type = "ASSIGN"
        self.id = identifier
        self.expresion = expresion
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent('identifier' ,level+ 1)
        self.print_with_indent(self.id,level+ 2)
        self.print_with_indent('value',level + 1)
        self.expresion.print_tree(level + 2)

class If(Expre):
    
    def __init__(self,condition,statement_if, statement_else = None):
        self.type = 'IF'
        self.condition = condition
        self.statement_if   = statement_if
        self.statement_else = statement_else
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent("condition",level+1)
        self.condition.print_tree(level + 2)
        
        self.print_with_indent('THEN', level+1)
        self.statement_if.print_tree(level + 2)
        
        if self.statement_else is not None:
            self.print_with_indent('ELSE',level)
            self.statement_else.print_tree(level + 1)

class For(Expre):
    
    def __init__(self,identifier,direction, expression , statement):
        self.type = 'FOR'
        self.identifier = identifier
        self.direction  = direction
        self.expression = expression
        self.statement  = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.identifier.print_tree(level + 1)
        self.direction.print_tree(level + 1)
        
        self.print_with_indent('IN',level + 1)
        self.expression.print_tree(level + 1)

        self.print_with_indent('DO',level + 1)
        self.statement.print_tree(level + 2)

class RepeatWhileDo(Expre):
    
    def __init__(self,statement1,expression,statement2):
        self.type = 'REPEAT'
        self.statement1 = statement1
        self.expression  = expression
        self.statement2 = statement2
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.statement1.print_tree(level + 1)
        
        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement2.print_tree(level + 1)

class WhileDo(Expre):
    
    def __init__(self,expression,statement):
        self.type = 'WHILE'
        self.expression  = expression
        self.statement = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement.print_tree(level + 1)

class RepeatWhile(Expre):
    
    def __init__(self,statement,expression):
        self.type = 'REPEAT'
        self.statement = statement
        self.expression  = expression
        
    def print_tree(self,level): 
        self.print_with_indent(self.type,level)
        self.statement.print_tree(level + 1)

        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

class Print(Expre):
    
    def __init__(self,type_print,lista_to_print):
        self.type = type_print.upper()
        self.lista_to_print = lista_to_print
        
    def print_tree(self,level): 
        self.print_with_indent(self.type, level)
        self.print_with_indent("elements",level + 1)
        for var in self.lista_to_print:
            var.print_tree(level + 2)

class Block(Expre):
    
    def __init__(self, list_st,declare = None): 
        self.type = "BLOCK"
        self.list_st = list_st
        self.declare = declare
    
    def print_tree(self,level):
        self.print_with_indent(self.type, level)
        
        if self.declare is not None:
            self.declare.print_tree(level + 1)

        for stat in self.list_st:
            stat.print_tree(level + 1)
            
        self.print_with_indent("BLOCK_END", level)

class Parenthesis(Expre):
    
    def __init__(self, expre):
        self.type = 'PARENTHESIS'
        self.condition = expre        
            
    def print_tree(self,level):  
        self.print_with_indent(self.type , level)
        self.condition.print_tree(level + 1)
    
class BinaryOP(Expre):
    
    def __init__(self,expre1,type_op,expre2):
        self.expre1  = expre1
        self.type_op = type_op
        self.expre2  = expre2
        
    def print_tree(self,level):  
        self.print_with_indent(self.type_op, level)
        self.expre1.print_tree(level + 1)
        self.expre2.print_tree(level + 1)

class UnaryOP(Expre):
    
    def __init__(self, type_op,expre1):
        self.type_op = type_op
        self.expre1  = expre1
            
    def print_tree(self,level):   
        self.print_with_indent(self.type_op , level)
        self.expre1.print_tree(level + 1)
    
class DeclareList(Expre):
    
    def __init__(self,declared_list):
        self.declared_list = declared_list
        
    def print_tree(self,level): 
        self.print_with_indent('USING', level)
        for declaration_vars in self.declared_list:
            declaration_vars.print_tree(level)
        self.print_with_indent('IN', level)

class TypeList(Expre):
    
    def __init__(self,data_type,id_list):
        self.data_type = data_type
        self.id_list = id_list
    
    def print_tree(self,level):

        for identifier in self.id_list:
            self.print_with_indent(self.data_type + ' ' + identifier,level + 1)
            
class Direction(Expre):
    
    def __init__(self,value):
        self.type = 'direction'
        self.value = value
        
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

class Set(Expre):
    
    def __init__(self, list_st): 
        self.type = 'set'
        self.list_st = list_st
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)

        for exp in self.list_st:
            exp.print_tree(level + 1)
            
class Bool(Expre):
    
    def __init__(self , value):
        self.type = 'bool'
        self.value = value
    
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

class Integer(Expre):
    
    def __init__(self , value):
        self.type = 'int'
        self.value = value
    
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(str(self.value), level + 1)

class String(Expre):
    
    def __init__(self , value):     
        self.type = 'string'
        self.value = value
    
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

class Identifier(Expre):
    
    def __init__(self , value):       
        self.type = 'identifier'
        self.value = value
    
    def print_tree(self , level):       
        self.print_with_indent(self.type  , level )
        self.print_with_indent(self.value , level + 1 )
