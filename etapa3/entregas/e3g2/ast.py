#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################

from Table import Table, indent

static_error = []

# Ajustar el alcance del simbolo
def set_scope(target,scope):
    if isinstance(target, Block):
        target.scope.outer = scope
    else:
        target.scope = scope

##################################
class Program:
    
    def __init__(self,lexspan,statement):
        self.statement = statement
        self.lexspan = lexspan
        self.scope = Table()

    def __str__(self):
        return "PROGRAM\n" + self.statement.print_tree(1)

    def check(self):
        set_scope(self.statement, self.scope)
        return self.statement.check()


class Statement(object): pass


def error_invalid_expression(exp_type, place, place_string, should):
    if exp_type != should and exp_type is not None:
        message = "ERROR: expresion de tipo '%s' en %s "
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

#################################################################

class Assign(Statement):
    
    def __init__(self,lexspan,variable,expression):
        self.variable = variable
        self.expression = expression
        self.lexspan = lexspan

    def print_tree(self, level):
        string =  indent(level) + "ASSIGN\n"
        string += indent(level + 1) + str(self.variable) +"\n"
        string += self.expression.print_tree(level + 1)
        return string


#############################################################################
######################COPIA DE CODIGO DE MATTEO FERRANDO#####################
#############################################################################

    def check(self):
        set_scope(self.variable, self.scope)
        set_scope(self.expression, self.scope)

        var_type = self.variable.check()
        exp_type = self.expression.check()

        aux = False
        if exp_type == 'TokenBool':
            aux = 'BOOL'
        if exp_type == 'TokenInt':
            aux = 'INT'
        if exp_type == 'TokenSet':
            aux = 'SET'

        if var_type is not None:
            var_info = self.scope.contains(self.variable)
            if var_info.protected:
                message = "ERROR: modificando la linea %d, columna %d "
                message += "valor de variable '%s' perteneciente a "
                message += "una declaracion for en la linea %d, y columna %d"
                var_lin, var_col = self.variable.lexspan[0]
                for_slin, for_scol = var_info.lexspan[0]
                data = var_lin, var_col, var_info.name, for_slin, for_scol
                static_error.append(message % data)

        if var_type is None or exp_type is None:
            return False

        if var_type != aux:
            message = "ERROR: asignando la expresion '%s' a la "
            message += "variable '%s' de tipo '%s' en la linea %d, y columna %d"
            message += " a la linea %d, y columna %d"
            s_lin, s_col = self.lexspan[0]
            e_lin, e_col = self.lexspan[1]
            data = (exp_type, self.variable.name, var_type,
                    s_lin, s_col, e_lin, e_col)
            static_error.append(message % data)
            return False

        return True

########################################################################

class Block(Statement):

    def __init__(self, lexspan, statements, scope=Table(),using=None,empty = None):
        self.lexspan = lexspan
        self.statements = statements
        self.scope = scope
        self.using = using
        self.empty = empty

    def print_tree(self, level):
        string = indent(level) + "BLOCK\n"

        if self.scope:
            string += self.scope.print_tree(level) + '\n'

        if self.using:
            string += indent(level + 1) + "USING\n"

        if (not(self.empty)):

            for stat in self.statements:
                string += stat.print_tree(level + 1) + '\n'
                string += indent(level + 1) + "SEPARATOR\n"
            string = string[:(-10 - len(indent(1)))]
            string += "BLOCK_END"
            return string

        string += indent(level) + "BLOCK_END"
        return string

    def check(self):
        boolean = True

        for stat in self.statements:
            set_scope(stat, self.scope)
            if stat.check() is False:
                boolean = False

        return boolean

######################################################################

class Scan(Statement):

    def __init__(self,lexspan, variable):
        self.variable = variable
        self.lexspan = lexspan

    def print_tree(self, level):
        string = indent(level) + "SCAN\n"
        string += indent(level + 1) + "variable: " + str(self.variable)
        return string

    def check(self):
        set_scope(self.variable, self.scope)
        var_type = self.variable.check()

        if var_type is None:
            return False
        else:
            return True

#######################################################################

