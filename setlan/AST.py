#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Abstract Syntax Tree for Setlan
Matteo Ferrando, 09-10285
"""

from sys import exit, stdout
from collections import deque
import re

import Errors
from SymbolTable import SymbolTable

scope_stack = deque()

def indent(n):
    return n * '    '

###############################################################################


class Program(object):
    """A program consists of running a statement"""
    def __init__(self, lexspan, statement):
        self.lexspan = lexspan
        self.statement = statement

    def __str__(self):
        return "PROGRAM" + self.statement.pretty_string(1)

    def check(self):
        pass

    def execute(self):
        pass

###############################################################################


# For inheritance
# in the .check() method, statements return booleans values
class Statement(object): pass


# def error_invalid_expression(exp_type, place, place_string, should):
#     if exp_type != should and exp_type is not None:
#         message = "ERROR: expression of type '%s' in %s "
#         message += "(must be '%s') from line %d, column %d"
#         message += " to line %d, column %d"
#         s_lin, s_col = place.lexspan[0]
#         e_lin, e_col = place.lexspan[1]
#         data = exp_type, place_string, should, s_lin, s_col, e_lin, e_col
#         static_error.append(message % data)
#         return False
#     elif exp_type is None:
#         return False
#     else:
#         return True

###############################################################################


class Assign(Statement):
    """The assign statement"""
    def __init__(self, lexspan, variable, expression):
        self.lexspan = lexspan
        self.variable = variable
        self.expression = expression
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "ASSIGN"
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "value"
        string += self.expression.pretty_string(level + 2)
        return string

    def check(self):
        pass

###############################################################################


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    def __init__(self, lexspan, statements, declarations):
        self.lexspan = lexspan
        self.statements = statements
        self.sym_table = SymbolTable()
        if declarations:
            for dt, var in declarations:
                new_dt = Type.type_from_string(dt)
                self.sym_table.insert(new_dt, var, default_value(new_dt))

    def pretty_string(self, level):
        string = "\n" + indent(level) + "BLOCK"

        if self.sym_table:
            string += "\n" + indent(level + 1) + "USING"

            for sym in self.sym_table:
                string += "\n" + indent(level + 2) + Type.string_from_type(sym.type)
                string += " " + str(sym.name)

            string += "\n" + indent(level + 1) + "IN"

        for stat in self.statements:
            string += stat.pretty_string(level + 1)

        string += "\n" + indent(level) + "BLOCK_END"
        return string

    def check(self):
        scope_stack.appendleft(self.sym_table)

###############################################################################


class Scan(Statement):
    """Scan statement, for user input"""
    def __init__(self, lexspan, variable):
        self.lexspan = lexspan
        self.variable = variable
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "SCAN"
        string += self.variable.pretty_string(level + 1)
        return string

    def check(self):
        pass

###############################################################################


class Print(Statement):
    """Print statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        self.lexspan = lexspan
        self.elements = elements
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "PRINT"
        string += "\n" + indent(level + 1) + "elements"

        for elm in self.elements:
            string += elm.pretty_string(level + 2)

        return string

    def check(self):
        pass

###############################################################################


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "IF"

        string += "\n" + indent(level + 1) + "condition"
        string += self.condition.pretty_string(level + 2)

        string += "\n" + indent(level + 1) + "THEN"
        string += self.then_st.pretty_string(level + 2)

        if self.else_st:
            string += "\n" + indent(level + 1) + "ELSE"
            string += self.else_st.pretty_string(level + 2)

        return string

    def check(self):
        pass

###############################################################################


class For(Statement):
    """For statement, works with sets"""
    def __init__(self, lexspan, variable, direction, in_set, statement):
        self.lexspan = lexspan
        self.variable = variable
        self.direction = Direction.direction_from_string(direction)
        self.in_set = in_set
        self.statement = statement
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "FOR"
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "direction"
        string += "\n" + indent(level + 2) + Direction.string_from_direction(self.direction)
        string += "\n" + indent(level + 1) + "IN"
        string += self.in_set.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "DO"
        string += self.statement.pretty_string(level + 2)

        return string

    def check(self):
        pass

###############################################################################


