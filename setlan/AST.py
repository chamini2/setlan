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

###############################################################################

scope_stack = deque()

def lookup_stack(name, lexspan):
    table_info = None
    for scope in scope_stack:
        if scope.contains(name):
            table_info = scope.lookup(name)
            break

    if table_info is None:
        message = "ERROR: variable '%s' referenced at line %d, column %d is not defined"
        lin, col = lexspan[0]
        data = name, lin, col
        Errors.static_error.append(message % data)

    return table_info

def update_stack(name, value):
    for scope in scope_stack:
        if scope.contains(name):
            break
    scope.update(name, value)

###############################################################################

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
        self.statement.check()

    def execute(self):
        self.statement.execute()

###############################################################################


# For inheritance
# in the .check() method, statements return booleans values
class Statement(object): pass

def error_expression_type(exp_type, got_type, lexspan):
    if got_type != Type.ErrorT:
        message = "ERROR: expecting expression of type '%s' and got"
        message += " type '%s' at line %d, column %d"
        lin, col = lexspan[0]
        data = exp_type, got_type, lin, col
        Errors.static_error.append(message % data)

###############################################################################


class Assign(Statement):
    """The assign statement"""
    def __init__(self, lexspan, variable, expression):
        self.lexspan = lexspan
        self.variable = variable
        self.expression = expression

    def pretty_string(self, level):
        string = "\n" + indent(level) + "ASSIGN"
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "value"
        string += self.expression.pretty_string(level + 2)
        return string

    def check(self):
        exp_type = self.expression.check()
        table_info = lookup_stack(self.variable.name, self.variable.lexspan)

        if table_info:
            var_type = table_info.type
            if var_type == Type.IteratorT:
                message = "ERROR: assigning value to not modifiable variable "
                message += "'%s' at line %d, column %d"
                lin, col = self.lexspan[0]
                data = table_info.name, lin, col
                Errors.static_error.append(message % data)

                var_type = Type.IntT

            if Type.ErrorT != exp_type != var_type:
                message = "ERROR: assigning expression of type '%s' to variable "
                message += "'%s' of type '%s' at line %d, column %d"
                lin, col = self.lexspan[0]
                data = exp_type, table_info.name, table_info.type, lin, col
                Errors.static_error.append(message % data)

    def execute(self):
        exp_value = self.expression.evaluate()
        update_stack(self.variable.name, exp_value)

###############################################################################


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    def __init__(self, lexspan, statements, declarations):
        self.lexspan = lexspan
        self.statements = statements
        self.sym_table = SymbolTable()
        for dt, var in declarations:
            new_dt = Type.type_from_string(dt)
            self.sym_table.insert(new_dt, var, Type.default_value(new_dt))

    def pretty_string(self, level):
        string = "\n" + indent(level) + "BLOCK"

        if self.sym_table:
            string += "\n" + indent(level + 1) + "USING"

            for sym in self.sym_table:
                string += "\n" + indent(level + 2) + str(sym.type)
                string += " " + str(sym.name)

            string += "\n" + indent(level + 1) + "IN"

        for stat in self.statements:
            string += stat.pretty_string(level + 1)

        string += "\n" + indent(level) + "BLOCK_END"
        return string

    def check(self):
        scope_stack.appendleft(self.sym_table)
        for stat in self.statements:
            stat.check()
        scope_stack.popleft()

    def execute(self):
        scope_stack.appendleft(self.sym_table)
        for stat in self.statements:
            stat.execute()
        scope_stack.popleft()

###############################################################################


class Scan(Statement):
    """Scan statement, for user input"""
    def __init__(self, lexspan, variable):
        self.lexspan = lexspan
        self.variable = variable

    def pretty_string(self, level):
        string = "\n" + indent(level) + "SCAN"
        string += self.variable.pretty_string(level + 1)
        return string

    def check(self):
        table_info = lookup_stack(self.variable.name, self.variable.lexspan)
        if table_info and table_info.type not in [Type.IntT, Type.BoolT]:
            message = "ERROR: scanning variable '%s' of type '%s' at"
            message += " line %d, column %d"
            lin, col = self.lexspan[0]
            data = table_info.name, table_info.type, lin, col
            Errors.static_error.append(message % data)

    def execute(self):
        def scan_int():
            raw = raw_input()
            match = re.match(r'^\s*-?\s*\d+\s*$', raw)

            if match:
                value = int(match.group())
                if -2147483648 <= value <= 2147483647:
                    return value

                print "\nERROR: expecting an int value, overflow, try again."
                return scan_int()

            print "\nERROR: expecting an int value, try again."
            return scan_int()

        def scan_bool():
            raw = raw_input()
            true_match = re.match(r'^\s*true\s*$', raw)
            false_match = re.match(r'^\s*false\s*$', raw)

            if true_match:
                return True
            elif false_match:
                return False

            print "\nERROR: expecting a bool value, try again."
            return scan_bool()

        table_info = lookup_stack(self.variable.name, self.variable.lexspan)

        if table_info.type == Type.IntT:
            scan_value = scan_int()
        elif table_info.type == Type.BoolT:
            scan_value = scan_bool()

        update_stack(self.variable.name, scan_value)

