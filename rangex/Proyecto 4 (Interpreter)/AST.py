#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Abstract Syntax Tree for RangeX Language
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285
"""

from SymTable import SymTable, indent
from sys import exit, stdout
import re

static_error = []


# To set the symbol table of symbol
def set_sym_table(target, sym_table):
    if isinstance(target, Block):
        target.sym_table.outer = sym_table
    else:
        target.sym_table = sym_table


class Program(object):
    """A program consists of running a statement"""
    def __init__(self, lexspan, statement):
        self.lexspan = lexspan
        self.statement = statement
        self.sym_table = SymTable()

    def __str__(self):
        return "PROGRAM\n" + self.statement.tree_string(1)

    def check(self):
        set_sym_table(self.statement, self.sym_table)
        return self.statement.check()

    def execute(self):
        self.statement.execute()

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
        data = exp_type, place_string, should, s_lin, s_col, e_lin, e_col
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
        self.lexspan = lexspan
        self.variable = variable
        self.expression = expression
        self.sym_table = None

    def tree_string(self, level):
        string = indent(level) + "ASSIGN\n" + indent(level + 1)
        string += "variable: " + str(self.variable)
        string += "\n" + indent(level + 1)
        string += "value:\n" + self.expression.tree_string(level + 2)
        return string

    def check(self):
        set_sym_table(self.variable, self.sym_table)
        set_sym_table(self.expression, self.sym_table)

        var_type = self.variable.check()
        exp_type = self.expression.check()

        if var_type is not None:
            var_info = self.sym_table.find(self.variable)
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

    def execute(self):
        value = self.expression.evaluate()
        data_type = self.expression.type
        self.sym_table.update(self.variable, data_type, value)

###############################################################################


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    def __init__(self, lexspan, statements, sym_table):
        self.lexspan = lexspan
        self.statements = statements
        self.sym_table = sym_table

    def tree_string(self, level):
        string = indent(level) + "BEGIN\n"

        if self.sym_table:
            string += self.sym_table.tree_string(level) + '\n'
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
            set_sym_table(stat, self.sym_table)
            if stat.check() is False:
                boolean = False

        return boolean

    def execute(self):
        for stat in self.statements:
            stat.execute()

###############################################################################


class Read(Statement):
    """Read statement, for user input"""
    def __init__(self, lexspan, variable):
        self.lexspan = lexspan
        self.variable = variable
        self.sym_table = None

    def tree_string(self, level):
        string = indent(level) + "READ\n"
        string += self.variable.tree_string(level + 1)
        return string

    def check(self):
        set_sym_table(self.variable, self.sym_table)
        var_type = self.variable.check()

        if var_type is None:
            return False
        else:
            return True

    def execute(self):
        def ask_int():
            raw = raw_input()
            match = re.match(r'^\s*-?\s*\d+\s*$', raw)
            if match:
                value = int(match.group())
                if not (-2147483648 <= value <= 2147483648):
                    print "\nexpecting an int value, overflow, try again."
                    return ask_int()
                return value
            else:
                print "\nexpecting an int value, try again."
                return ask_int()

        def ask_range():
            raw = raw_input()
            raw = raw.strip(' \t\n\r')
            raw = re.split(r"\.\.|,", raw)
            if len(raw) != 2:
                print "\nexpecting a range value, try again."
                return ask_range()

            left = re.match(r'^\s*-?\s*\d+\s*$', raw[0])
            right = re.match(r'^\s*-?\s*\d+\s*$', raw[1])
            if not (left and right):
                print "\nexpecting a range value, try again."
                return ask_range()

            left, right = int(left.group()), int(right.group())
            if not (-2147483648 <= left <= 2147483648):
                print "\nexpecting a range value, overflow, try again."
                return ask_int()
            if not (-2147483648 <= right <= 2147483648):
                print "\nexpecting a range value, overflow, try again."
                return ask_int()

            if left > right:
                print "\nexpecting a range value,",
                print "left side larger than right side, try again."
                return ask_range()

            return left, right

        def ask_bool():
            raw = raw_input()
            raw = raw.strip(' \t\n\r')
            raw = raw.lower()
            if raw == 'true' or raw == 'false':
                return eval(raw.title())
            else:
                print "\nexpecting a bool value, try again."
                return ask_bool()

        symbol = self.sym_table.find(self.variable)
        if symbol.data_type == 'INT':
            value = ask_int()
        elif symbol.data_type == 'RANGE':
            value = ask_range()
        else:
            value = ask_bool()

        self.sym_table.update(self.variable, symbol.data_type, value)

###############################################################################


class Write(Statement):
    """Write statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        self.lexspan = lexspan
        self.elements = elements
        self.sym_table = None

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
            set_sym_table(elem, self.sym_table)
            if elem.check() is None:
                boolean = False

        return boolean

    def execute(self):
        for elem in self.elements:
            intrp = elem.evaluate()
            if isinstance(intrp, bool):
                stdout.write(str(intrp).lower())
            elif isinstance(intrp, tuple):
                stdout.write(str(eval(str(intrp[0]))))
                stdout.write('..')
                stdout.write(str(eval(str(intrp[1]))))
            else:
                stdout.write(str(eval(str(intrp))))