class While(Statement):
    """While statement"""
    def __init__(self, lexspan, repeat_st, condition, do_st):
        self.lexspan = lexspan
        self.repeat_st = repeat_st
        self.condition = condition
        self.do_st = do_st
        # self.sym_table = None

    def pretty_string(self, level):
        string = ""
        if self.repeat_st:
            string += "\n" + indent(level) + "REPEAT"
            string += self.repeat_st.pretty_string(level + 1)

        string += "\n" + indent(level) + "WHILE"
        string += "\n" + indent(level + 1) + "condition"
        string += self.condition.pretty_string(level + 2)

        if self.do_st:
            string += "\n" + indent(level) + "DO"
            string += self.do_st.pretty_string(level + 1)

        return string

    def check(self):
        pass

###############################################################################


# For inheritance
# in the .check() method, expressions return the data type or None
class Expression(object): pass

# For inheritance
class Direction(object):
    MinD, MaxD = range(2)

    def pretty_string(self, level, num):
        return "\n" + indent(level) + string_from_direction(num)

    @staticmethod
    def direction_from_string(str):
        if str == "min":
            return Direction.MinD
        if str == "max":
            return Direction.MaxD

    @staticmethod
    def string_from_direction(num):
        if num == Direction.MinD:
            return "min"
        if num == Direction.MaxD:
            return "max"

def default_value(data_type):
    if data_type == Type.IntT:
        return 0
    if data_type == Type.BoolT:
        return False
    if data_type == Type.SetT:
        return []

# For inheritance
# just for checking the type of an exprssion.
class Type(object):
    IntT, SetT, BoolT, StringT, VariableT, BinaryT, UnaryT = range(7)

    def pretty_string(self, level, num):
        return "\n" + indent(level) + type_from_string(num)

    @staticmethod
    def string_from_type(num):
        if num == Type.IntT:
            return "int"
        if num == Type.SetT:
            return "set"
        if num == Type.BoolT:
            return "bool"
        if num == Type.StringT:
            return "string"
        if num == Type.VariableT:
            return "variable"
        if num == Type.BinaryT:
            return "binary"
        if num == Type.UnaryT:
            return "unary"

    @staticmethod
    def type_from_string(str):
        if str.lower() == "int":
            return Type.IntT
        if str.lower() == "set":
            return Type.SetT
        if str.lower() == "bool":
            return Type.BoolT
        if str.lower() == "string":
            return Type.StringT
        if str.lower() == "variable":
            return Type.VariableT
        if str.lower() == "binary":
            return Type.BinaryT
        if str.lower() == "unary":
            return Type.UnaryT

    # def pretty_string(self, level):
    #     return "\n" + indent(level) + self.__class__.__name__[:-5].lower()

###############################################################################


# For inheritance
class Literal(Expression):

    def check(self):
        return self.type

###############################################################################


class Variable(Literal):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
        self.type = Type.VariableT
        self.lexspan = lexspan
        self.name = name
        self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        string += "\n" + indent(level + 1) + str(self)
        return string

    def check(self):
        table_info = None
        for scope in scope_stack:
            if scope.contains(self.name):
                table_info = scope.lookup(self.name)
                break

        if table_info is None:
            message = "ERROR: variable '%s' referenced in line %d, column %d is not defined"
            lin, col = self.lexspan[0]
            data = self.name, lin, col
            Errors.static_error.append(message % data)
        else:
            return table_info.type

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

###############################################################################


class Int(Literal):
    """Class to define an expression of int"""
    def __init__(self, lexspan, value):
        self.type = Type.IntT
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        string += "\n" + indent(level + 1) + str(self.value)
        return string

    def __str__(self):
        return str(self.value)

    def evaluate(self):
        return self.value

#######################################


class Bool(Literal):
    """Class to define an expression of bool"""
    def __init__(self, lexspan, value):
        self.type = Type.BoolT
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        string += "\n" + indent(level + 1) + str(self.value).lower()
        return string

    def __str__(self):
        return str(self.value)

    def evaluate(self):
        return eval(self.value.title())

#######################################


class Set(Literal):
    """Class to define an expression of range"""
    def __init__(self, lexspan, value):
        self.type = Type.SetT
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        for elm in self.value:
            string += elm.pretty_string(level + 1)
        return string

#######################################


