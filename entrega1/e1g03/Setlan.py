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
	'int':'int',
	'bool':'bool',
	'set':'set',
	'true':'True',
	'false':'False',
	'if':'IF',
	'then':'THEN',
	'else':'ELSE',
	'for':'FOR',
	'min':'MIN',
	'max':'MAX',
	'repeat':'repeat',
	'while':'while',
	'do':'do',
	'scan':'scan',
	'program':'program',
	'return':'return',
	'and':'and',
	'or':'or',
	'not':'not',
	'print':'print',
	'println':'println',
	'using':'using',
	'in':'in',
	}
#Declaramos los tokens
tokens = ('int', 'bool', 'set', 'ID', 'True', 'False', 'STRING', 'OPENCURLY', 
	'CLOSECURLY', 'QUOTES', 'BACKSLASH', 'IF', 'THEN', 'ELSE', 'MINUS', 
	'PLUS', 'EQUALS', 'LESS', 'GREATER', 'FOR', 'min', 'max', 'repeat', 
	'while', 'do', 'scan', 'program', 'return', 'TIMES', 'DIVIDE', 'MOD', 
	'UNION', 'INTERSECTION', 'PLUSSET', 'MINUSSET', 'TIMESSET',	'DIVIDESET', 
	'MODSET', 'COMPARE', 'AND', 'OR', 'NOT', 'LESSEQUALS', 'NUMBER',
	'GREATEREQUALS', 'NOTEQUALS', 'MAXSET', 'MINSET', 'NSET', 'AT', 'HASHTAG', 
	'COMMA', 'SEMICOLON', 'print', 'println', 'OPENPAREN', 'CLOSEPAREN', 
	'using', 'in')

#Definimos las reglas de los tokens
t_int = r'int'
t_bool = r'bool'
t_set = r'set'
t_True = r'true'
t_False = r'false'
t_STRING = r'".*?"'
t_OPENCURLY = r'{'
t_CLOSECURLY = r'}'
t_QUOTES = r'\"'
t_BACKSLASH = r'\\'
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
t_min = r'min'
t_max = r'max'
t_repeat = r'repeat'
t_while = r'while'
t_do = 'do'
t_scan = 'scan'
t_program = 'program'
t_return = 'return'
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
t_println = r'println'
t_print = r'print'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_using = r'using'
t_in = r'in'



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
	ERRORS.append("ERROR : SE ENCONTRO UN CARACTER INESPERADO "+
				  "\"%s\" EN LA LINEA %d, COLUMNA %d" 
				  % (t.value[0], t.lineno, t.lexpos))
	t.lexer.skip(1)

def t_NUMBER(t): # Definicion del Token NUMBER que reconoce a los numeros enteros
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
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
	if toke.type == "ID":
		TOKENS.append("Token_%s : \"%s\" (Linea %d, Columna %d)"
		 % (toke.type, toke.value, toke.lineno, toke.lexpos))
	elif toke.type == "STRING":
		TOKENS.append("Token_%s : %s (Linea %d, Columna %d)" 
			% (toke.type, toke.value, toke.lineno, toke.lexpos))
	elif toke.type == "NUMBER":
		TOKENS.append("Token_%s : %d (Linea %d, Columna %d)" 
			% (toke.type, toke.value, toke.lineno, toke.lexpos))
	else:
		TOKENS.append("Token_%s (Linea %d, Columna %d)" 
			% (toke.type, toke.lineno, toke.lexpos))

		#Imprimimos la lista de TOKENS en caso de que ERRORS este vacio, 
		#en caso contrario imprimimos ERRORS
if ERRORS == []:
	for i in TOKENS:
		print i
else:
	for i in ERRORS:
		print i