class WriteLn(Write):
    """Writeln statement, Write with a new line at the end"""
    def __init__(self, lexspan, elements):
        Write.__init__(self, lexspan, elements)

    def execute(self):
        Write.execute(self)
        stdout.write('\n')

###############################################################################


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st
        self.sym_table = None

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
        set_sym_table(self.condition, self.sym_table)
        set_sym_table(self.then_st, self.sym_table)

        cnd_type = self.condition.check()
        thn_type = self.then_st.check()

        if self.else_st:
            set_sym_table(self.else_st, self.sym_table)
            els_type = self.else_st.check()

        if not error_invalid_expression(cnd_type, self.condition,
                                        "'if' condition", 'BOOL'):
            boolean = False

        if thn_type is False:
            boolean = False

        if self.else_st and els_type is False:
            boolean = False

        return boolean

    def execute(self):
        condition = self.condition.evaluate()
        if condition:
            self.then_st.execute()
        elif self.else_st:
            self.else_st.execute()

###############################################################################


class CaseOf(Statement):
    """CaseOf statement, an int between ranges"""
    def __init__(self, lexspan, int_expr, cases):
        self.lexspan = lexspan
        self.int_expr = int_expr
        self.cases = cases
        self.sym_table = None

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
        set_sym_table(self.int_expr, self.sym_table)
        exp_type = self.int_expr.check()

        if not error_invalid_expression(exp_type, self.int_expr,
                                        "'case' condition", 'INT'):
            boolean = False

        for case in self.cases:
            set_sym_table(case, self.sym_table)
            if case.check() is False:
                boolean = False

        return boolean

    def execute(self):
        int_expr = self.int_expr.evaluate()
        for case in self.cases:
            case.execute(int_expr)