class Print(Statement):

    def __init__(self,lexspan,elements):
        self.elements = elements
        self.lexspan = lexspan

    def print_tree(self, level):
        if isinstance(self, PrintLn):
            string = indent(level) + "PRINT\n"
        else:
            string = indent(level) + "PRINTLN\n"

        for elem in self.elements:
            string += indent(level + 1) + "element:\n"
            string += elem.print_tree(level + 2) + '\n'

        return string[:-1]

    def check(self):
        boolean = True

        for elem in self.elements:
            set_scope(elem, self.scope)
            if elem.check() is None:
                boolean = False

        return boolean

class PrintLn(Print):
    def __init__(self, lexspan, elements):
        Print.__init__(self, lexspan, elements)

#########################################################################

class If(Statement):

    def __init__(self,lexspan,condition,then_st,else_st=None):
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st
        self.lexspan = lexspan

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
                                        "'TokenIf' condition", 'TokenBool'):
            boolean = False

        if thn_type is False:
            boolean = False

        if self.else_st and els_type is False:
            boolean = False

        return boolean

####################################################################

class For(Statement):

    def __init__(self,lexspan, variable, direction, statement,token):
        self.variable = variable
        self.direction = direction
        self.statement = statement
        self.token     = token
        self.lexspan = lexspan

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

    def check(self):
        boolean = True

        for_scope = Table()
        for_scope.outer = self.scope
        for_scope.insert(self.variable, 'TokenInt', True)

        set_scope(self.direction, self.scope)
        set_scope(self.statement, for_scope)

        exp_type = self.direction.check()

        if not error_invalid_expression(exp_type, self.direction,
                                        "'for' min", 'TokenMin'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

class While(Statement):

    def __init__(self,lexspan, condition, statement):
        self.condition = condition
        self.statement = statement
        self.lexspan = lexspan

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string

    def check(self):
        boolean = True
        set_scope(self.condition, self.scope)
        set_scope(self.statement, self.scope)

        exp_type = self.condition.check()

        if not error_invalid_expression(exp_type, self.condition,
                                        "'while' condition", 'TokenBool'):
            boolean = False

        if self.statement.check() is False:
            boolean = False

        return boolean

##################################################

## LOS REPEATS NO TIENEN CHECKEO

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


class Expression(object): pass


class Variable(Expression):
    
    def __init__(self,lexspan, name):
        self.name = name
        self.lexspan = lexspan

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
        return indent(level) + "variable\n " + indent(level + 2) +str(self.name)

    def check(self):
        if self.scope.is_local(self):
            variable = self.scope.contains(self)
            #print self.scope.is_local(self)
            return variable.data_type
        else:
            message = "ERROR: la variable '%s' no esta en scope en la linea %d, y columna %d"
            line, column = self.lexspan[0]
            data = self.name, line, column
            static_error.append(message % data)
            return None

########################################################################

class Int(Expression):
    
    def __init__(self,lexspan, value):
        self.value = value
        self.lexspan = lexspan

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "int " + str(self.value)

    def check(self):
        return 'TokenInt'

#####################################################################

class Bool(Expression):
    
    def __init__(self,lexspan, value):
        self.value = value
        self.lexspan = lexspan

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "bool " + str(self.value)

    def check(self):
        return 'TokenBool'

####################################################################

class Set(Expression):
    
    def __init__(self,lexspan, values):
        self.values = values
        self.lexspan = lexspan

    def print_tree(self, level):
        string = indent(level) +"SET\n"
        for value in self.values:
            string += indent(level+1) + str(value) +"\n"
        return string

    def check(self):
        set_scope(self.values, self.scope)
        type_tuples = [('TokenInt', 'TokenSet', 'TokenSet')]
        return check_bin(self.lexspan, type_tuples)

######################################################################

class String(Expression):
    
    def __init__(self,lexspan, value):
        self.value = value
        self.lexspan = lexspan

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)

    def check(self):
        return 'STRING'

#######################################################################

def error_unsuported_binary(lexspan, operator, left, right):
    message = "ERROR: operador invalido '%s' para el tipo '%s' y '%s' "
    message += "de la linea %d, columna %d a la linea %d, columna %d"
    s_lin, s_col = lexspan[0]
    e_lin, e_col = lexspan[1]
    data = str(operator), str(left), str(right), s_lin, s_col, e_lin, e_col
    static_error.append(message % data)


