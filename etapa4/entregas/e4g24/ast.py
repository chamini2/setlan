#!/isr/bin/env python
# -*- coding: utf-8 -*-

####
#CI3725 - Etapa 1 - Análisis Lexicográfico
#Fabio, Castro, 10-10132
#Antonio, Scaramazza 11-10957
####

from SymTable import SymTable, indent
from sys import exit, stdout
import re
import copy

static_error = []


# To set the scope of symbol
def set_scope(target, scope):
    if isinstance(target, Block):
        target.scope.outer = scope
    else:
        target.scope = scope


class Program:
    """Un programa consiste en expresiones"""
    def __init__(self, lexspan, statement):
        self.lexspan = lexspan
        self.statement = statement
        self.scope = SymTable()

    def __str__(self):
        return "PROGRAM\n" + self.statement.print_tree(1)

    def print_symtab(self):
        return "SymTable: \n"+str(self.statement.print_symtab(1))

    def check(self):
        set_scope(self.statement, self.scope)
        return self.statement.check()

    def execute(self):
        self.statement.execute()

# Para heredar
class Statement: pass

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

class Assign(Statement):
    """Declaracion de asignacion"""
    def __init__(self, lexspan, variable, expression):
        self.lexspan = lexspan
        self.variable = variable
        self.expression = expression

    def print_tree(self, level):
        string = indent(level) + "ASSIGN\n" + indent(level + 1)
        string += "variable: " + str(self.variable)
        string += "\n" + indent(level + 1)
        string += "value:\n" + self.expression.print_tree(level + 2)
        return string

    def print_symtab(self,level):
        string = ""
        return string

    def check(self):
        set_scope(self.variable, self.scope)
        set_scope(self.expression, self.scope)

        var_type = self.variable.check()
        exp_type = self.expression.check()

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
        data_type = self.expression.check()
        self.scope.update(self.variable, data_type, value)

class Block(Statement):
    """Declaracion de bloque"""
    def __init__(self, lexspan, statements, scope):
        self.lexspan = lexspan
        self.statements = statements
        self.scope = scope

    def print_tree(self, level):
        string = indent(level) + "BEGIN\n"

        if self.scope:
            string += indent(level) + "USING\n"
            string += self.scope.print_tree(level) + '\n'
            string += indent(level) + "IN\n"

        for stat in self.statements:
            string += stat.print_tree(level + 1) + '\n'
            string += indent(level + 1) + "SEPARATOR\n"
        string = string[:(-10 - len(indent(1)))]
        string += "END"

        return string

    def execute(self):
        for stat in self.statements:
            stat.execute()


    def print_symtab(self, level):
        if self.scope:
            string = indent(level-1) + "SCOPE\n"
            string += self.scope.print_symtab(level) 
        for stat in self.statements:
            string += stat.print_symtab(level+2) 
        if self.scope:
            string += indent(level-1) + "END_SCOPE\n"
        return string       

    def check(self):
        boolean = True
        for stat in self.statements:
            set_scope(stat, self.scope)
            if stat.check() is False:
                boolean = False
        return boolean

class Scan(Statement):
    """Declaracion scan, se aplica sobre una variable """
    def __init__(self, lexspan, variable):
        self.lexspan = lexspan
        self.variable = variable

    def print_tree(self, level):
        string = indent(level) + "SCAN\n"
        string += indent(level + 1) + "variable: " + str(self.variable)
        return string

    def print_symtab(self, level):
        return ""

    def check(self):
        set_scope(self.variable, self.scope)
        var_type = self.variable.check()
        if (var_type is None):
            return False
        elif(self.variable.check() == "SET"):
            message = "ERROR: unsupported type '%s' for scan "
            message += "from line %d, column %d"
            s_lin, s_col = self.lexspan[1]
            data = str(self.variable), s_lin, s_col
            static_error.append(message % data)
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

        def ask_bool():
            raw = raw_input()
            raw = raw.strip(' \t\n\r')
            raw = raw.lower()
            if raw == 'true' or raw == 'false':
                return eval(raw.title())
            else:
                print "\nexpecting a bool value, try again."
                return ask_bool()

        symbol = self.scope.find(self.variable)
        if symbol.data_type == 'INT':
            value = ask_int()
        else:
            value = ask_bool()

        self.scope.update(self.variable, symbol.data_type, value)

def getKey(item):
    return item.evaluate()


