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
    
    column = (t.lexpos - last_cr)
    return column    

#Retorna un string conteniendo la linea y la columna
def getLineAndColumn(code,t):
    return '(Línea {0}, Columna {1})' .format(t.lexer.lineno, find_column(code,t))

#Retorna el string necesario para la impresion
def getTokenString(code, t):
    return 'token {0:15} ({1})\t'.format(t.type, t.value) + getLineAndColumn(code,t)

#Token para los identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reservedWords.get(t.value,'IDENTIFIER')
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para los Numeros
def t_NUMBER(t):
    r'\d+'
    
    if int(t.value) > 2147483648:
        lexer_errorList.append('Error: overflow de un numero entero.' \
                                 + getLineAndColumn(t.lexer.lexdata,t)) 
    
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Token para los strings
def t_STRING(t):
    r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para Operadores de Conjuntos

def t_UNION(t):
    r'\+\+'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_DIFERENCE(t):
    r'\\'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MAXVALUE(t):
    r'>\?'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MINVALUE(t):
    r'<\?'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_NUMELEMENTS(t):
    r'\$\?'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_CONTAINMENT(t):
    r'@'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para los Operadores de Mapeo sobre Conjuntos
def t_PLUSMAP(t):
    r'<\+>'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MINUSMAP(t):
    r'<->'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_TIMESMAP(t):
    r'<\*>'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_DIVIDEMAP(t):
    r'</>'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MODULEMAP(t):
    r'<%>'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para los Operadores Simples
def t_PLUS(t):
    r'\+'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MINUS(t):
    r'\-'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_TIMES(t):
    r'\*'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_UNEQUAL(t):
    r'/='
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_DIVIDE(t):
    r'/'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_MODULE(t):
    r'%'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_EQUAL(t):
    r'=='
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_INTERSECTION(t):
    r'><'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_LESSEQ(t):
    r'<='
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_LESS(t):
    r'<'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_GREATEQ(t):
    r'>='
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_GREAT(t):
    r'>'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Token para los simbolos del lenguaje
def t_ASSIGN(t):
    r'='
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_COMMA(t):
    r','
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_SEMICOLON(t):
    r';'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para las expresiones
def t_LPARENTHESIS(t):
    r'\('
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_RPARENTHESIS(t):
    r'\)'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Tokens para los Bloques
def t_OPENCURLY(t):
    r'{'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

def t_CLOSECURLY(t):
    r'}'
    lexer_tokenList.append(getTokenString(t.lexer.lexdata,t))
    return t

#Manejo de errores  
def t_error(t):
    errorString  = 'Error: se encontro un caracter inesperado "{0}"' .format(t.value[0])
    errorString +=  getLineAndColumn(t.lexer.lexdata,t)
    lexer_errorList.append(errorString)
    t.lexer.skip(1)

#Lista de errores del Lexer
lexer_errorList = []
lexer_tokenList = []

#Constructor del lexer
lex.lex()

def build_lexer(code):
    lexer = lex.lex()

    #pasamos el codigo al lexer.
    lexer.input(code)

    # for tok in lexer:
    #     tokenList.append(tok)

    for tok in lexer_tokenList:
        print tok

if __name__ == '__main__':
    pass
