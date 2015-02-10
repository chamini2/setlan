#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Lexer para el lenguaje Setlan
Fabio, Castro 10-10132
Antonio, Scaramazza 11-10957
"""

import ply.lex as lex

# Palabras reservadas del lenguaje
reserved = {
    # lenguaje
    'program' : 'PROGRAM',

    # tipos
    'int' : 'INT',
    'bool' : 'BOOL',
    'set' : 'SET',

    ## valores
    'true' : 'TRUE',
    'false' : 'FALSE',

    # instrucciones
    'using' : 'USING',
    'in' : 'IN',

    ## condicionales
    'if' : 'IF',
    'else' : 'ELSE',

    ## lazos
    'repeat' : 'REPEAT',
    'while' : 'WHILE',

    'do': 'DO',

    'for' : 'FOR',

    # Especiales del FOR

    'min':'MIN',
    'max':'MAX',

    ## entrada/salida
    'scan' : 'SCAN',

    'print' : 'PRINT',
    'println' : 'PRINTLN',

    # expresiones/operadores
    'or' : 'OR',
    'and' : 'AND',
    'not' : 'NOT',

    ## funciones
    #'def' : 'DEF',
    #'return': 'RETURN'
}

# Tokens a ser reconocidos
tokens = [
    # Lenguaje
    'NUMBER',
    'COMMA',
    'SEMICOLON',
    'ASSIGN',

    # IDENTIFICADORES
    'ID',

    # INSTRUCCIONES
    'STRING',

    # EXPRESIONES/OPERADORES
        # OPERADORES DE CONJUNTOS
            'SETPLUS',
            'SETMINUS',
            'SETTIMES',
            'SETMOD',
            'SETDIVITION',
            'SETMAX',
            'SETMIN',
            'SETLEN',
            'SETINTERSECTION',
            'SETUNION',
            'SETDIFFERENCE',
        # OPERADORES DE Enteros
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MODULE',
        #  OPERADORES BOOLEANOS
            'LESS',
            'LESSEQ',
            'GREAT',
            'GREATEQ',
            'EQUAL',
            'UNEQUAL',
            # OPERADORES BOOLEANOS SOBRE CONJUNTOS
                'SETBELONG',   
        #  PARENTIZACION
           'OPENPAREN',
           'CLOSEPAREN',
           'OPENCURLY',
           'CLOSECURLY'
] + list(reserved.values())



def t_NUMBER(token):
    r'\d+'
    val = int(token.value)
    if val > 2147483648:
        error_NUMBER(token)
    token.value = val
    return token

t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='

def t_ID(t):
    r'\w[\w\d]*'
    # Si no existen palabras reservadas que concuender, entonces es un Identificador
    t.type = reserved.get(t.value, 'ID')
    return t


# Los Strings almacenan toda entrada sin importar los saltos de linea
# Siempre que estas esten entre " "

t_STRING = r'\"([^\\\n]|(\\(n|"|\\)))*?\"'

# token de conjuntos
t_SETPLUS = r'\<\+\>'
t_SETMINUS = r'\<\-\>'
t_SETTIMES = r'\<\*\>'
t_SETDIVITION = r'\<\/\>'
t_SETMOD = r'\<\%\>'
t_SETMAX = r'\>\?'
t_SETMIN = r'\<\?'
t_SETLEN = r'\$\?'
t_SETINTERSECTION = r'\>\<'
t_SETUNION = r'\+\+'
t_SETDIFFERENCE = r'\\'

# token de entero
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'

# token de booleano
t_LESS = r'\<'
t_LESSEQ = r'\<\='
t_GREAT = r'\>'
t_GREATEQ = r'\>\='
t_EQUAL = r'\=\='
t_UNEQUAL = r'\/\='

#token de booleano sobre entero
t_SETBELONG = r'\@'

# parentizacion
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_OPENCURLY = r'\{'
t_CLOSECURLY = r'\}'

# Ignora espacion, tabuladores y comentarios en formato C
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

# El unico caracter de salto de linea a conciderar es "\n"
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Determinar el numero de columna en la linea actual
def find_column(text,token):
    last_cr = text.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

# Error a mostrar en caso de encontrar un caracter inseperado
def t_error(token):
    text = token.lexer.lexdata
    message = "Error: Se encontró un caracter inesperado '%s' en la línea %d, columna %d"    r'\d+'
    val = int(token.value)
    if val > 2147483648:
        error_NUMBER(token)

    token.value = val
    return token
    data = (token.value[0], token.lineno, find_column(text, token))
    lexer_error.append(message % data)
    token.lexer.skip(1)


# Error a mostrar número, número muy grande
def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "Error: Overflow for int '%s' at line %d, column %d"
    data = (token.value, token.lineno, find_column(text, token))
    lexer_error.append(message % data)

# Build the lexer
lex.lex()
lexer_error = []

###############################################################################


# The file (stored in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file_string, debug=0):

    lexer = lex.lex()
    tokens_list = []

    lexer.input(file_string, debug=debug)

    # Pass entire file through lexer
    for tok in lexer:
        tokens_list.append(tok)

    # If no "Unexpected character" or "Overflow" was found
    if not lexer_error:
        return tokens_list
    else:
        # Print all the errors
        for error in lexer_error:
            print error

        # Empty list to indicate error
        return []


# Only to be called if this is the main module
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
        debug = argv[2]
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    # Reads the file and passes it to the Lexer
    tokens_list = lexing(file_string, debug)

    for tok in tokens_list:
        print 'tok(' + str(tok.type) + ')' + '            '[:-(len(tok.type))],
        print 'val(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(file_string, tok))


# If this is the module running
if __name__ == "__main__":
    main()