class Print(Statement):
    """Write statement, for printing in standard output"""
    def __init__(self, lexspan, elements):
        self.lexspan = lexspan
        self.elements = elements

    def print_tree(self, level):
        if isinstance(self, PrintLn):
            string = indent(level) + "PRINTLN\n"
        else:
            string = indent(level) + "PRINT\n"

        for elem in self.elements:
            string += indent(level + 1) + "element:\n"
            string += elem.print_tree(level + 2) + '\n'

        return string[:-1]

    def print_symtab(self, level):
        return ""

    def check(self):
        boolean = True
        for elem in self.elements:
            set_scope(elem, self.scope)
            if elem.check() is None:
                boolean = False
        return boolean

    def execute(self):
        for elem in self.elements:
            intrp = elem.evaluate()
            if isinstance(intrp, bool):
                stdout.write(str(intrp).lower())
            elif isinstance(intrp, list):
                intrp.sort(key = getKey)
                out = "{"
                list_temp = []
                for i in intrp:
                    if i.evaluate() not in list_temp:
                        list_temp.append(i.evaluate())
                        out += str(i.evaluate())
                        out += ","
                if out[len(out)-1]==",":
                    out = out[:-1]
                out += "}"
                stdout.write(str(out))
            else:
                stdout.write(str(eval(str(intrp))))


class PrintLn(Print):
    """Writeln statement, Write with a new line at the end"""
    def __init__(self, lexspan, elements):
        Print.__init__(self, lexspan, elements)

    def execute(self):
        Print.execute(self)
        stdout.write('\n')


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st
        self.scope = None

    def print_tree(self, level):
        string = indent(level) + "IF\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "then:\n"
        string += self.then_st.print_tree(level + 2)
        if self.else_st:
            string += '\n' + indent(level + 1) + "else:\n"
            string += self.else_st.print_tree(level + 2)
        return string

    def print_symtab(self, level):
        string = self.then_st.print_symtab(level)
        if self.else_st:
            string += self.else_st.print_symtab(level)
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

    def execute(self):
        condition = self.condition.evaluate()
        if condition:
            self.then_st.execute()
        elif self.else_st:
            self.else_st.execute()

class For(Statement):
    """Declaracion for, funciona sobre conjuntos"""
    def __init__(self, lexspan, variable, in_set, statement, dire):
        self.lexspan = lexspan
        self.variable = variable
        self.in_set = in_set
        self.statement = statement
        self.dire = dire

    def print_tree(self, level):
        string = indent(level) + "FOR\n"
        string += indent(level + 1) + "variable: " + str(self.variable) + '\n'
        string += indent(level + 1) + str(self.dire) + ":\n"
        string += self.in_set.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string

    def print_symtab(self, level):
        return self.statement.print_symtab(level)

    def check(self):
        boolean = True
        for_sym_table = SymTable()
        for_sym_table.outer = self.scope
        self.scope.insert(self.variable, 'INT')
        set_scope(self.in_set, self.scope)
        set_scope(self.statement, for_sym_table)
        if(self.in_set.check() != "SET"):
            message = "ERROR: unsupported type '%s' for For "
            message += "from line %d, column %d"
            s_lin, s_col = self.lexspan[1]
            data = str(self.variable), s_lin, s_col
            static_error.append(message % data)
            boolean = False
        if self.statement.check() is False:
            boolean = False
        return boolean

    def execute(self):
        t_set_2 = copy.deepcopy(self.in_set.evaluate())
        t_set = []
        t_temp = []
        for i in t_set_2:
            if i.evaluate() not in t_temp:
                t_set.append(i)
                t_temp.append(i.evaluate()) 
        if self.dire == 'max' : t_set.sort(key = getKey,reverse = True)
        else: t_set.sort( key = getKey)
        for val in t_set: 
            self.statement.scope.find(self.variable).set_protected(False)
            self.scope.update(self.variable, 'INT', val.evaluate())
            self.scope.find(self.variable).set_protected(True)
            self.statement.execute()
            self.scope.find(self.variable).set_protected(False)


class While(Statement):
    """Declaracion while, toma una expresion"""
    def __init__(self, lexspan, condition, statement):
        self.lexspan = lexspan
        self.condition = condition
        self.statement = statement
        self.sym_table = None

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string


    def print_symtab(self, level):
        return self.statement.print_symtab(level)

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

    def execute(self):
        while self.condition.evaluate():
            self.statement.execute()


