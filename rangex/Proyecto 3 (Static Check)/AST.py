#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Abstract Syntax Tree for RangeX Language
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285
"""

from SymTable import SymTable, indent


static_error = []


# To set the scope of symbol
def set_scope(target, scope):
    if isinstance(target, Block):
        target.scope.outer = scope
    else:
        target.scope = scope


class Program(object):
    """A program consists of running a statement"""
    def __init__(self, lexspan, statement):
        # self.type = "program"
        self.lexspan = lexspan
        self.statement = statement
        self.scope = SymTable()

    def __str__(self):
        return "PROGRAM\n" + self.statement.tree_string(1)

    def check(self):
        set_scope(self.statement, self.scope)
        return self.statement.check()

###############################################################################


# For inheritance
# in the .check() method, statements return booleans values
class Statement(object): pass


def error_invalid_expression(exp_type, place, place_string, should):
    if exp_type != should and exp_type is not None:
        message = "ERROR: expression of type '%s' in %s "
        message += "(must be '%s') from line %d, column %d"
        message += " to line %d, column %d"
        s_lin, s_col = place.lexspan[0]
        e_lin, e_col = place.lexspan[1]
        data = place_string, exp_type, should, s_lin, s_col, e_lin, e_col
        static_error.append(message % data)
        return False
    elif exp_type is None:
        return False
    else:
        return True

###############################################################################


class Assign(Statement):
    """The assign statement"""
    def __init__(self, lexspan, variable, expression):
        # self.type = "assign"
        self.lexspan = lexspan
        self.variable = variable
        self.expression = expression

    def tree_string(self, level):
        string = indent(level) + "ASSIGN\n" + indent(level + 1)
        string += "variable: " + str(self.variable)
        string += "\n" + indent(level + 1)
        string += "value:\n" + self.expression.tree_string(level + 2)
        return string

    def check(self):
        set_scope(self.variable, self.scope)
        set_scope(self.expression, self.scope)

        var_type = self.variable.check()
        exp_type = self.expression.check()

        if var_type is not None:
            var_info = self.scope.find(self.variable)
            if var_info.protected:
                message = "ERROR: modifying at line %d, column %d "
                message += "value of variable '%s' that belongs to "
                message += "a for statement at line %d, column %d"
                var_lin, var_col = self.variable.lexspan[0]
                for_slin, for_scol = var_info.lexspan[0]
                data = var_lin, var_col, var_info.name, for_slin, for_scol
                static_error.append(message % data)

        if var_type is None or exp_type is None:
            return False

        if var_type != exp_type:
            message = "ERROR: assigning expression of type '%s' to "
            message += "variable '%s' of type '%s' from line %d, column %d"
            message += " to line %d, column %d"
            s_lin, s_col = self.lexspan[0]
            e_lin, e_col = self.lexspan[1]
            data = (exp_type, self.variable.name, var_type,
                    s_lin, s_col, e_lin, e_col)
            static_error.append(message % data)
            return False

        return True


###############################################################################


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    def __init__(self, lexspan, statements, scope=SymTable()):
        # self.type = "block"
        self.lexspan = lexspan
        self.statements = statements
        self.scope = scope

    def tree_string(self, level):
        string = indent(level) + "BEGIN\n"

        if self.scope:
            string += self.scope.tree_string(level) + '\n'
        string += indent(level) + "STATEMENTS\n"

        for stat in self.statements:
            string += stat.tree_string(level + 1) + '\n'
            string += indent(level + 1) + "SEPARATOR\n"
        string = string[:(-10 - len(indent(1)))]
        string += "END"

        return string

    def check(self):
        boolean = True

        for stat in self.statements:
            set_scope(stat, self.scope)
            if stat.check() is False:
                boolean = False

        return boolean

###############################################################################


class Read(Statement):
    """Read statement, for user input"""
    def __init__(self, lexspan, variable):
        # self.type = "read"
        self.lexspan = lexspan
        self.variable = variable

    def tree_string(self, level):
        string = indent(level) + "READ\n"
        string += self.variable.tree_string(level + 1)
        return string

    def check(self):
        set_scope(self.variable, self.scope)
        var_type = self.variable.check()

        if var_type is None:
            return False
        else:
            return True

###############################################################################


class Write(Statement):
    """Write statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        # self.type = "write"
        self.lexspan = lexspan
        self.elements = elements

    def tree_string(self, level):
        if isinstance(self, WriteLn):
            string = indent(level) + "WRITELN\n"
        else:
            string = indent(level) + "WRITE\n"

        for elem in self.elements:
            string += indent(level + 1) + "element:\n"
            string += elem.tree_string(level + 2) + '\n'

        return string[:-1]

    def check(self):
        boolean = True

        for elem in self.elements:
            set_scope(elem, self.scope)
            if elem.check() is None:
                boolean = False

        return boolean