###############################################################################


class Print(Statement):
    """Print statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        self.lexspan = lexspan
        self.elements = elements

    def pretty_string(self, level):
        string = "\n" + indent(level) + "PRINT"
        string += "\n" + indent(level + 1) + "elements"

        for elm in self.elements:
            string += elm.pretty_string(level + 2)

        return string

    def check(self):
        for elm in self.elements:
            elm.check()

    def execute(self):
        for elm in self.elements:
            elm_value = elm.evaluate()

            if isinstance(elm_value, bool):
                stdout.write(str(elm_value).lower())

            elif isinstance(elm_value, int):
                stdout.write(str(elm_value))

            elif isinstance(elm_value, str):
                stdout.write(eval(elm_value))

            elif isinstance(elm_value, set):
                elm_value = sorted(elm_value)
                # intersperse
                elm_value = sum([[x, ", "] for x in elm_value],[])[:-1]

                stdout.write("{ ")
                for e in elm_value:
                    stdout.write( str(e) )
                stdout.write(" }")

###############################################################################


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st

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
        condition_type = self.condition.check()

        if condition_type != Type.BoolT:
            error_expression_type(Type.BoolT, condition_type, self.condition.lexspan)

        self.then_st.check()
        if self.else_st:
            self.else_st.check()

    def execute(self):
        if self.condition.evaluate():
            self.then_st.execute()
        elif self.else_st:
            self.else_st.execute()

###############################################################################


class For(Statement):
    """For statement, works with sets"""
    def __init__(self, lexspan, variable, direction, in_set, statement):
        self.lexspan = lexspan
        self.direction = Direction.direction_from_string(direction)
        self.in_set = in_set
        self.statement = statement

        self.variable = variable
        self.sym_table = SymbolTable()
        self.sym_table.insert(Type.IteratorT, variable, Type.default_value(Type.IntT))

    def pretty_string(self, level):
        string = "\n" + indent(level) + "FOR"
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "direction"
        string += "\n" + indent(level + 2) + str(self.direction)
        string += "\n" + indent(level + 1) + "IN"
        string += self.in_set.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "DO"
        string += self.statement.pretty_string(level + 2)

        return string

    def check(self):
        in_type = self.in_set.check()

        if in_type != Type.SetT:
            error_expression_type(Type.SetT, in_type, self.in_set.lexspan)

        scope_stack.appendleft(self.sym_table)
        self.statement.check()
        scope_stack.popleft()

    def execute(self):
        in_value = self.in_set.evaluate()

        if self.direction == Direction.MinD:
            in_value = sorted(in_value)
        else:
            in_value = sorted(in_value, reverse=True)

        scope_stack.appendleft(self.sym_table)
        for elm in in_value:
            update_stack(self.variable.name, elm)
            self.statement.execute()
        scope_stack.popleft()

###############################################################################


class While(Statement):
    """While statement"""
    def __init__(self, lexspan, repeat_st, condition, do_st):
        self.lexspan = lexspan
        self.repeat_st = repeat_st
        self.condition = condition
        self.do_st = do_st

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
        if self.repeat_st:
            self.repeat_st.check()

        condition_type = self.condition.check()
        if condition_type != Type.BoolT:
            error_expression_type(Type.BoolT, condition_type, self.condition.lexspan)

        if self.do_st:
            self.do_st.check()

    def execute(self):
        if self.repeat_st: 
            self.repeat_st.execute()
        while self.condition.evaluate():
            if self.do_st: 
                self.do_st.execute()
            if self.repeat_st: 
                self.repeat_st.execute()

###############################################################################


class Enum(object):
    def __init__(self, cl, value, string):
        self.cl = cl
        self.value = value
        self.string = string

    def __eq__(self, other):
        return self.cl == other.cl and self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value

    def __str__(self):
        return self.string

# For inheritance
class Direction(object):
    MinD = Enum("Direction", 1, "min")
    MaxD = Enum("Direction", 2, "max")

    def pretty_string(self, level, num):
        return "\n" + indent(level) + str(num)

    @staticmethod
    def direction_from_string(string):
        if string == "min":
            return Direction.MinD
        if string == "max":
            return Direction.MaxD

# For inheritance
# just for checking the type of an exprssion.
class Type(object):
    IntT      = Enum("Type", 1, "int")
    IteratorT = Enum("Type", 2, "int")
    SetT      = Enum("Type", 3, "set")
    BoolT     = Enum("Type", 4, "bool")
    StringT   = Enum("Type", 5, "string")
    VariableT = Enum("Type", 6, "variable")
    BinaryT   = Enum("Type", 7, "binary")
    UnaryT    = Enum("Type", 8, "unary")
    ErrorT    = Enum("Type", 9, "error")

    def pretty_string(self, level, dt):
        return "\n" + indent(level) + str(dt)

    @staticmethod
    def type_from_string(string):
        if string == "int":
            return Type.IntT      
        if string == "set":
            return Type.SetT      
        if string == "bool":
            return Type.BoolT     
        if string == "string":
            return Type.StringT   
        if string == "variable":
            return Type.VariableT 
        if string == "binary":
            return Type.BinaryT   
        if string == "unary":
            return Type.UnaryT    
        if string == "error":
            return Type.ErrorT    

    @staticmethod
    def default_value(data_type):
        if data_type == Type.IntT:
            return 0
        if data_type == Type.BoolT:
            return False
        if data_type == Type.SetT:
            return set()

###############################################################################


# For inheritance
# in the .check() method, expressions return the data type or None
class Expression(object): pass

###############################################################################


# For inheritance
class Literal(Expression):

    def check(self):
        return self.type

    def evaluate(self):
        return self.value

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        string += "\n" + indent(level + 1) + str(self)
        return string


###############################################################################


class Variable(Literal):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
        self.type = Type.VariableT
        self.lexspan = lexspan
        self.name = name

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

    def check(self):
        table_info = lookup_stack(self.name, self.lexspan)
        if table_info:
            return table_info.type
        else:
            return Type.ErrorT

    def evaluate(self):
        table_info = lookup_stack(self.name, self.lexspan)
        return table_info.value        

###############################################################################


class Int(Literal):
    """Class to define an expression of int"""
    def __init__(self, lexspan, value):
        self.type = Type.IntT
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value)

#######################################


class Bool(Literal):
    """Class to define an expression of bool"""
    def __init__(self, lexspan, value):
        self.type = Type.BoolT
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value).lower()

#######################################


class Set(Literal):
    """Class to define an expression of range"""
    def __init__(self, lexspan, value):
        self.type = Type.SetT
        self.lexspan = lexspan
        self.value = value

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.lower()
        for elm in self.value:
            string += elm.pretty_string(level + 1)
        return string

    def check(self):
        for elm in self.value:
            elm_type = elm.check()
            if elm_type != Type.IntT:
                error_expression_type(Type.IntT, elm_type, elm.lexspan)
        return Type.SetT

    def evaluate(self):
        values = set()
        for elm in self.value:
            values.add(elm.evaluate())
        return values

#######################################


class String(Literal):
    """Class to define an expression of a printable string"""
    def __init__(self, lexspan, value):
        self.type = Type.StringT
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return self.value

###############################################################################


# how = overflow
# how = division by zero
# how = max/min empty set
def error_dynamic(how, lexspan):
    message = "ERROR: " + how + " in operation at line %d, column %d"
    lin, col = lexspan[0]
    data = lin, col
    print '\n\n', message % data
    exit()

class Binary(Expression):
    """Binary expressions"""
    def __init__(self, lexspan, operator, operation, left, right, operand_types, return_type):
        self.type = Type.BinaryT
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.operation = operation
        self.left = left
        self.right = right
        self.operand_types = operand_types
        self.return_type = return_type

    def __str__(self):
        string = '(' + str(self.left) + str(self.operator) 
        string += '  ' + str(self.right) + ')'
        return string

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.upper() 
        string += " " + self.operator
        string += self.left.pretty_string(level + 1)
        string += self.right.pretty_string(level + 1)
        return string

    def check(self):
        left_type = self.left.check()
        right_type = self.right.check()

        if left_type == Type.IteratorT:
            left_type = Type.IntT

        if right_type == Type.IteratorT:
            right_type = Type.IntT

        if Type.ErrorT not in (left_type, right_type) not in self.operand_types:
            message = "ERROR: operator '%s' used incorrectly with types '%s' and '%s'"
            message += " at line %d, column %d"
            lin, col = self.lexspan[0]
            data = self.operator, left_type, right_type, lin, col
            Errors.static_error.append(message % data)

        return self.return_type

    def evaluate(self):
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()

        if isinstance(self, Divide) and right_value == 0:
            error_dynamic("division by zero", self.lexspan)

        value = self.operation(left_value, right_value)

        if self.return_type == Type.IntT and not -2147483648 <= value <= 2147483647:
            error_dynamic("overflow", self.lexspan)

        return value

###############################################################################


class Plus(Binary):
    """Binary expressions with a '+'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.IntT
        operation = lambda x,y: x + y
        Binary.__init__(self, lexspan, "+", operation, left, right, operand_types, return_type)