class Repeat(Statement):
    """Declaracion repeat, toma una expresion"""
    def __init__(self, lexspan, statement, condition):
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "REPEAT\n"
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        return string

    def print_symtab(self, level):
        return self.statement.print_symtab(level)

    def check(self):
        boolean = True
        set_scope(self.condition, self.scope)
        set_scope(self.statement, self.scope)
        exp_type = self.condition.check()
        if self.statement.check() is False:
            boolean = False
        if not error_invalid_expression(exp_type, self.condition,
                                     "'repeat' condition", 'BOOL'):
            boolean = False
        
        return boolean

    def execute(self):
        self.statement.execute()
        while self.condition.evaluate():
            self.statement.execute()

class RepeatWhile(Statement):
    """Declaracion repeat-while, toma una expresion"""
    def __init__(self,  lexspan, statement, condition, statement2):
        self.condition  = condition
        self.statement  = statement
        self.statement2 = statement2

    def print_tree(self, level):
        string = indent(level) + "REPEAT\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "WHILE \n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO:\n"
        string += self.statement2.print_tree(level + 2)
        return string

    def print_symtab(self, level):
        return self.statement.print_symtab(level)
        

    def check(self):
        boolean = True
        set_scope(self.condition, self.scope)
        set_scope(self.statement, self.scope)
        set_scope(self.statement2, self.scope)
        if self.statement.check() is False:
            boolean = False
        exp_type = self.condition.check()
        if not error_invalid_expression(exp_type, self.condition,
                                     "'repeat', 'while', condition", 'BOOL'):
            boolean = False
        if self.statement2.check() is False:
            boolean = False
        return boolean

    def execute(self):
        self.statement.execute()
        while self.condition.evaluate():
            self.statement2.execute()
            self.statement.execute()


class Expression: pass


class Variable(Expression):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
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

    def print_tree(self, level):
        return indent(level) + "VARIABLE: " + str(self.name)

    def print_symtab(self, level):
        string = ""
        return string

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

    def evaluate(self):
        symbol = self.scope.find(self)
        # if not symbol.initialized:
        #     message = "ERROR: variable '%s' not initialized"
        #     message += " at line %d, column %d"
        #     line, column = self.lexspan[0]
        #     data = self.name, line, column
        #     print message % data
        #     exit()
        return symbol.value


class Int(Expression):
    """Clase a definir un entero"""
    def __init__(self, lexspan, value):
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "INT: " + str(self.value)

    def print_symtab(self, level):
        string = ""
        return string

    def check(self):
        return 'INT'

    def evaluate(self):
        return self.value


class Bool(Expression):
    """Clase a definir un booleano"""
    def __init__(self, lexspan, value):
        self.lexspan = lexspan
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "BOOL: " + str(self.value)

    def print_symtab(self, level):
        string = ""
        return string

    def check(self):
        return 'BOOL'

    def evaluate(self):
        return eval(self.value.title())

class Set(Expression):
    """Clase a definir un conjunto"""
    def __init__(self, lexspan, values):
        self.lexspan = lexspan
        if values is not None:
            self.values = values
        else:
            self.values = []

    def __str__(self):
        return str(self.values)

    def print_tree(self, level):
        string = indent(level) + "VALORES:\n" 
        for i in self.values:
            string+= i.print_tree(level+1)+ '\n'
        return string

    def print_symtab(self, level):
        string = ""
        return string

    def check(self):
        if self.values is not None:
            for i in self.values:
                set_scope(i, self.scope)
                if i.check() != "INT":
                    error_unsuported_set(self.lexspan,i.check())
            return "SET"


    def evaluate(self):
        i = 0
       # while i < len(self.values):        
        #    self.values[i] = Int((0,0),self.values[i].evaluate())
         #   i=i+1
        return self.values

def error_unsuported_set(lexspan, type):
    message = "ERROR: unsupported type '%s' for interior of set "
    message += "from line %d, column %d"
    s_lin, s_col = lexspan
    data = str(operator), s_lin, s_col
    static_error.append(message % data)

class String(Expression):
    """Clase a definir una cadena de caracteres"""
    def __init__(self, lexspan, value):
        self.lexspan = lexspan
        self.value = value
        self.sym_table = None

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)

    def check(self):
        return 'STRING'

    def print_symtab(self, level):
        string = ""
        return string

    def evaluate(self):
        return self.value

def error_unsuported_binary(lexspan, operator, left, right):
    message = "ERROR: unsupported operator '%s' for types '%s' and '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(left), str(right), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)