class WriteLn(Write):
    """Writeln statement, Write with a new line at the end"""
    def __init__(self, lexspan, elements):
        Write.__init__(self, lexspan, elements)
        # self.type = "writeln"

###############################################################################


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        # self.type = "if"
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st

    def tree_string(self, level):
        string = indent(level) + "IF\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "then:\n"
        string += self.then_st.tree_string(level + 2)

        if self.else_st:
            string += '\n' + indent(level + 1) + "else:\n"
            string += self.else_st.tree_string(level + 2)

        return string

    def check(self):
        boolean = True
        set_scope(self.condition, self.scope)
        set_scope(self.then_st, self.scope)

        cnd_type = self.condition.check()
        thn_type = self.then_st.check()

        if self.else_st:
            set_scope(self.else_st, self.scope)
            els_type = self.else_st.check()

        if not error_invalid_expression(cnd_type, self.condition,
                                        "'if' condition", 'BOOL'):
            boolean = False

        if thn_type is False:
            boolean = False

        if self.else_st and els_type is False:
            boolean = False

        return boolean

###############################################################################


class CaseOf(Statement):
    """CaseOf statement, an int between ranges"""
    def __init__(self, lexspan, int_expr, cases):
        # self.type = "caseof"
        self.lexspan = lexspan
        self.int_expr = int_expr
        self.cases = cases

    def tree_string(self, level):
        string = indent(level) + "CASE\n"
        string += indent(level + 1) + "value:\n"
        string += self.int_expr.tree_string(level + 2) + '\n'

        for case in self.cases:
            string += case.tree_string(level + 1)
        string += indent(level) + "END"

        return string

    def check(self):
        boolean = True
        set_scope(self.int_expr, self.scope)
        exp_type = self.int_expr.check()

        if not error_invalid_expression(exp_type, self.int_expr,
                                        "'case' condition", 'INT'):
            boolean = False

        for case in self.cases:
            set_scope(case, self.scope)
            if case.check() is False:
                boolean = False

        return boolean