# Revisa que le operador izquierdo y derecho acepten cualquier disposicion
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

    if left != right :
        if ((left == 'TokenInt' and right == 'INT') or
            (left == 'INT' and right == 'TokenInt') or

            (left == 'TokenBool' and right == 'BOOL') or
            (left == 'BOOL' and right == 'TokenBool')):
            pass
        else:
            if left is not None and right is not None:
                error_unsuported_binary(lexspan, operator, left, right)
                #print lexspan, " ",left," ", right
    return None

########################################################################

class Binary(Expression):
    
    def __init__(self,lexspan, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
        self.lexspan = lexspan

    def print_tree(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += self.operator + '\n'
        string += self.left.print_tree(level + 2) + '\n'
        string += self.right.print_tree(level + 2)
        return string
########################################################################

class Union(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "++", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenSet', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

########################################################################

class PlusMap(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<+>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

########################################################################

class MinusMap(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<->", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)
########################################################################

class DivideMap(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "</>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

########################################################################

class TimesMap(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<*>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

########################################################################

class ModuleMap(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<%>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

########################################################################

class SubSet(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "@", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenSet', 'TokenSet'), ('TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)


########################################################################


class Plus(Binary):
    
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "+", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Minus(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = "-"
        Binary.__init__(self, lexspan, "-", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Times(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = "*"
        Binary.__init__(self, lexspan, "*", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt'), ('TokenSet', 'TokenInt', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Divide(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = "/"
        Binary.__init__(self, lexspan, "/", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Modulo(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = "%"
        Binary.__init__(self, lexspan, "%", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Intersection(Binary):
    
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<>", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenSet', 'TokenSet')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Or(Binary):
    
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "or", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenBool', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class And(Binary):
    
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "and", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenBool', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Less(Binary):
    
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "<", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool'), ('TokenSet', 'TokenSet', 'TokenBool')]
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
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool'), ('TokenSet', 'TokenSet', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Great(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = ">"
        Binary.__init__(self, lexspan, ">", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class GreatEq(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = ">="
        Binary.__init__(self, lexspan, ">=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool'), ('TokenSet', 'TokenSet', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Equal(Binary):
    def __init__(self, lexspan, left, right):
        Binary.__init__(self, lexspan, "==", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool'),
                       ('TokenSet', 'TokenSet', 'TokenBool'), ('TokenBool', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################


class Unequal(Binary):
    
    def __init__(self, lexspan, left, right):
        # self.type = "/="
        Binary.__init__(self, lexspan, "/=", left, right)

    def check(self):
        set_scope(self.left, self.scope)
        set_scope(self.right, self.scope)
        left = self.left.check()
        right = self.right.check()
        type_tuples = [('TokenInt', 'TokenInt', 'TokenBool'),
                       ('TokenSet', 'TokenSet', 'TokenBool'), ('TokenBool', 'TokenBool')]
        return check_bin(self.lexspan, self.operator, left, right, type_tuples)

#######################################

def error_unsuported_unary(lexspan, operator, operand):
    message = "ERROR: mala operacion de '%s' de tipo: '%s' "
    message += "de la linea %d, columna %d a la linea %d, columna %d"
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

##########################################################################

class Unary(Expression):
    def __init__(self,lexspan, operator, operand):
        self.operator = operator
        self.operand = operand
        self.lexspan = lexspan

    def print_tree(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) 
        string += str(self.operator) + '\n'
        string += indent(level + 1) + "operand:\n"
        string += self.operand.print_tree(level + 2)
        return string

#########################################################################

class Not(Unary):
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "not", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('TokenBool',)]
        return check_unary(self.lexspan, self.operator, operand, types)

#########################################################################

class Minus(Unary):
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "-", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('TokenInt',)]
        return check_unary(self.lexspan, self.operator, operand, types)

#########################################################################

class MinValue(Unary):
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "<?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('TokenSet',)]
        return check_unary(self.lexspan, self.operator, operand, types)

#########################################################################

class MaxValue(Unary):
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, ">?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('TokenSet',)]
        return check_unary(self.lexspan, self.operator, operand, types)
#########################################################################

class NumberElements(Unary):
    def __init__(self, lexspan, operand):
        Unary.__init__(self, lexspan, "$?", operand)

    def check(self):
        set_scope(self.operand, self.scope)
        operand = self.operand.check()
        types = [('TokenSet',)]
        return check_unary(self.lexspan, self.operator, operand, types)