#######################################


class Minus(Binary):
    """Binary expressions with a '-'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.IntT
        operation = lambda x,y: x - y
        Binary.__init__(self, lexspan, "-", operation, left, right, operand_types, return_type)

#######################################


class Times(Binary):
    """Binary expressions with a '*'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.IntT
        operation = lambda x,y: x * y
        Binary.__init__(self, lexspan, "*", operation, left, right, operand_types, return_type)

#######################################


class Divide(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.IntT
        operation = lambda x,y: x / y
        Binary.__init__(self, lexspan, "/", operation, left, right, operand_types, return_type)

#######################################


class Modulo(Binary):
    """Binary expressions with a '%'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.IntT
        operation = lambda x,y: x % y
        Binary.__init__(self, lexspan, "%", operation, left, right, operand_types, return_type)

#######################################

class Union(Binary):
    """Binary expressions with a '++'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.SetT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: x | y
        Binary.__init__(self, lexspan, "++", operation, left, right, operand_types, return_type)

#######################################


class Difference(Binary):
    """Binary expressions with a '\'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.SetT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: x - y
        Binary.__init__(self, lexspan, "\\", operation, left, right, operand_types, return_type)

#######################################


class Intersection(Binary):
    """Binary expressions with a '><'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.SetT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: x & y
        Binary.__init__(self, lexspan, "><", operation, left, right, operand_types, return_type)

#######################################

class SetPlus(Binary):
    """Binary expressions with a '<+>'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: set(map(lambda z: x + z, y))
        Binary.__init__(self, lexspan, "<+>", operation, left, right, operand_types, return_type)

#######################################


class SetMinus(Binary):
    """Binary expressions with a '<->'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: set(map(lambda z: x - z, y))
        Binary.__init__(self, lexspan, "<->", operation, left, right, operand_types, return_type)

#######################################


class SetTimes(Binary):
    """Binary expressions with a '<*>'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: set(map(lambda z: x * z, y))
        Binary.__init__(self, lexspan, "<*>", operation, left, right, operand_types, return_type)

#######################################


class SetDivide(Binary):
    """Binary expressions with a '</>'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: set(map(lambda z: x / z, y))
        Binary.__init__(self, lexspan, "</>", operation, left, right, operand_types, return_type)

#######################################


class SetModulo(Binary):
    """Binary expressions with a '<%>'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.SetT
        operation = lambda x,y: set(map(lambda z: x % z, y))
        Binary.__init__(self, lexspan, "<%>", operation, left, right, operand_types, return_type)

#######################################

class Or(Binary):
    """Binary expressions with a 'or'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.BoolT, Type.BoolT)]
        return_type = Type.BoolT
        operation = lambda x,y: x or y
        Binary.__init__(self, lexspan, "or", operation, left, right, operand_types, return_type)