class Case(Statement):
    """A specific case (range and associated statement) for a CaseOf"""
    def __init__(self, lexspan, range_expr, statement):
        # self.type = "case"
        self.lexspan = lexspan
        self.range_expr = range_expr
        self.statement = statement

    def tree_string(self, level):
        string = indent(level) + "case:\n"
        string += indent(level + 1) + "range:\n"
        string += self.range_expr.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "statement:\n"
        string += self.statement.tree_string(level + 2) + '\n'

        return string

    def check(self):
        boolean = True
        set_scope(self.range_expr, self.scope)
        set_scope(self.statement, self.scope)

        exp_type = self.range_expr.check()

        if not error_invalid_expression(exp_type, self.range_expr,
                                        "'case' range", 'RANGE'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

###############################################################################


class For(Statement):
    """For statement, works in ranges"""
    def __init__(self, lexspan, variable, in_range, statement):
        # self.type = "for"
        self.lexspan = lexspan
        self.variable = variable
        self.in_range = in_range
        self.statement = statement

    def tree_string(self, level):
        string = indent(level) + "FOR\n"
        string += self.variable.tree_string(level + 1) + '\n'

        string += indent(level + 1) + "IN:\n"
        string += self.in_range.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "DO:\n"
        string += self.statement.tree_string(level + 2)

        return string

    def check(self):
        boolean = True

        for_scope = SymTable()
        for_scope.outer = self.scope
        for_scope.insert(self.variable, 'INT', True)

        set_scope(self.in_range, self.scope)
        set_scope(self.statement, for_scope)

        exp_type = self.in_range.check()

        if not error_invalid_expression(exp_type, self.in_range,
                                        "'for' range", 'RANGE'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean


###############################################################################


class While(Statement):
    """While statement, takes a condition"""
    def __init__(self, lexspan, condition, statement):
        # self.type = "while"
        self.lexspan = lexspan
        self.condition = condition
        self.statement = statement

    def tree_string(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "DO:\n"
        string += self.statement.tree_string(level + 2)

        return string

    def check(self):
        boolean = True
        set_scope(self.condition, self.scope)
        set_scope(self.statement, self.scope)

        exp_type = self.condition.check()

        if not error_invalid_expression(exp_type, self.condition,
                                        "'while' condition", 'BOOL'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

###############################################################################


# For inheritance
# in the .check() method, expressions return the data type or None
class Expression(object): pass

###############################################################################


class Variable(Expression):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
        # self.type = "var"
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

    def tree_string(self, level):
        return indent(level) + "VARIABLE: " + str(self.name)

    def check(self):
        if self.scope.is_member(self):
            variable = self.scope.find(self)
            return variable.data_type
        else:
            message = "ERROR: variable '%s' not in scope at line %d, column %d"
            line, column = self.lexspan[0]
            data = self.name, line, column
            static_error.append(message % data)
            return None

###############################################################################


class Int(Expression):
    """Class to define an expression of int"""
    def __init__(self, lexspan, value):
        # self.type = "int"
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value)

    def tree_string(self, level):
        return indent(level) + "INT: " + str(self.value)

    def check(self):
        return 'INT'

#######################################


class Bool(Expression):
    """Class to define an expression of bool"""
    def __init__(self, lexspan, value):
        # self.type = "bool"
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value)

    def tree_string(self, level):
        return indent(level) + "BOOL: " + str(self.value)

    def check(self):
        return 'BOOL'

#######################################


class Range(Expression):
    """Class to define an expression of range"""
    def __init__(self, lexspan, from_value, to_value):
        # self.type = "range"
        self.lexspan = lexspan
        self.from_value = from_value
        self.to_value = to_value

    def __str__(self):
        return str(self.from_value) + '..' + str(self.to_value)

    def tree_string(self, level):
        string = indent(level) + "FROM:\n"
        string += self.from_value.tree_string(level + 1) + '\n'
        string += indent(level) + "TO:\n"
        string += self.to_value.tree_string(level + 1)
        return string

    def check(self):
        set_scope(self.from_value, self.scope)
        set_scope(self.to_value, self.scope)
        left = self.from_value.check()
        right = self.to_value.check()
        type_tuples = [('INT', 'INT', 'RANGE')]
        return check_bin(self.lexspan, '..', left, right, type_tuples)

#######################################


class String(Expression):
    """Class to define an expression of a printable string"""
    def __init__(self, lexspan, value):
        # self.type = "string"
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return self.value

    def tree_string(self, level):
        return indent(level) + "STRING: " + str(self.value)

    def check(self):
        return 'STRING'

###############################################################################


def error_unsuported_binary(lexspan, operator, left, right):
    message = "ERROR: unsupported operator '%s' for types '%s' and '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(left), str(right), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)


# Checks that the left and right operator has any of the accepted layouts
def check_bin(lexspan, operator, left, right, types):
    for type_tuple in types:
        t_return = None
        if len(type_tuple) == 3:
            t_left, t_right, t_return = type_tuple
        else:
            t_left, t_right = type_tuple

        if (left, right) == (t_left, t_right):
            if t_return is not None:
                return t_return
            else:
                return left

    if left is not None and right is not None:
        error_unsuported_binary(lexspan, operator, left, right)
    return None


class Binary(Expression):
    """Binary expressions"""
    def __init__(self, lexspan, operator, left, right):
        # self.type = "binary: "
        self.lexspan = lexspan
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        string = str(self.operator) + ' ('
        string += str(self.left) + ', ' + str(self.right) + ')'
        return string

    def tree_string(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += "operator: " + str(self.operator) + '\n'

        string += indent(level + 1) + "left operand:\n"
        string += self.left.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "right operand:\n"
        string += self.right.tree_string(level + 2)

        return string

###############################################################################


class Plus(Binary):
    """Binary expressions with a '+'"""
    def __init__(self, lexspan, left, right):
        # self.type = "+"
        Binary.__init__(self, lexspan, "+", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('RANGE', 'RANGE')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Minus(Binary):
    """Binary expressions with a '-'"""
    def __init__(self, lexspan, left, right):
        # self.type = "-"
        Binary.__init__(self, lexspan, "-", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Times(Binary):
    """Binary expressions with a '*'"""
    def __init__(self, lexspan, left, right):
        # self.type = "*"
        Binary.__init__(self, lexspan, "*", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('RANGE', 'INT', 'RANGE')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Divide(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        # self.type = "/"
        Binary.__init__(self, lexspan, "/", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Modulo(Binary):
    """Binary expressions with a '%'"""
    def __init__(self, lexspan, left, right):
        # self.type = "%"
        Binary.__init__(self, lexspan, "%", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Intersection(Binary):
    """Binary expressions with a '<>'"""
    def __init__(self, lexspan, left, right):
        # self.type = "<>"
        Binary.__init__(self, lexspan, "<>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('RANGE', 'RANGE')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Or(Binary):
    """Binary expressions with a 'or'"""
    def __init__(self, lexspan, left, right):
        # self.type = "or"
        Binary.__init__(self, lexspan, "or", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class And(Binary):
    """Binary expressions with a 'and'"""
    def __init__(self, lexspan, left, right):
        # self.type = "and"
        Binary.__init__(self, lexspan, "and", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        # self.type = "<"
        Binary.__init__(self, lexspan, "<", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        # self.type = "<="
        Binary.__init__(self, lexspan, "<=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Great(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        # self.type = ">"
        Binary.__init__(self, lexspan, ">", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class GreatEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        # self.type = ">="
        Binary.__init__(self, lexspan, ">=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Equal(Binary):
    """Binary expressions with a '=='"""
    def __init__(self, lexspan, left, right):
        # self.type = "=="
        Binary.__init__(self, lexspan, "==", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('RANGE', 'RANGE', 'BOOL'), ('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Unequal(Binary):
    """Binary expressions with a '/='"""
    def __init__(self, lexspan, left, right):
        # self.type = "/="
        Binary.__init__(self, lexspan, "/=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('RANGE', 'RANGE', 'BOOL'), ('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Belong(Binary):
    """Binary expressions with a '>>'"""
    def __init__(self, lexspan, left, right):
        # self.type = ">>"
        Binary.__init__(self, lexspan, ">>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'RANGE', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

###############################################################################


def error_unsuported_unary(lexspan, operator, operand):
    message = "ERROR: unsupported operator '%s' for type: '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(operand), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)


def check_unary(lexspan, operator, operand, types):
    for tpe in types:
        t_return = None
        if len(tpe) == 2:
            t_operand, t_return = tpe
        else:
            t_operand, = tpe

        if operand == t_operand:
            if t_return is not None:
                return t_return
            else:
                return operand

    if operand is not None:
        error_unsuported_unary(lexspan, operator, operand)
    return None


class Unary(Expression):
    """Unary expressions"""
    def __init__(self, lexspan, operator, operand):
        # self.type = "unary: "
        self.lexspan = lexspan
        self.operator = operator
        self.operand = operand

    def tree_string(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) + "operator: "
        string += str(self.operator) + '\n'

        string += indent(level + 1) + "operand:\n"
        string += self.operand.tree_string(level + 2)

        return string

###############################################################################


class UMinus(Unary):
    """Unary expressions with a '-'"""
    def __init__(self, lexspan, operand):
        # self.type = "-"
        Unary.__init__(self, lexspan, "-", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('INT',)]
        return check_unary(self.lexspan, self.operator, operand, types)

#######################################


class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        # self.type = "not"
        Unary.__init__(self, lexspan, "not", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('BOOL',)]
        return check_unary(self.lexspan, self.operator, operand, types)

#######################################


class RtoI(Unary):
    """Unary expressions with a 'rtoi()'"""
    def __init__(self, lexspan, operand):
        # self.type = "rtoi"
        Unary.__init__(self, lexspan, "rtoi", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

#######################################


class Length(Unary):
    """Unary expressions with a 'length()'"""
    def __init__(self, lexspan, operand):
        # self.type = "length"
        Unary.__init__(self, lexspan, "length", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

#######################################


class Top(Unary):
    """Unary expressions with a 'top()'"""
    def __init__(self, lexspan, operand):
        # self.type = "top"
        Unary.__init__(self, lexspan, "top", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

#######################################


class Bottom(Unary):
    """Unary expressions with a 'bottom()'"""
    def __init__(self, lexspan, operand):
        # self.type = "bottom"
        Unary.__init__(self, lexspan, "bottom", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        return check_unary(self.lexspan, self.operator, operand, types)