class Case(Statement):
    """A specific case (range and associated statement) for a CaseOf"""
    def __init__(self, lexspan, range_expr, statement):
        self.lexspan = lexspan
        self.range_expr = range_expr
        self.statement = statement
        self.sym_table = None

    def tree_string(self, level):
        string = indent(level) + "case:\n"
        string += indent(level + 1) + "range:\n"
        string += self.range_expr.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "statement:\n"
        string += self.statement.tree_string(level + 2) + '\n'

        return string

    def check(self):
        boolean = True
        set_sym_table(self.range_expr, self.sym_table)
        set_sym_table(self.statement, self.sym_table)

        exp_type = self.range_expr.check()

        if not error_invalid_expression(exp_type, self.range_expr,
                                        "'case' range", 'RANGE'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

    def execute(self, int_expr):
        range_from, range_to = self.range_expr.evaluate()
        if range_from <= int_expr <= range_to:
            self.statement.execute()

###############################################################################


class For(Statement):
    """For statement, works in ranges"""
    def __init__(self, lexspan, variable, in_range, statement):
        self.lexspan = lexspan
        self.variable = variable
        self.in_range = in_range
        self.statement = statement
        self.sym_table = None

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

        for_sym_table = SymTable()
        for_sym_table.outer = self.sym_table
        for_sym_table.insert(self.variable, 'INT', True)

        set_sym_table(self.in_range, self.sym_table)
        set_sym_table(self.statement, for_sym_table)

        exp_type = self.in_range.check()

        if not error_invalid_expression(exp_type, self.in_range,
                                        "'for' range", 'RANGE'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

    def execute(self):
        in_from, in_to = self.in_range.evaluate()
        for val in range(in_from, in_to + 1):
            self.statement.sym_table.update(self.variable, 'INT', val)
            self.statement.execute()

###############################################################################


class While(Statement):
    """While statement, takes a condition"""
    def __init__(self, lexspan, condition, statement):
        self.lexspan = lexspan
        self.condition = condition
        self.statement = statement
        self.sym_table = None

    def tree_string(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.tree_string(level + 2) + '\n'

        string += indent(level + 1) + "DO:\n"
        string += self.statement.tree_string(level + 2)

        return string

    def check(self):
        boolean = True
        set_sym_table(self.condition, self.sym_table)
        set_sym_table(self.statement, self.sym_table)

        exp_type = self.condition.check()

        if not error_invalid_expression(exp_type, self.condition,
                                        "'while' condition", 'BOOL'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

    def execute(self):
        while self.condition.evaluate():
            self.statement.execute()

###############################################################################


# For inheritance
# in the .check() method, expressions return the data type or None
class Expression(object): pass

###############################################################################


class Variable(Expression):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
        self.type = 'VARIABLE'
        self.lexspan = lexspan
        self.name = name
        self.sym_table = None

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
        if self.sym_table.is_member(self):
            variable = self.sym_table.find(self)
            self.type = variable.data_type
            return self.type
        else:
            message = "ERROR: variable '%s'"
            message += " not in sym_table at line %d, column %d"
            line, column = self.lexspan[0]
            data = self.name, line, column
            static_error.append(message % data)
            return None

    def evaluate(self):
        symbol = self.sym_table.find(self)
        if not symbol.initialized:
            message = "ERROR: variable '%s' not initialized"
            message += " at line %d, column %d"
            line, column = self.lexspan[0]
            data = self.name, line, column
            print message % data
            exit()

        return symbol.value

###############################################################################


class Int(Expression):
    """Class to define an expression of int"""
    def __init__(self, lexspan, value):
        self.type = 'INT'
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return str(self.value)

    def tree_string(self, level):
        return indent(level) + "INT: " + str(self.value)

    def check(self):
        return self.type

    def evaluate(self):
        return self.value

#######################################


class Bool(Expression):
    """Class to define an expression of bool"""
    def __init__(self, lexspan, value):
        self.type = 'BOOL'
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return str(self.value)

    def tree_string(self, level):
        return indent(level) + "BOOL: " + str(self.value)

    def check(self):
        return self.type

    def evaluate(self):
        return eval(self.value.title())

#######################################


class Range(Expression):
    """Class to define an expression of range"""
    def __init__(self, lexspan, from_value, to_value):
        self.type = 'RANGE'
        self.lexspan = lexspan
        self.operator = '..'
        self.from_value = from_value
        self.to_value = to_value
        self.sym_table = None

    def __str__(self):
        return str(self.from_value) + self.operator + str(self.to_value)

    def tree_string(self, level):
        string = indent(level) + "FROM:\n"
        string += self.from_value.tree_string(level + 1) + '\n'
        string += indent(level) + "TO:\n"
        string += self.to_value.tree_string(level + 1)
        return string

    def check(self):
        set_sym_table(self.from_value, self.sym_table)
        set_sym_table(self.to_value, self.sym_table)
        left = self.from_value.check()
        right = self.to_value.check()
        type_tuples = [('INT', 'INT', 'RANGE')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        from_val = self.from_value.evaluate()
        to_val = self.to_value.evaluate()

        if from_val > to_val:
            error_empty_range(self.lexspan, self.operator)

        if not (-2147483648 <= from_val <= 2147483648):
            error_overflow(self.from_value.lexspan, self.operator)

        if not (-2147483648 <= to_val <= 2147483648):
            error_overflow(self.to_value.lexspan, self.operator)

        return from_val, to_val

#######################################


class String(Expression):
    """Class to define an expression of a printable string"""
    def __init__(self, lexspan, value):
        self.type = 'STRING'
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return self.value

    def tree_string(self, level):
        return indent(level) + "STRING: " + str(self.value)

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
        self.type = "BINARY"
        self.lexspan = lexspan
        self.operator = operator
        self.left = left
        self.right = right
        self.sym_table = None

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
        Binary.__init__(self, lexspan, "+", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('RANGE', 'RANGE')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.type == 'INT':
            value = left + right
            if not (-2147483648 <= value <= 2147483648):
                error_overflow(self.lexspan, self.operator)
            return value

        else:
            from_l, to_l = left
            from_r, to_r = right
            from_val, to_val = min(from_l,from_r), max(to_l, to_r)

            if from_val > to_val:
                error_empty_range(self.lexspan, self.operator)

            if not (-2147483648 <= from_val <= 2147483648):
                error_overflow(self.from_value.lexspan, self.operator)

            if not (-2147483648 <= to_val <= 2147483648):
                error_overflow(self.to_value.lexspan, self.operator)

            return from_val, to_val

#######################################


class Minus(Binary):
    """Binary expressions with a '-'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "-", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        value = left - right

        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

#######################################


class Times(Binary):
    """Binary expressions with a '*'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "*", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('RANGE', 'INT', 'RANGE')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.type == 'INT':
            value = left * right
            if not (-2147483648 <= value <= 2147483648):
                error_overflow(self.lexspan, self.operator)
            return value

        else:
            form_val, to_val = left[0] * right, left[1] * right
            if right >= 0:
                return form_val, to_val
            else:
                return to_val, form_val

#######################################


class Divide(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if right == 0:
            error_division_by_zero(self.lexspan, self.operator)

        value = left / right
        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

#######################################


class Modulo(Binary):
    """Binary expressions with a '%'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "%", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if right == 0:
            error_division_by_zero(self.lexspan, self.operator)

        value = left % right
        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

#######################################


class Intersection(Binary):
    """Binary expressions with a '<>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<>", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('RANGE', 'RANGE')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        l_from, l_to = self.left.evaluate()
        r_from, r_to = self.right.evaluate()
        from_val, to_val = max(l_from, r_from), min(l_to, r_to)

        if from_val > to_val:
            error_empty_range(self.lexspan, self.operator)

        if not (-2147483648 <= from_val <= 2147483648):
            error_overflow(self.from_value.lexspan, self.operator)

        if not (-2147483648 <= to_val <= 2147483648):
            error_overflow(self.to_value.lexspan, self.operator)

        return from_val, to_val

#######################################


class Or(Binary):
    """Binary expressions with a 'or'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "or", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left or right

#######################################


class And(Binary):
    """Binary expressions with a 'and'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "and", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left and right

#######################################


class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.left.type == 'INT':
            return left < right
        else:
            return left[1] < right[0]

#######################################


class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<=", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.left.type == 'INT':
            return left <= right
        else:
            return left[1] <= right[0]

#######################################


class Great(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.left.type == 'INT':
            return left > right
        else:
            return left[1] > right[0]

#######################################


class GreatEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">=", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('RANGE', 'RANGE', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.left.type == 'INT':
            return left >= right
        else:
            return left[1] >= right[0]

#######################################


class Equal(Binary):
    """Binary expressions with a '=='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "==", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('RANGE', 'RANGE', 'BOOL'), ('BOOL', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left == right

#######################################


class Unequal(Binary):
    """Binary expressions with a '/='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/=", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('RANGE', 'RANGE', 'BOOL'), ('BOOL', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left != right

#######################################


class Belong(Binary):
    """Binary expressions with a '>>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">>", left, right)

    def check(self):
        set_sym_table(self.left, self.sym_table)
        set_sym_table(self.right, self.sym_table)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'RANGE', 'BOOL')]
        self.type = check_bin(self.lexspan, self.operator,
                              left, right, type_tuples)
        return self.type

    def evaluate(self):
        left = self.left.evaluate()
        r_from, r_to = self.right.evaluate()

        return r_from <= left <= r_to

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
        self.type = "UNARY"
        self.lexspan = lexspan
        self.operator = operator
        self.operand = operand
        self.sym_table = None

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
        Unary.__init__(self, lexspan, "-", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('INT',)]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        operand = self.operand.evaluate()
        return operand * -1

#######################################


class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "not", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('BOOL',)]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        operand = self.operand.evaluate()
        return not operand

#######################################


class RtoI(Unary):
    """Unary expressions with a 'rtoi()'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "rtoi", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        op_from, op_to = self.operand.evaluate()
        if op_from != op_to:
            message = "ERROR: usage of 'rtoi()' function on range with"
            message += "length greater than 1, "
            message += "from line %d, column %d to line %d, column %d"
            s_lin, s_col = self.lexspan[0]
            e_lin, e_col = self.lexspan[1]
            data = s_lin, s_col, e_lin, e_col
            print '\n\n', message % data
            exit()
        else:
            return op_from

#######################################


class Length(Unary):
    """Unary expressions with a 'length()'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "length", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        op_from, op_to = self.operand.evaluate()
        return op_to - op_from + 1

#######################################


class Top(Unary):
    """Unary expressions with a 'top()'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "top", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        _, op_to = self.operand.evaluate()
        return op_to

#######################################


class Bottom(Unary):
    """Unary expressions with a 'bottom()'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "bottom", operand)

    def check(self):
        set_sym_table(self.operand, self.sym_table)
        operand = self.operand.check()
        types = [('RANGE', 'INT')]
        self.type = check_unary(self.lexspan, self.operator, operand, types)
        return self.type

    def evaluate(self):
        op_from, _ = self.operand.evaluate()
        return op_from
