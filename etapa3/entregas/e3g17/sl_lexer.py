# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Segunda entrega del proyecto.             #
#   Lexer para el lenguaje Setlan             #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

import ply.lex as lex

lexer = None
error_lex = []
lineas = []

# Declaración de tokens

tokens = (
		'PROGRAM',
		'LCURLY',
		'RCURLY',
		'LPAREN',
		'RPAREN',
		'PRINT',
		'PRINTLN',
		'IN',
		'USING',
		'INT',
		'BOOL',
		'SCAN',
		'IDENTIFIER',
		'COMMA',
		'SEMICOLON',
		'ASSIGN',
		'STRING',
		'PLUS',
		'MINUS',
		'IF',
		'ELSE',
		'TRUE',
		'OR',
		'AND',
		'NOT',
		'FALSE',
		'FOR',
		'REPEAT',
		'WHILE',
		'DO',
		'SET',
		'LESSTHAN',
		'GREATERTHAN',
		'LTOREQUAL',
		'GTOREQUAL',
		'EQUAL',
		'NOTEQUAL',
		'ASTERISK',
		#'DEF', #(NOT USED)
		#'RETURN', #(NOT USED)
		'INTDIV',
		'PERCENT',
		'ARROBA',
		'UNION',
		'INTERSECTION',
		'COMPLEMENT',
		'SETSUM',
		#'SETREST', #(NOT USED)
		'SETSUBSTRACT',
		'SETMULT',
		'SETDIV',
		'SETMOD',
		'SETMAX',
		'SETMIN',
		'SETLENGTH',
		'INTEGER',
		'MIN',
		'MAX',
	)

# Diccionario de reservadas

reserved = {
	'program' : 'PROGRAM',
	'print' : 'PRINT',
	'println' : 'PRINTLN',
	'using' : 'USING',
	'int' : 'INT',
	'bool' : 'BOOL',
	'scan' : 'SCAN',
	'if' : 'IF',
	'else' : 'ELSE',
	'in' : 'IN',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'or' : 'OR',
	'and' : 'AND',
	'not' : 'NOT',
	'for' : 'FOR',
	'repeat' : 'REPEAT',
	'while' : 'WHILE',
	'do' : 'DO',
	'set' : 'SET',
	#'def' : 'DEF', #(NOT USED)
	#'return' : 'RETURN', #(NOT USED)
	'min' : 'MIN',
	'max' : 'MAX'
}

# Reglas simples para reconocer los tokens

t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGN = r'='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_GTOREQUAL = r'>='
t_LTOREQUAL = r'<='
t_EQUAL = r'=='
t_NOTEQUAL = r"/="
t_ASTERISK = r'\*' 
t_ARROBA = r'@'
t_INTDIV = r'/'
t_PERCENT = r'%'
t_UNION = r'\+\+'
t_INTERSECTION = r'><'
t_COMPLEMENT = r'\\'
t_SETSUM = r'<\+>'
t_SETSUBSTRACT = r'<->'
t_SETMULT = r'<\*>'
t_SETDIV = r'</>'
t_SETMOD = r'<%>'
t_SETMAX = r'>\?'
t_SETMIN = r'<\?'
t_SETLENGTH = r'\$\?'
t_ignore  = ' |\t'

# Reglas más complicadas que requieren de función

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    i = 0
    while(i < len(t.value)):
    	if(t.value[i] == '\n'):
    		error.append(t)
    		break
    	i = i + 1
    while t.value.count(r'\"') > 0 :
        if t.value.count(r'\"') > 0:
            t.value = t.value[:t.value.find(r'\"')] + t.value[t.value.find(r'\"')+1:]
    aux = t.value.count(r'\\')
    while aux > 0 :
        if t.value.count(r'\\') > 0:
            t.value = t.value[:t.value.find(r'\\')] + t.value[t.value.find(r'\\')+1:]
            aux = aux - 1 
    return t

def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value,'IDENTIFIER')
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ignore_comment(t):
	r'\#.*'
	pass

# Función que atrapa expresiones no reconocidas

def t_error(t):
	global error_lex
	error_lex.append(t)  # Se incluyen en la lista de error
	t.lexer.skip(1)

def build_lexer(contenido):
	global lexer
	lexer = lex.lex()
	lexer.input(contenido)
	return lexer

def get_errors():
	return error_lex