def error_overflow(lexspan, operator):
    message = "ERROR: overflow in '%s' operation, "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), s_lin, s_col, e_lin, e_col
    print '\n\n', message % data
    exit()


# Checks that the left and right operator has any of the accepted layouts
def check_bin(lexspan, operator, left, right, types):
    count = 0
    count2 = 0
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
                return right
        if left != t_left:
            count2=count2+1
        if right != t_right:
            count=count+1
    if left is not None and right is not None:
        error_unsuported_binary(lexspan, operator, left, right)
        if(len(types)-1==count):
            return right
        elif(len(types)-1==count2):
            return left
    return None

class Binary(Expression):
    """Expresion binaria"""
    def __init__(self, lexspan, operator, left, right):
        self.lexspan = lexspan
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        string = str(self.operator) + ' ('
        string += str(self.left) + ', ' + str(self.right) + ')'
        return string

    def print_symtab(self, level):
        string = ""
        return string

    def print_tree(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += "operator: " + self.operator + '\n'
        string += indent(level + 1) + "left operand:\n"
        string += self.left.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "right operand:\n"
        string += self.right.print_tree(level + 2)
        return string

######        Operadores enteros        ######

class Plus(Binary):
    """Binary expressions with a '+'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "+", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('SET', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.check() == 'INT':
            value = left + right
            if not (-2147483648 <= value <= 2147483648):
                error_overflow(self.lexspan, self.operator)
            return value


class Minus(Binary):
    """Binary expressions with a '-'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "-", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        value = left - right

        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

class Times(Binary):
    """Binary expressions with a '*'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "*", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT'), ('SET', 'INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.check() == 'INT':
            value = left * right
            if not (-2147483648 <= value <= 2147483648):
                error_overflow(self.lexspan, self.operator)
            return value

class Divide(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if right == 0:
            error_division_by_zero(self.lexspan, self.operator)

        value = left / right
        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

class Module(Binary):
    """Binary expressions with a '%'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "%", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if right == 0:
            error_division_by_zero(self.lexspan, self.operator)

        value = left % right
        if not (-2147483648 <= value <= 2147483648):
            error_overflow(self.lexspan, self.operator)

        return value

######        Operadores sobre Conjuntos       ######

    ######       Entero sobre Conjuntos       ######
class Setplus(Binary):
    """Binary expressions with a '<+>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<+>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        for i in range(0,len(right)):
            right[i].value += left
        return copy.deepcopy(right)

class Setminus(Binary):
    """Binary expressions with a '<->'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<->", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        for i in range(0,len(right)):
            right[i].value -= left
        return copy.deepcopy(right)

class Settimes(Binary):
    """Binary expressions with a '<*>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<*>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        for i in range(0,len(right)):
            right[i].value *= left
        return copy.deepcopy(right)

class Setmod(Binary):
    """Binary expressions with a '<%>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<%>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left == 0:
            error_division_by_zero(self.lexspan, self.operator)
        for i in range(0,len(right)):
            right[i].value %= left
        return copy.deepcopy(right)

class Setdivition(Binary):
    """Binary expressions with a '</>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "</>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left == 0:
            error_division_by_zero(self.lexspan, self.operator)
        for i in range(0,len(right)):
            right[i].value /= left
        return copy.deepcopy(right)

######        Cojunto sobre Conjunto       ######

class Setintersection(Binary):
    """Binary expressions with a '><'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "><", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('SET', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        izq = self.left.evaluate()
        der = self.right.evaluate()
        if len(izq)>0:
            if len(der)>0:
                nuevo_izq = []
                nuevo_retorno = []
                for j in izq:
                    nuevo_izq.append(j.evaluate())
                i = 0  
                while i < len(der):
                    if der[i].evaluate() in nuevo_izq:
                        nuevo_retorno.append(Int(der[i].lexspan,der[i].evaluate()))
                    i = i+1  
                return nuevo_retorno  
            else:
                return der
        else:
            return izq
        

class Setunion(Binary):
    """Binary expressions with a '++'"""
    def __init__(self, lexspan, left, right):
        # self.type = "<>"
        Binary.__init__(self, lexspan, "++", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('SET', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        izq = self.left.evaluate()
        der = self.right.evaluate()
        if len(izq)>0:
            if len(der)>0:
                nuevo_izq = []
                nuevo_retorno = []
                for j in izq:
                    nuevo_izq.append(j.evaluate())
                i = 0  
                for j in izq:
                    nuevo_retorno.append(Int(j.lexspan,j.evaluate()))
                while i < len(der):
                    if der[i].evaluate() not in nuevo_izq:
                        nuevo_retorno.append(Int(der[i].lexspan,der[i].evaluate()))
                    i = i+1
                return nuevo_retorno  
            else:
                return izq
        else:
            return der



class Setdifference(Binary):
    """Binary expressions with a '\'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "\\", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('SET', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        izq = self.left.evaluate()
        der = self.right.evaluate()
        if len(izq)>0:
            if len(der)>0:
                nuevo_der = []
                nuevo_retorno = []
                for j in der:
                    nuevo_der.append(j.evaluate())
                i = 0  
                while i < len(izq):
                    if izq[i].evaluate() not in nuevo_der:
                        nuevo_retorno.append(Int(izq[i].lexspan,izq[i].evaluate()))
                    i = i+1  
                return nuevo_retorno  
            else:
                return izq
        else:
            return izq


######        Operadores Booleanos        ######

class Or(Binary):
    """Binary expressions with a 'or'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "or", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left or right

class And(Binary):
    """Binary expressions with a 'and'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "and", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left and right

class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left < right
        

class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)


    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left <= right


class Great(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)


    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left > right
        

class GreatEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left >= right


class Equal(Binary):
    """Binary expressions with a '=='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "==", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('SET', 'SET', 'BOOL'), ('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if (self.left.check() == self.right.check() == "SET"):
            right_temp = []
            left_temp = []
            for i in right:
                right_temp.append(i.evaluate())
            for i in left:
                left_temp.append(i.evaluate())
            for i in left:
                if i.evaluate() not in right_temp:
                    return False
            for i in right:
                if i.evaluate() not in left_temp:
                    return False
            return True
        else:
            return left == right


class Unequal(Binary):
    """Binary expressions with a '/='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'),
                       ('SET', 'SET', 'BOOL'), ('BOOL', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left != right

######        Operadores Booleanos sobre Conjuntos     ######


class Setbelong(Binary):
    """Binary expressions with a '@'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "@", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

    def evaluate(self):
        left = self.left.evaluate()
        t_set = self.right.evaluate()
        for i in t_set:
            if i.evaluate() == left: return True
        return False
###############################################################################

def error_unsuported_unary(lexspan, operator, operand):
    message = "ERROR: unsupported operator '%s' for type: '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(operand), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)

def error_division_by_zero(lexspan, operator):
    message = "ERROR: division by zero with in '%s' operation, "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), s_lin, s_col, e_lin, e_col
    print '\n\n', message % data
    exit()


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
    """Expresion unaria"""
    def __init__(self, lexspan, operator, operand):
        self.lexspan = lexspan
        self.operator = operator
        self.operand = operand

    def print_tree(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) + "operator: "
        string += str(self.operator) + '\n'
        string += indent(level + 1) + "operand:\n"
        string += self.operand.print_tree(level + 2)
        return string

###### Operadores Unarios ######

class UMinus(Unary):
    """Unary expressions with a '-'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "-", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('INT',)]
        return check_unary(self.lexspan, self.operator, operand, types)

    def evaluate(self):
        operand = self.operand.evaluate()
        return operand * -1

##### Operadores Unarios sobre Conjuntos ######

class Setmax(Unary):
    """Unary expressions with a '>?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, ">?", operand) 

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('SET','INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

    def evaluate(self):
        valor = self.operand.evaluate()
        if len(valor)>0:
            x = valor[0].evaluate()
            for i in valor:
                x = max(i.evaluate(),x)
            return x
        else:
            error_empty_set(self.lexspan, self.operator)

class Setmin(Unary):
    """Unary expressions with a '<?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "<?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('SET','INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

    def evaluate(self):
        valor = self.operand.evaluate()
        if len(valor)>0:
            x = valor[0].evaluate()
            for i in valor:
                x = min(i.evaluate(),x)
            return x
        else:
            error_empty_set(self.lexspan, self.operator)

def error_empty_set(lexspan, operator):
    message = "ERROR: empty set not permitted for '%s' operation, "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), s_lin, s_col, e_lin, e_col
    print '\n\n', message % data
    exit()

class SetLen(Unary):
    """Unary expressions with a '$?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "$?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('SET','INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

    def evaluate(self):
        t_set = self.operand.evaluate()
        return len(t_set)

class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "not", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('BOOL',)]
        return check_unary(self.lexspan, self.operator, operand, types)

    def evaluate(self):
        operand = self.operand.evaluate()
        return not operand