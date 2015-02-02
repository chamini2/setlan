#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Abstract Syntax Tree for Setlan
Matteo Ferrando, 09-10285
"""

from sys import exit, stdout
import re

static_error = []

def indent(n):
    return n * '|   '

###############################################################################


class Program(object):
    """A program consists of running a statement"""
    def __init__(self, lexspan, statement):
        self.lexspan = lexspan
        self.statement = statement
        # self.sym_table = SymTable()

    def __str__(self):
        return "program" + self.statement.pretty_string(1)

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
        string = "\n" + indent(level) + "="
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level + 1) + "value:"
        string += self.expression.pretty_string(level + 2)
        return string

###############################################################################


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    def __init__(self, lexspan, statements, sym_table):
        self.lexspan = lexspan
        self.statements = statements
        # self.sym_table = sym_table

    def pretty_string(self, level):
        string = "\n" + indent(level) + "{"

        if self.sym_table:
            string += "\n" + indent(level + 1) + "using"

            for typ, var in self.sym_table:
                string += "\n" + indent(level + 2) + typ
                string += " " + str(var)

            string += "\n" + indent(level + 1) + "in"

        for stat in self.statements:
            string += stat.pretty_string(level + 2)

        string += "\n" + indent(level) + "}"
        return string

###############################################################################


class Scan(Statement):
    """Scan statement, for user input"""
    def __init__(self, lexspan, variable):
        self.lexspan = lexspan
        self.variable = variable
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "scan"
        string += self.variable.pretty_string(level + 1)
        return string

###############################################################################


class Print(Statement):
    """Print statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        self.lexspan = lexspan
        self.elements = elements
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "print"

        for elm in self.elements:
            string += elm.pretty_string(level + 1)

        return string

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
        string = "\n" + indent(level) + "if"

        string += "\n" + indent(level + 1) + "condition"
        string += self.condition.pretty_string(level + 2)

        string += "\n" + indent(level + 1) + "then"
        string += self.then_st.pretty_string(level + 2)

        if self.else_st:
            string += "\n" + indent(level + 1) + "else"
            string += self.else_st.pretty_string(level + 2)

        return string

###############################################################################


class For(Statement):
    """For statement, works with sets"""
    def __init__(self, lexspan, variable, direction, in_set, statement):
        self.lexspan = lexspan
        self.variable = variable
        self.in_set = in_set
        self.statement = statement
        # self.sym_table = None

    def pretty_string(self, level):
        string = "\n" + indent(level) + "for"
        string += self.variable.pretty_string(level + 1)
        string += "\n" + indent(level) + str(direction)
        string += self.in_set.pretty_string(level + 1)
        string += "\n" + indent(level) + "do"
        string += self.statement.pretty_string(level + 1)

        return string
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
            string += "\n" + indent(level) + "repeat"
            string += self.repeat_st.pretty_string(level + 1)

        string += "\n" + indent(level) + "while"
        string += self.condition.pretty_string(level + 1)

        if self.do_st:
            string += "\n" + indent(level) + "do"
            string += self.do_st.pretty_string(level + 1)

        return string


###############################################################################


# For inheritance
# in the .check() method, expressions return the data type or None
class Expression(object): pass

# For inheritance
class Direction(object):
    def pretty_string(self, level):
        return "\n" + indent(level) + self.__class__.__name__[:-10]

class Min_Direction(Direction): pass
class Max_Direction(Direction): pass

# For inheritance
# just for checking the type of an exprssion.
class Type(object):
    def pretty_string(self, level):
        return "\n" + indent(level) + self.__class__.__name__[:-5]

class Variable_Type(Type): pass
class Int_Type(Type): pass
class Set_Type(Type): pass
class Bool_Type(Type): pass
class String_Type(Type): pass
class Binary_Type(Type): pass
class Unary_Type(Type): pass

###############################################################################


class Literal(Expression):
    def pretty_string(self, level):
        string = "\n" + indent(level) + self.__class__.__name__
        string += "\n" + indent(level + 1) + str(self.value)
        return string

###############################################################################


class Variable(Literal):
    """Class to define a variable"""
    def __init__(self, lexspan, value):
        self.type = Variable_Type
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)

###############################################################################


class Int(Literal):
    """Class to define an expression of int"""
    def __init__(self, lexspan, value):
        self.type = Int_Type
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return str(self.value)

    def check(self):
        return self.type

    def evaluate(self):
        return self.value

#######################################


class Bool(Literal):
    """Class to define an expression of bool"""
    def __init__(self, lexspan, value):
        self.type = Bool_Type
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return str(self.value)

    def check(self):
        return self.type

    def evaluate(self):
        return eval(self.value.title())

#######################################


class Set(Literal):
    """Class to define an expression of range"""
    def __init__(self, lexspan, value):
        self.type = Set_Type
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

#######################################


class String(Literal):
    """Class to define an expression of a printable string"""
    def __init__(self, lexspan, value):
        self.type = String_Type
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

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


def error_empty_range(lexspan, operator):
    message = "ERROR: empty range from '%s' operation, "
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
        self.type = Binary_Type
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.left = left
        self.right = right
        self.sym_table = None

    def __str__(self):
        string = str(self.operator) + ' ('
        string += str(self.left) + ', ' + str(self.right) + ')'
        return string

    def pretty_string(self, level):
        return "\n" + indent(level) + str(self)

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
        self.type = Unary_Type
        self.lexspan = lexspan
        self.operator = operator # for printing
        self.operand = operand
        self.sym_table = None

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
