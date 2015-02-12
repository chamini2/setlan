#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Parser para el lenguaje Setlan
Fabio, Castro 10-10132
Antonio, Scaramazza 11-10957
"""

import ply.yacc as yacc
from lexer import tokens, lexer_error, find_column
from ast import *


# Primera regla a evaluar
# Un programa Setlan siempre comienza con la palabra reservada 'program'
def p_program(symbol):
    "program : PROGRAM statement"
    symbol[0] = Program(symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# Declaracion de asignacion
# ID '=' expresion
def p_statement_assing(symbol):
    "statement : ID ASSIGN expression"
    symbol[0] = Assign(Variable(symbol[1]), symbol[3])



# Declaracion de bloque
# posee un bloque opcional de declaracion de variables
# este comienza con 'using' y termina con 'in'
def p_statement_block(symbol):
    """statement : OPENCURLY statement_list CLOSECURLY
                 | OPENCURLY USING declare_list IN statement_list CLOSECURLY"""
    if len(symbol) == 4:
        symbol[0] = Block(symbol[2])
    else:
        # symbol[0] = Block(symbol[4], symbol[3])
        symbol[0] = Block(symbol[5])


# Regla de la gramatica para declarar el tipo de una variable
def p_statement_declare_list(symbol):
    """declare_list : data_type declare_comma_list SEMICOLON
                    | declare_list data_type declare_comma_list SEMICOLON"""
    if len(symbol) == 4:
        symbol[0] = [(symbol[2], symbol[1])]
    else:
        symbol[0] = symbol[1] + [(symbol[3], symbol[2])]


# Regla para crear una lista con el nombre de las variables
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : ID
                          | declare_comma_list COMMA ID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(symbol[3])]


# Las declaraciones se separan por un ';'
def p_statement_statement_list(symbol):
    """statement_list : 
                      | statement_list statement SEMICOLON"""
    if len(symbol) == 1:
        symbol[0] = []
    else:
        symbol[0] = symbol[1] + [symbol[2]]


# Tipos permitidos del lenguaje
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | SET """
    symbol[0] = symbol[1]

###############################     IN/OUT      ###############################


# Declaracion scan, se aplica sobre una variable 
def p_statement_scan(symbol):
    "statement : SCAN ID"
    symbol[0] = Scan(Variable(symbol[2]))


# Comando 'print', muestra por pantalla las expresiones dadas
def p_statement_print(symbol):
    """statement : PRINT comma_list
                 | PRINTLN comma_list"""
    if symbol[1].upper() == 'PRINT':
        symbol[0] = Print(symbol[2])
    else:
        if len(symbol) == 3:
            symbol[0] = Print(symbol[2] + [String('"\\n"')])
        else:
            symbol[0] = Print([String('"\\n"')])


# Lista de elementos a imprimir con la funcion 'print' 
def p_statement_comma_list(symbol):
    """comma_list : expression
                  | comma_list COMMA expression"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

############################     CONDICIONALES      #############################


# Declaracion 'IF', puedo o no haber 'ELSE"
def p_statement_if(symbol):
    """statement :  IF OPENPAREN expression CLOSEPAREN  statement ELSE statement
                  |   IF OPENPAREN expression CLOSEPAREN  statement  """
    if len(symbol) == 6:
        symbol[0] = If(symbol[3], symbol[5])
    else:
        symbol[0] = If(symbol[3], symbol[5], symbol[7])


###############################     LAZOS      #################################


# Declaracion for, la variable recorre el conjunto en la direccion indicada
def p_statement_for(symbol):
    """statement : FOR ID MAX expression DO statement
                 | FOR ID MIN expression DO statement"""
    symbol[0] = For(Variable(symbol[2]), symbol[4], symbol[6], symbol[3])


# Declaracion while-do, despues de pasar el chequeo de guarda,
# se realizan las expresiones en el bloque
def p_statement_while(symbol):
    "statement : WHILE OPENPAREN expression CLOSEPAREN DO statement"
    symbol[0] = While(symbol[3], symbol[6])

# Declaracion repeat-while, realiza las instruciones en el bloque,
# luego evalua la expresion en el while, si se cumple vuelve al bloque
def p_statement_repeat(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN "
    symbol[0] = Repeat(symbol[2], symbol[5])


# Combinacion de ambos lazos
def p_statement_repeat_while(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN DO statement"
    symbol[0] = RepeatWhile(symbol[2], symbol[5], symbol[8])


###############################################################################
#############################     EXPRESIONES     #############################
###############################################################################


# Precedencia de los operadores
precedence = (
    # lenguaje
    ("right", 'CLOSEPAREN'),
    ("right", 'ELSE'),
    # booleano
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),

    # comparador
    ("nonassoc", 'SETBELONG'),
    ("nonassoc", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
    # conjunto 
    ("left", 'SETUNION','SETDIFFERENCE'),
    ("left",'SETINTERSECTION'),
    ("right",'SETMAX','SETMIN','SETLEN'),
    # int sobre conjunto
    ("left", 'SETPLUS','SETMINUS'),
    ("left", 'SETTIMES','SETDIVITION','SETMOD'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULE'), 
    ("right", 'UMINUS'),
)

##############################     TIPOS     ###############################


# Numeros
def p_exp_int_literal(symbol):
    "expression : NUMBER"
    symbol[0] = Int(symbol[1])


# Booleanos
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    symbol[0] = Bool(symbol[1].upper())


# Conjuntos
def p_exp_set_literal(symbol):
    "expression : OPENCURLY comma_list CLOSECURLY"
    symbol[0] = Set(symbol[2])


# Cadena de caracteres
def p_exp_string_literal(symbol):
    "expression : STRING"
    symbol[0] = String(symbol[1])


# Variables
def p_expression_id(symbol):
    "expression : ID"
    symbol[0] = Variable(symbol[1])


# Expresiones entre parentesis
def p_expression_group(symbol):
    """expression : OPENPAREN expression CLOSEPAREN"""
    symbol[0] = symbol[2]

#############################    OPERADORES     ###############################


# Operadores bianrios de enteros
def p_exp_int_binary(symbol):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression
                  | expression MODULE expression"""
    operator = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '%': 'MODULE'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Menos unario para enteros
