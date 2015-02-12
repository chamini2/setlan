#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 22/01/2015
Ult. Modificacion el 07/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

import ply.lex as lex


#Palabras reservadas del Lenguaje
reservedWords = {
    #Lenguaje
	'program' : 'PROGRAM',
	'using'   : 'USING',
    'in'      : 'IN',
    'print'   : 'PRINT',
    'println' : 'PRINTLN',
    'scan'    : 'SCAN',

    #Control de flujo
    'if'      : 'IF',
    'else'    : 'ELSE',

    #Ciclos
    'for'     : 'FOR',
    'repeat'  : 'REPEAT',
    'while'   : 'WHILE',
    'do'      : 'DO',

    #Valores
	'true'    : 'TRUE',
	'false'   : 'FALSE',
    
    #Tipos
    'int'     : 'INT',
    'bool'    : 'BOOL',
    'set'     : 'SET',
    
    #Operadores    
    'min'     : 'MIN',
    'max'     : 'MAX', 
    'and'     : 'AND',
    'or'      : 'OR',
    'not'     : 'NOT',  
}

#Palabras a ser reconocidas
tokens = [
    #Lenguaje
    'ASSIGN',
    'COMMA',
    'SEMICOLON',

    #Identificador
    'IDENTIFIER',

    #Instrucciones
    'STRING',

    #Numeros
    'NUMBER',

    #Operadores Simples
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE',
    'EQUAL',
    'UNEQUAL',
    'LESS',
    'LESSEQ',
    'GREAT',
    'GREATEQ',

    #Operadores de Conjuntos
    'UNION',
    'INTERSECTION',
    'DIFERENCE',
    'MAXVALUE',
    'MINVALUE',
    'NUMELEMENTS',
    'CONTAINMENT',

    #Operadores de Mapeo sobre Conjuntos
    'PLUSMAP',
    'MINUSMAP',
    'TIMESMAP',
    'DIVIDEMAP',
    'MODULEMAP',

    #Expresiones
    'LPARENTHESIS',
    'RPARENTHESIS',

    #Bloques    
    'OPENCURLY',
    'CLOSECURLY'
] + list(reservedWords.values())

t_ignore = ' \t'
t_ignore_COMMENTS = r'\#.*' 

#Contamos el numero de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Calculamos el numero de columna en caso de error.
def find_column(code,t):
    last_cr = code.rfind('\n',0,t.lexer.lexpos)
    if last_cr < 0:
        last_cr = 0
    
    column = (t.lexpos - last_cr) + 1
    return column    

#Retorna un string conteniendo la linea y la columna
def getLineAndColumn(code,t):
    return '(Línea {0}, Columna {1})' .format(t.lexer.lineno, find_column(code,t))

#Token para los identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reservedWords.get(t.value,'IDENTIFIER')
    return t

#Tokens para los Numeros
def t_NUMBER(t):
    r'\d+'
    
    if int(t.value) > 2147483648:
        t.lexer.errorList.append('Error: overflow de un numero entero.' \
                                 + getLineAndColumn(t.lexer.lexdata,t)) 

    return t

#Token para los strings
def t_STRING(t):
    r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'
    return t

#Tokens para Operadores de Conjuntos

t_UNION = r'\+\+'
t_DIFERENCE = r'\\'
t_MAXVALUE = r'>\?'
t_MINVALUE = r'<\?'
t_NUMELEMENTS = r'\$\?'
t_CONTAINMENT = r'@'

#Tokens para los Operadores de Mapeo sobre Conjuntos
t_PLUSMAP = r'<\+>'
t_MINUSMAP = r'<->'
t_TIMESMAP = r'<\*>'
t_DIVIDEMAP = r'</>'
t_MODULEMAP = r'<%>'

#Tokens para los Operadores Simples
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_UNEQUAL = r'/='
t_DIVIDE = r'/'
t_MODULE = r'%'
t_EQUAL = r'=='
t_INTERSECTION = r'><'
t_LESS = r'<'
t_LESSEQ = r'<='
t_GREAT = r'>'
t_GREATEQ = r'>='

#Token para los simbolos del lenguaje
t_ASSIGN = r'='
t_COMMA = r','
t_SEMICOLON = r';'

#Tokens para las expresiones
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'

#Tokens para los Bloques
t_OPENCURLY = r'{'
t_CLOSECURLY = r'}'

#Manejo de errores  
def t_error(t):
    errorString  = 'Error: se encontro un caracter inesperado "{0}"' .format(t.value[0])
    errorString +=  getLineAndColumn(t.lexer.lexdata,t)
    lexer_errorList.append(errorString)
    t.lexer.skip(1)

#Lista de errores del Lexer
lexer_errorList = []

#Constructor del lexer
lex.lex()

def build_lexer(code):
    lexer = lex.lex()
    tokenList = []

    #pasamos el codigo al lexer.
    lexer.input(code)

    for tok in lexer:
        tokenList.append(tok)

if __name__ == '__main__':
    pass