class String(Literal):
    """Class to define an expression of a printable string"""
    def __init__(self, lexspan, value):
        self.type = Type.StringT
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        string += "\n" + indent(level + 1) + str(self)
        return string

    def check(self):
        pass

    def __str__(self):
        return self.value

    def check(self):
        return self.type

    def evaluate(self):
        return self.value

###############################################################################


def error_overflow(lexspan, operator):
    message = "ERROR: overflow in '%s' operation, "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), s_lin, s_col, e_lin, e_col
    print '\n\n', message % data
    exit()

def error_division_by_zero(lexspan, operator):
    message = "ERROR: division by zero with in '%s' operation, "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), s_lin, s_col, e_lin, e_col
    print '\n\n', message % data
    exit()

def error_unsuported_binary(lexspan, operator, left, right):
    message = "ERROR: unsupported operator '%s' for types '%s' and '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(left), str(right), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)

class Binary(Expression):
    """Binary expressions"""
    def __init__(self, lexspan, operator, left, right):
        self.type = Type.BinaryT
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.left = left
        self.right = right
        self.sym_table = None

    def __str__(self):
        string = '(' + str(self.left) + str(self.operator) 
        string += '  ' + str(self.right) + ')'
        return string

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.upper() 
        string += " " + str(self.operator)
        string += self.left.pretty_string(level + 1)
        string += self.right.pretty_string(level + 1)
        return string

###############################################################################


class Plus(Binary):
    """Binary expressions with a '+'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "+", left, right)

#######################################


class Minus(Binary):
    """Binary expressions with a '-'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "-", left, right)

#######################################


class Times(Binary):
    """Binary expressions with a '*'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "*", left, right)

#######################################


class Divide(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/", left, right)

#######################################


class Modulo(Binary):
    """Binary expressions with a '%'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "%", left, right)

#######################################

class Union(Binary):
    """Binary expressions with a '++'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "++", left, right)

#######################################


class Difference(Binary):
    """Binary expressions with a '\\'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "\\", left, right)

#######################################


class Intersection(Binary):
    """Binary expressions with a '><'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "><", left, right)

#######################################

class SetPlus(Binary):
    """Binary expressions with a '<+>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<+>", left, right)

#######################################


class SetMinus(Binary):
    """Binary expressions with a '<->'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<->", left, right)

#######################################


class SetTimes(Binary):
    """Binary expressions with a '<*>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<*>", left, right)

#######################################


class SetDivide(Binary):
    """Binary expressions with a '</>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "</>", left, right)

#######################################


class SetModulo(Binary):
    """Binary expressions with a '<%>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<%>", left, right)

#######################################

class Or(Binary):
    """Binary expressions with a 'or'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "or", left, right)

#######################################


class And(Binary):
    """Binary expressions with a 'and'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "and", left, right)

#######################################


class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<", left, right)

#######################################


class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<=", left, right)

#######################################


class Greater(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">", left, right)

#######################################


class GreaterEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">=", left, right)

#######################################


class Equal(Binary):
    """Binary expressions with a '=='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "==", left, right)

#######################################


class Unequal(Binary):
    """Binary expressions with a '/='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/=", left, right)

#######################################


class Contains(Binary):
    """Binary expressions with a '@'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "@", left, right)

###############################################################################


def error_unsuported_unary(lexspan, operator, operand):
    message = "ERROR: unsupported operator '%s' for type: '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(operand), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)


class Unary(Expression):
    """Unary expressions"""
    def __init__(self, lexspan, operator, operand):
        self.type = Type.UnaryT
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.operand = operand
        self.sym_table = None

    def __str__(self):
        string = '(' + str(self.operator) + ' ' + str(self.operand) + ')'
        return string

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.upper() 
        string += " " + str(self.operator)
        string += self.operand.pretty_string(level + 1)
        return string

###############################################################################


class Negate(Unary):
    """Unary expressions with a '-'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "-", operand)

#######################################


class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "not", operand)

#######################################


class Max(Unary):
    """Unary expressions with a '>?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, ">?", operand)

#######################################


class Min(Unary):
    """Unary expressions with a '<?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "<?", operand)

#######################################


class Size(Unary):
    """Unary expressions with a '$?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "$?", operand)