def p_exp_int_unary(symbol):
    "expression : MINUS expression %prec UMINUS" 
    symbol[0] = Unary('MINUS', symbol[2])


# Operadores binarios de conjuntos sobre conjuntos
def p_exp_set_binary(symbol):
    """expression : expression SETUNION expression
                  | expression SETINTERSECTION expression 
                  | expression SETDIFFERENCE expression """
    operator = {
        '++': 'SETUNION',
        '><': 'SETINTERSECTION',
        '\\': 'SETDIFFERENCE'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])  


# Operadores unarios de conjuntos
def p_exp_set_unary(symbol):
    """expression : SETMAX   expression 
                  | SETMIN   expression 
                  | SETLEN   expression """
    operator = {
        '>?': 'SETMAX',
        '<?': 'SETMIN',
        '$?': 'SETLEN'
    }[symbol[1]]              

    symbol[0] = Unary(operator, symbol[2]) 

# Operadores binarios de conjuntos sobre enteros
def p_exp_int_set_binary(symbol):
    """expression : expression SETPLUS   expression
                  | expression SETMINUS  expression
                  | expression SETTIMES  expression
                  | expression SETDIVITION expression
                  | expression SETMOD expression"""
    operator = {
        '<+>': 'SETPLUS',
        '<->': 'SETMINUS',
        '<*>': 'SETTIMES',
        '</>': 'SETDIVITION',
        '<%>': 'SETMOD',
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Operadores binarios sobre booleanos
def p_exp_bool_binary(symbol):
    """expression : expression OR      expression
                  | expression AND     expression"""
    operator = {
        'or': 'OR',
        'and': 'AND',
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# NOT unario para booleanos
def p_exp_bool_unary(symbol):
    "expression : NOT expression"
    if isinstance(symbol[2], Bool):
        expr = eval(symbol[2].value.title())
        expr = str(not expr).upper()
        symbol[0] = Bool(expr)
    else:
        symbol[0] = Unary(symbol[1].upper(), symbol[2])


# Operadores binarios de comparacion
def p_exp_bool_compare(symbol):
    """expression : expression LESS    expression
                  | expression LESSEQ  expression
                  | expression GREAT   expression
                  | expression GREATEQ expression
                  | expression EQUAL   expression
                  | expression UNEQUAL expression"""
    operator = {
        '<': 'LESS',
        '<=': 'LESSEQ',
        '>': 'GREAT',
        '>=': 'GREATEQ',
        '==': 'EQUAL',
        '/=': 'UNEQUAL'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Operador binario de entero en conjunto
def p_exp_bool_int_set(symbol):
    "expression : expression SETBELONG expression"
    symbol[0] = Binary('SETBELONG', symbol[1], symbol[3])


# Error a imprimir si el parser encuentra un error
def p_error(symbol):
    if symbol:
        text = symbol.lexer.lexdata
        message = "ERROR: Syntax error at line %d, column %d: "
        message += "Unexpected token '%s'"
        data = (symbol.lineno, find_column(text, symbol), symbol.value)
        parser_error.append(message % data)
    else:
        parser_error.append("ERROR: Syntax error at EOF")


# Generar el parser
parser = yacc.yacc(start='program')
parser_error = []


# EL archivo pasa por el parser, y es devuelto como el AST
def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)
    if parser.error:
        ast = None
    return ast

###############################################################################



def main(argv=None):
    import sys      # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No input file"
        return
    elif len(argv) > 3:
        print "ERROR: Invalid number of arguments"
        return

    if len(argv) == 3:
        debug = eval(argv[2])
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    ast = parsing(file_string, debug)

    if lexer_error:
        ast = None
        for error in lexer_error:
            print error
    elif parser_error:
        ast = None
        for error in parser_error:
            print error
    else:
        print ast

    return ast



if __name__ == "__main__":
    main()