#######################################


class And(Binary):
    """Binary expressions with a 'and'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.BoolT, Type.BoolT)]
        return_type = Type.BoolT
        operation = lambda x,y: x and y
        Binary.__init__(self, lexspan, "and", operation, left, right, operand_types, return_type)

#######################################


class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.BoolT
        operation = lambda x,y: x < y
        Binary.__init__(self, lexspan, "<", operation, left, right, operand_types, return_type)

#######################################


class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.BoolT
        operation = lambda x,y: x <= y
        Binary.__init__(self, lexspan, "<=", operation, left, right, operand_types, return_type)

#######################################


class Greater(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.BoolT
        operation = lambda x,y: x > y
        Binary.__init__(self, lexspan, ">", operation, left, right, operand_types, return_type)

#######################################


class GreaterEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT)]
        return_type = Type.BoolT
        operation = lambda x,y: x >= y
        Binary.__init__(self, lexspan, ">=", operation, left, right, operand_types, return_type)

#######################################


class Equal(Binary):
    """Binary expressions with a '=='"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT),
                         (Type.BoolT, Type.BoolT), 
                         (Type.SetT, Type.SetT)]
        return_type = Type.BoolT
        operation = lambda x,y: x == y
        Binary.__init__(self, lexspan, "==", operation, left, right, operand_types, return_type)

