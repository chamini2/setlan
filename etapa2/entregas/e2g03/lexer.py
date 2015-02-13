#!/usr/bin/python
"""################################################
### Integrantes: Luis Diaz 11-10293				###
###				 Hosmar Colmenares 11-11211	    ###
###												###
### Universidad Simon Bolivar					###
### 	CI  3725								###
###												###
################################################"""


import ply.lex as lex
from sys import argv

script, filename = argv
text = open(filename)
ERRORS = []
TOKENS = []

#Reservamos las palabras para los tokens
reserved = {
	'int':'INT',
	'bool':'BOOL',
	'set':'SET',
	'true':'TRUE',
	'false':'FALSE',
	'if':'IF',
	'then':'THEN',
	'else':'ELSE',
	'for':'FOR',
	'min':'MIN',
	'max':'MAX',
	'repeat':'REPEAT',
	'while':'WHILE',
	'do':'DO',
	'scan':'SCAN',
	'program':'PROGRAM',
	'return':'RETURN',
	'and':'AND',
	'or':'OR',
	'not':'NOT',
	'print':'PRINT',
	'println':'PRINTLN',
	'using':'USING',
	'in':'IN',
	}
#Declaramos los tokens
tokens = ('INT', 'BOOL', 'SET', 'ID', 'TRUE', 'FALSE', 'STRING', 'OPENCURLY', 
	'CLOSECURLY', 'DIF', 'IF', 'THEN', 'ELSE', 'MINUS', 'PLUS', 'EQUALS',
	'LESS', 'GREATER', 'FOR', 'MIN', 'MAX', 'REPEAT', 'WHILE', 'DO', 'SCAN',
	'PROGRAM', 'RETURN', 'TIMES', 'DIVIDE', 'MOD', 'UNION', 'INTERSECTION', 
	'PLUSSET', 'MINUSSET', 'TIMESSET', 'DIVIDESET', 'MODSET', 'COMPARE', 'AND',
	'OR', 'NOT', 'LESSEQUALS', 'NUMBER', 'GREATEREQUALS', 'NOTEQUALS', 'MAXSET',
	'MINSET', 'NSET', 'AT', 'HASHTAG', 'COMMA', 'SEMICOLON', 'PRINT', 'PRINTLN',
	'OPENPAREN', 'CLOSEPAREN', 'USING', 'IN', 'OPENBRACKETS', 'CLOSEBRACKETS')

#Definimos las reglas de los tokens
t_INT = r'int'
t_BOOL = r'bool'
t_SET = r'set'
t_TRUE = r'true'
t_FALSE = r'false'
t_STRING = r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'
t_OPENCURLY = r'{'
t_CLOSECURLY = r'}'
t_DIF = r'\\'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_MINUS = r'-'
t_UNION = r'\+\+'
t_PLUS = r'\+'
t_COMPARE = r'=='
t_EQUALS = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_FOR = r'for'
t_MIN = r'min'
t_MAX = r'max'
t_REPEAT = r'repeat'
t_WHILE = r'while'
t_DO = 'do'
t_SCAN = 'scan'
t_PROGRAM = 'program'
t_RETURN = 'return'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%' 
t_INTERSECTION = r'><'
t_PLUSSET = r'<\+>'
t_MINUSSET = r'<->'
t_TIMESSET = r'<\*>'
t_DIVIDESET = r'</>'
t_MODSET = r'<%>'
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_LESSEQUALS = r'<='
t_GREATEREQUALS = r'>='
t_NOTEQUALS = r'/='
t_MAXSET = r'>\?'
t_MINSET = r'<\?'
t_NSET = r'\$\?'
t_AT = r'@'
t_HASHTAG = r'\#'
t_COMMA = r','
t_SEMICOLON = r';'
t_PRINTLN = r'println'
t_PRINT = r'print'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_USING = r'using'
t_IN = r'in'
t_OPENBRACKETS = r'\['
t_CLOSEBRACKETS = r'\]'


t_ignore = " \t" #Con esta definicion ignoraremos los espacios y tabuladores
t_ignore_comment = r'[#].*' # Con esta definicion ignoramos los comentarios

def t_newline(t): # Esta funcion lleva el conteo de las lineas
	r'\n+'
	t.lexer.lineno += len(t.value)

def find_column(input,token): #Esta funcion lleva el conteo de las columnas para cada linea
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
		last_cr = -1
    column = (token.lexpos - last_cr) 
    return column

def t_error(t): # Agrega a la lista ERRORS los tokens que no son aceptados por SETLAN
	t.lexpos = find_column(lexer.lexdata,t)
	ERRORS.append("ERROR : UNEXPECTED CHARACTER "+
				  "(%s) AT LINE %d, COLUMN %d" 
				  % (t.value[0], t.lineno, t.lexpos))
	t.lexer.skip(1)

def t_NUMBER(t): # Definicion del Token NUMBER que reconoce a los numeros enteros
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Line %d\t:\tNumber %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t

def t_ID(t): # Definicion del Token ID que reconoce a las variables
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')

    return t

lexer = lex.lex() #Creamos el lexer

lexer.input(text.read()) #Abrimos el archivo a leer

while True: #Agregamos los Tokens a las listas TOKENS o ERRORS dependiendo de su tipo
	toke=lexer.token()

	if not toke: break
	toke.lexpos = find_column(lexer.lexdata,toke)
	TOKENS.append("Token_%s :  value (%s) at (Line %d, Column %d)"
		 % (toke.type, toke.value, toke.lineno, toke.lexpos))

		#Imprimimos la lista de TOKENS en caso de que ERRORS este vacio, 
		#en caso contrario imprimimos ERRORS
#if ERRORS == []:
#	for i in TOKENS:
#		print i
else:
	for i in ERRORS:
		print i