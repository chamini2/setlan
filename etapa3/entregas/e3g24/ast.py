#!/isr/bin/env python
# -*- coding: utf-8 -*-

####
#CI3725 - Etapa 1 - Análisis Lexicográfico
#Fabio, Castro, 10-10132
#Antonio, Scaramazza 11-10957
####

from SymTable import SymTable, indent


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

class Block(Statement):
    """Declaracion de bloque"""
    def __init__(self, lexspan, statements, scope=SymTable()):
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


class PrintLn(Print):
    """Writeln statement, Write with a new line at the end"""
    def __init__(self, lexspan, elements):
        Print.__init__(self, lexspan, elements)


class If(Statement):
    """If statement"""
    def __init__(self, lexspan, condition, then_st, else_st=None):
        self.lexspan = lexspan
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st


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

class For(Statement):
    """Declaracion for, funciona sobre conjuntos"""
    def __init__(self, lexspan, variable, in_set, statement, dire,scope=SymTable()):
        self.lexspan = lexspan
        self.variable = variable
        self.in_set = in_set
        self.statement = statement
        self.dire = dire
        self.scope = scope

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
        set_scope(self.in_set, self.scope)
        self.scope.insert(self.variable, 'INT')
        if(self.in_set.check() != "SET"):
            message = "ERROR: unsupported type '%s' for scan "
            message += "from line %d, column %d"
            s_lin, s_col = self.lexspan[1]
            data = str(self.variable), s_lin, s_col
            static_error.append(message % data)
            boolean = False
        set_scope(self.statement, self.scope)
        if self.statement.check() is False:
            boolean = False
        return boolean


class While(Statement):
    """Declaracion while, toma una expresion"""
    def __init__(self, lexspan, condition, statement):
        self.lexspan = lexspan
        self.condition = condition
        self.statement = statement

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



class Expression: pass


class Variable(Expression):
    """Class to define a variable"""
    def __init__(self, lexspan, name):
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

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)

    def check(self):
        return 'STRING'

    def print_symtab(self, level):
        string = ""
        return string

def error_unsuported_binary(lexspan, operator, left, right):
    message = "ERROR: unsupported operator '%s' for types '%s' and '%s' "
    message += "from line %d, column %d to line %d, column %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(left), str(right), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)


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
        check_bin(self.lexspan, self.operator, left, right, type_tuples)

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


class Setdifference(Binary):
    """Binary expressions with a '/'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "/", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('SET', 'SET')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)


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


class Less(Binary):
    """Binary expressions with a '<'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('SET', 'SET', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

class LessEq(Binary):
    """Binary expressions with a '<='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('SET', 'SET', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)


class Great(Binary):
    """Binary expressions with a '>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('SET', 'SET', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

class GreatEq(Binary):
    """Binary expressions with a '>='"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'INT', 'BOOL'), ('SET', 'SET', 'BOOL')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

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

######        Operadores Booleanos sobre Conjuntos     ######


class Setbelong(Binary):
    """Binary expressions with a '>>'"""
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, ">>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('INT', 'SET', 'BOOL')]
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


class Setmin(Unary):
    """Unary expressions with a '<?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "<?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('SET','INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

class SetLen(Unary):
    """Unary expressions with a '$?'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "$?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('SET','INT')]
        return check_unary(self.lexspan, self.operator, operand, types)

class Not(Unary):
    """Unary expressions with a 'not'"""
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "not", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('BOOL',)]
        return check_unary(self.lexspan, self.operator, operand, types)