#######################################


class Unequal(Binary):
    """Binary expressions with a '/='"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.IntT),
                         (Type.BoolT, Type.BoolT), 
                         (Type.SetT, Type.SetT)]
        return_type = Type.BoolT
        operation = lambda x,y: x != y
        Binary.__init__(self, lexspan, "/=", operation, left, right, operand_types, return_type)

#######################################


class Contains(Binary):
    """Binary expressions with a '@'"""
    def __init__(self, lexspan, left, right):
        operand_types = [(Type.IntT, Type.SetT)]
        return_type = Type.BoolT
        operation = lambda x,y: x in y
        Binary.__init__(self, lexspan, "@", operation, left, right, operand_types, return_type)

###############################################################################


class Unary(Expression):
    """Unary expressions"""
    def __init__(self, lexspan, operator, operation, operand, operand_type, return_type):
        self.type = Type.UnaryT
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.operation = operation
        self.operand = operand
        self.operand_type = operand_type
        self.return_type = return_type

    def __str__(self):
        string = '(' + str(self.operator) + ' ' + str(self.operand) + ')'
        return string

    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__.upper() 
        string += " " + str(self.operator)
        string += self.operand.pretty_string(level + 1)
        return string

    def check(self):
        exp_type = self.operand.check()

        if exp_type == Type.IteratorT:
            exp_type = Type.IntT

        if Type.ErrorT != exp_type != self.operand_type:
            message = "ERROR: operator '%s' used incorrectly with with type '%s'"
            message += " at line %d, column %d"
            lin, col = self.lexspan[0]
            data = self.operator, exp_type, lin, col
            Errors.static_error.append(message % data)

        return self.return_type

    def evaluate(self):
        exp_value = self.operand.evaluate()

        if (isinstance(self, Min) or isinstance(self, Max)) and len(exp_value) == 0:
            error_dynamic("empty set", self.lexspan)

        value = self.operation(exp_value)

        if self.return_type == Type.IntT and not -2147483648 <= value <= 2147483647:
            error_dynamic("overflow", self.lexspan)

        return value

###############################################################################


class Negate(Unary):
    """Unary expressions with a '-'"""
    def __init__(self, lexspan, operand):
        operand_type = Type.IntT
        return_type = Type.IntT
        operation = lambda x: -x
        Unary.__init__(self, lexspan, "-", operation, operand, operand_type, return_type)

#######################################


class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        operand_type = Type.BoolT
        return_type = Type.BoolT
        operation = lambda x: not x
        Unary.__init__(self, lexspan, "not", operation, operand, operand_type, return_type)

#######################################


class Max(Unary):
    """Unary expressions with a '>?'"""
    def __init__(self, lexspan, operand):
        operand_type = Type.SetT
        return_type = Type.IntT
        operation = lambda x: sorted(x, reverse=True)[0]
        Unary.__init__(self, lexspan, ">?", operation, operand, operand_type, return_type)

#######################################


class Min(Unary):
    """Unary expressions with a '<?'"""
    def __init__(self, lexspan, operand):
        operand_type = Type.SetT
        return_type = Type.IntT
        operation = lambda x: sorted(x)[0]
        Unary.__init__(self, lexspan, "<?", operation, operand, operand_type, return_type)

#######################################


class Size(Unary):
    """Unary expressions with a '$?'"""
    def __init__(self, lexspan, operand):
        operand_type = Type.SetT
        return_type = Type.IntT
        operation = lambda x: len(x)
        Unary.__init__(self, lexspan, "$?", operation, operand, operand_type, return_type)
