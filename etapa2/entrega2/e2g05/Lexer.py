#!/usr/bin/env python
#Lexer.py



import ply.lex as lexer
import sys


#Lista donde estaran los errores que encontremos.
list_error = []

# Palabras reservadas.
reserved = {
	'int' : 'tokint',
	'min' : 'tokmin',
	'max' : 'tokmax',
	'repeat' : 'tokrepeat',
	'false' : 'tokfalse',
	'true' : 'toktrue',
	'bool' : 'tokbool',
	'not' : 'toknot',
	'using' : 'tokusing',
	'print' : 'tokprint',
	'println' : 'tokprintln',
	'in' : 'tokin',
	'while' : 'tokwhile',
	'set' : 'tokset',
	'if' : 'tokif',
	'then' : 'tokthen',
	'else' : 'tokelse',
	'for' : 'tokfor',
	'do' : 'tokdo',
	'or' : 'tokor',
	'scan' : 'tokscan',
	'and' : 'tokand',
	'program' : 'tokprogram'

}

tokens = [
			'semicolon',
			'assignment',
			'comma',
			'greater',
			'equalsgreater',
			'less',
			'equalsless',
			'leftparen',
			'rightparen',
			'opencurly',
			'closecurly',
			'equals',
			'distinto',
			'plus',
			'minus',
			'multip',
			'div',
			'mod',
			'number',
			'id',
			'newline',
			'comment',
			'string',
			'arroba',
			'modset',
			'divset',
			'multipset',
			'minusset',
			'sumset',
			'intersection',
			'different',
			'union',
			'lenset',
			'maxset',
			'minset',
	] + list(reserved.values())


	# Definimos las expresiones regulares para cada uno de los tokens.

t_semicolon = r'\;'
t_assignment = r'\='
t_comma = r'\,'
t_greater = r'\>'
t_equalsgreater = r'\>='
t_less = r'\<'
t_equalsless = r'\<='
t_leftparen = r'\('
t_rightparen = r'\)'
t_opencurly = r'\{'
t_closecurly = r'\}'
t_equals = r'\=='
t_distinto = r'\/='
t_plus = r'\+'
t_minus = r'\-'
t_multip = r'\*'
t_div = r'\/'
t_mod = r'\%'
t_arroba = r'\@'
t_modset = r'\<\%>' 
t_divset = r'\</>' 
t_multipset = r'\<\*>'
t_minusset = r'\<\->' 
t_sumset = r'\<\+>' 
t_intersection = r'\>\<'
t_different = r'\\'
t_union = r'\+\+'
t_lenset = r'\$\?'
t_maxset =  r'>\?'
t_minset = r'<\?'

	# Para que no lea espacios y tabulaciones
t_ignore = '\n\t'


	# Convertir numero en entero 
def t_number(t):
	r'\d+'
	value = int(t.value)
	if (value > 2147483648):
		error_TokenNumber(t)
	t.value = value
	return t


def error_TokenNumber(t):
    text = t.lexer.lexdata
    message = "ERROR: Overflow for int '%s' at line %d, column %d"
    data = (t.value, t.lineno, find_column(text, t))
    lexer_error.append(message % data)

	# Los identificadores.
def t_id(t):
	r'[a-zA-Z][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'id') 
	return t


	# Los caracteres inesperados, los cuales no se encuentran en el lenguaje.
def t_error(t):
	list_error.append(t)
	t.lexer.skip(1)


def t_comment(t):
	r'\#[^\n][a-zA-Z][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'comment')
	pass

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

	#
	# Funcion que maneja una cadena de caracteres.
	#
def t_string(t):
	r'\"([^\\\n]|(\\.))*?\"'
	valor = t.value[1:len(t.value)-1]
	t.type = reserved.get(t.value,'string')
	return t

	#
	# Funcion que calcula el numero de columna en el que se encuentra un token.
	#
def column_token(input,token):
	last = input.rfind('\n',0,token.lexpos)
	if (last < 0):
		last = 1
		column = 1
	else:
		column = (token.lexpos - last)
	return column

	#
    # Constructor del lexer
    #

	# Simulador del analizador lexicografico de setlan.
def scanner(files,flag):
	# Lista para guardar los tokens que encuentre
	tokens_found = []	
	
	try:

	# Abrir el archivo de texto
		archivo = open(files)

			
		# Leer el archivo
		data = archivo.read()

		# Construimos el lexer
		l = lexer.lex()
		l.input(data)

		# Obtener y guardar los tokens
		while True:
			tok = lexer.token()
			if not tok: break
			# Se agrego el token a la lista 
			tokens_found.append(tok)

		archivo.close()

		return tokens_found

	except IOError:
			# Si no se pudo encontrar el archivo

		print 'ERROR: No se pudo abrir el archivo de texto \"%s\"' % archivo_texto
		exit()

		# Encontrar e imprimir errores lexicos. 
	if ((len(list_error) == 0) & flag):

		for i in tokens_found:
			print i
			if (i.type == 'string'):
				s1 = '(Linea: %d, Columna: %d) %s:(" %s  ")'
				print s1 % (i.lineno,column_token(data,i),i.type,i.value)
			elif (i.type == 'id'):
				s2 = "(Linea: %d, Columna: %d) %s:%s"
				print s2 % (i.lineno,column_token(data,i),i.type,i.value)

			elif (i.type == 'number'):
				s3 = "(Linea: %d, Columna: %d) %s: %d"
				print s3 % (i.lineno,column_token(data,i),i.type,i.value)
			else:
				s4 = "(Linea: %d, Columna: %d) %s (%s)"
				print s4 % (i.lineno,column_token(data,i),i.type,i.value)

		return 0

	else:

		for error in list_error:
			print error
			er = "ERROR: Caracter inesperado \"%s\" (Linea: %d, Columna: %d)"
			print er % (error.value[0],error.lineno,column_token(data,error))
						
		return 1

# END Lexer.py
