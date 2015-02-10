"""Arbol Sintactico Abstracto del lenguaje Setlan
Fabio, Castro 10-10132
Antonio, Scaramazza 11-10957
"""

# Para colocar la identacion
def indent(level):
    return "    " * level


class Program:
    """Un programa consiste en expresiones"""
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return "PROGRAM\n" + self.statement.print_tree(1)


# Para heredar
class Statement: pass


class Assign(Statement):
    """Declaracion de asignacion"""
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def print_tree(self, level):
        string = indent(level) + "ASSIGN\n" + indent(level + 1)
        string += "variable: " + str(self.variable)
        string += "\n" + indent(level + 1)
        string += "value:\n" + self.expression.print_tree(level + 2)
        return string


class Block(Statement):
    """Declaracion de bloque"""
    def __init__(self, statements):
        self.statements = statements

    def print_tree(self, level):
        string = indent(level) + "BLOCK\n"
        for stat in self.statements:
            string += stat.print_tree(level + 1) + '\n'
            string += indent(level + 1) + "SEPARATOR\n"
        #string = string[:(-10 - len(indent(1)))]
        string += indent(level) + "BLOCK_END"
        return string


class Scan(Statement):
    """Declaracion scan, se aplica sobre una variable """
    def __init__(self, variable):
        self.variable = variable

    def print_tree(self, level):
        string = indent(level) + "SCAN\n"
        string += indent(level + 1) + "variable: " + str(self.variable)
        return string


class Print(Statement):
    """Comando 'print', muestra por pantalla las expresiones dadas"""
    def __init__(self, elements):
        self.elements = elements

    def print_tree(self, level):
        string = indent(level) + "PRINT\n"
        for elem in self.elements:
            string += indent(level + 1) + "element:\n"
            string += elem.print_tree(level + 2) + '\n'
        return string[:-1]


class If(Statement):
    """If statement"""
    def __init__(self, condition, then_st, else_st=None):
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


class For(Statement):
    """Declaracion for, funciona sobre conjuntos"""
    def __init__(self, variable, in_range, statement, dire):
        self.variable = variable
        self.in_range = in_range
        self.statement = statement
        self.dire = dire

    def print_tree(self, level):
        string = indent(level) + "FOR\n"
        string += indent(level + 1) + "variable: " + str(self.variable) + '\n'
        string += indent(level + 1) + str(self.dire) + ":\n"
        string += self.in_range.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string


class While(Statement):
    """Declaracion while, toma una expresion"""
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

class Repeat(Statement):
    """Declaracion repeat, toma una expresion"""
    def __init__(self, statement, condition):
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        return string

class RepeatWhile(Statement):
    """Declaracion repeat-while, toma una expresion"""
    def __init__(self, statement, condition, statement2):
        self.condition  = condition
        self.statement  = statement
        self.statement2 = statement2

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement2:\n"
        string += self.statement2.print_tree(level + 2)
        return string


class Expression: pass


class Variable(Expression):
    """Calse a definir una variable"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def print_tree(self, level):
        return indent(level) + "VARIABLE: " + str(self.name)


class Int(Expression):
    """Clase a definir un entero"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "INT: " + str(self.value)


class Bool(Expression):
    """Clase a definir un booleano"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "BOOL: " + str(self.value)


class Set(Expression):
    """Clase a definir un conjunto"""
    def __init__(self, valores):
        self.valores = valores

    def __str__(self):
        return str(self.valores) + '..' + str(self.valores)

    def print_tree(self, level):
        string = indent(level) + "VALORES:\n" 
        for i in self.valores:
            string+= i.print_tree(level+1)+ '\n'
        return string


class String(Expression):
    """Clase a definir una cadena de caracteres"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)


class Binary(Expression):
    """Expresion binaria"""
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def print_tree(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += "operator: " + self.operator + '\n'
        string += indent(level + 1) + "left operand:\n"
        string += self.left.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "right operand:\n"
        string += self.right.print_tree(level + 2)
        return string


class Unary(Expression):
    """Expresion unaria"""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def print_tree(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) + "operator: "
        string += str(self.operator) + '\n'
        string += indent(level + 1) + "operand:\n"
        string += self.operand.print_tree(level + 2)
        return string
