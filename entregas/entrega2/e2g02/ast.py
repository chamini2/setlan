#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################

#Funcion que hace la tabulacion en la impresion
def indent(level):
    return "    " * level


class Program:
    
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return "PROGRAM\n" + self.statement.print_tree(1)


# Herencia
class Statement: pass

class Assign(Statement):
    
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def print_tree(self, level):
        string =  indent(level) + "ASSIGN\n"
        string += indent(level + 1) + str(self.variable) +"\n"
        string += self.expression.print_tree(level + 1)
        return string

class Block(Statement):

    def __init__(self, statement, using=None, declarations=None,empty = None):
        self.statement = statement
        self.using = using
        self.declarations = declarations
        self.empty = empty

    def print_tree(self, level):

            string = indent(level) + "BLOCK\n"
            if self.using:
                string += indent(level + 1) + "USING\n"
                for declaration in self.declarations:
                    string += indent(level + 2) + str(declaration[0])+"\n"
                    for var in declaration[1]:
                        string += indent(level + 3) + str(var)+"\n"  
                string += indent(level + 1) + "IN" + "\n" 
            if (not(self.empty)):
                for stat in self.statement:
                    
                    string += stat.print_tree(level + 1) +'\n'
        
                string = string[:(-20 - len(indent(1)))]
                string += "BLOCK_END"
                return string
            string += "BLOCK_ENDDDD"
            return string



class Scan(Statement):

    def __init__(self, variable):
        self.variable = variable

    def print_tree(self, level):
        string = indent(level) + "SCAN\n"
        string += indent(level + 1) + "variable: " + str(self.variable)
        return string


class Print(Statement):

    def __init__(self, elements):
        self.elements = elements

    def print_tree(self, level):
        string = indent(level) + "PRINT\n"
        for elem in self.elements:
            string += elem.print_tree(level + 1) + '\n'
        return string[:-1]


class If(Statement):

    def __init__(self, condition, then_st, else_st=None):
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st

    def print_tree(self, level):
        string = indent(level) + "IF\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "instruction:\n"
        string += self.then_st.print_tree(level + 2)
        if self.else_st:
            string += '\n' + indent(level + 1) + "else:\n"
            string += self.else_st.print_tree(level + 2)
        return string

class For(Statement):

    def __init__(self, variable, direction, statement,token):
        self.variable = variable
        self.direction = direction
        self.statement = statement
        self.token     = token

    def print_tree(self, level):
        string = indent(level) + "FOR\n"
        string += indent(level + 1) + "variable: " + str(self.variable) + '\n'
        if self.token == "min":
            string += indent(level + 1) +"MIN\n"
        if self.token == "max":
            string += indent(level + 1) +"MAX\n"
        string += self.direction.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2) + '\n' 
        string +=  indent(level) +"END_FOR\n"
        return string 


class While(Statement):

    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string

class WhileRepeat(Statement):

    def __init__(self, condition, statement,statement2=None):
        self.condition = condition
        self.statement = statement
        self.statement2 = statement2

    def print_tree(self, level):
        string = indent(level) + "REPEAT\n"
        string += indent(level + 1) + "statement:\n"
        for stat in self.statement:
            string += stat.print_tree(level + 2) + '\n'
        string += indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement2.print_tree(level + 2)
        return string

class RepeatWhile(Statement):
    def __init__(self, ccondition, statement):
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "REPEAT\n"
        string += indent(level + 1) + "statement:\n"
        for stat in self.statement:
            string += stat.print_tree(level + 2) + '\n'
        string += indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        return string
# Herencia
class Expression: pass


class Variable(Expression):
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def print_tree(self, level):
        return indent(level) + "variable\n " + indent(level + 2) +str(self.name)


class Int(Expression):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "int " + str(self.value)


class Bool(Expression):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "bool " + str(self.value)


class Set(Expression):
    
    def __init__(self, values):
        self.values = values

    def print_tree(self, level):
        
        string = indent(level) +"SET\n"
        for value in self.values:
            #print value
            string += indent(level+1) + str(value) +"\n"
        # string += self.to_value.print_tree(level + 1)
        return string


class String(Expression):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)


class Binary(Expression):
    
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def print_tree(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += self.operator + '\n'
        string += self.left.print_tree(level + 2) + '\n'
        string += self.right.print_tree(level + 2)
        return string


class Unary(Expression):
    
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def print_tree(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) 
        string += str(self.operator) + '\n'
        string += indent(level + 1) + "operand:\n"
        string += self.operand.print_tree(level + 2)
        return string
