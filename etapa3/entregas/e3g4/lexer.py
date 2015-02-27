#!/usr/bin/python
#encoding: utf-8

#############################################################################
## 							   Proyecto traductores e Interpretadores  							   ##
##															    SETLAN												  		   ##
#############################################################################
#																																						#
#														---(Primera Entrega)---									 				#
#Integrantes:																																#
#		Nelson Saturno 09-10797																		 							#
#		Neylin Belisario 09-10093																	 							#
#												 																										#
#############################################################################


import re
import lex
import sys	

listaErrores =[]

# SE DEFINEN LAS PALABRAS RESERVADAS #
palabrasReservadas = {'program':'Program',
											'int':'Int',
					   					'bool':'Bool',
					   					'true':'True',
					   					'false':'False',
					   					'set':'Set',
											'using':'Using',
											'in':'In',
											'print':'Print',
											'scan':'Scan',
											'println':'PrintLn',
					   					'if':'If',
					   					'else':'Else',
					   					'else if':'ElseIf',
					   					'for':'For',
					   					'do':'Do',
					   					'min':'Min',
					   					'max':'Max',
					   					'repeat':'Repeat',
					   					'while':'While',
					   					'or':'Or',
					   					'and':'And',
					   					'not':'Not'}


# SE DEFINEN LA LISTA DE TOKENS #
tokens = ['Llave_Abre',
		  		'Llave_Cierra',
		  		'Pto_Coma',
		  		'ID',
		  		'Coma',
		  		'String',
		  		'Equal',
		  		'Suma',
		  		'Greater',
					'Less',
		  		'GreaterEqual',
		  		'LessEqual',
		  		'Par_Abre',
		  		'Par_Cierra',
		  		'Mult',
		  		'Equiv',
		  		'Resta',
		  		'Div',
		  		'Mod',
		  		'Union',
		  		'Dif',
		  		'Inter',
		  		'SumaConj',
		  		'RestaConj',
		  		'MultConj',
		  		'DivConj',
		  		'ModConj',
		  		'MaxConj',
		  		'MinConj',
		  		'NumElemConj',
		  		'NotEquiv',
		  		'IsInConj',
		  		'Number'] + list(palabrasReservadas.values())


# Se definen las expresiones regulares para cada token #
t_Llave_Abre = r'\{'
t_Llave_Cierra = r'\}'
t_Pto_Coma = r'\;'
t_Coma = r'\,'
t_Equal = r'\='
t_Suma = r'\+'
t_Par_Abre = r'\('
t_Par_Cierra = r'\)'
t_Mult = r'\*'
t_Resta = r'\-'
t_Div =r'\/'
t_Mod = r'\%'
t_Union = r'\+\+'
t_Dif = r'\\'
t_Inter = r'\>\<'
t_SumaConj = r'\<\+\>'
t_RestaConj = r'\<\-\>'
t_MultConj = r'\<\*\>'
t_DivConj = r'\<\/\>'
t_ModConj = r'\<\%\>'
t_MaxConj = r'\>\?'
t_MinConj = r'\<\?'
t_NumElemConj = r'\$\?'
t_Less = r'\<'
t_Greater = r'\>'
t_LessEqual = r'\<\='
t_GreaterEqual = r'\>\='
t_Equiv = r'\=\='
t_NotEquiv = r'\/\='
t_IsInConj = r'\@'
t_ignore = ' \t'

# Salto de linea
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Comentario
def t_COMMENT(t):
	r'\#.*'
	pass

# Token para Numero
def t_Number(t):
	r'-?\d{1,10}'
	t.value = int(t.value)    
	return t

# Token para Variable
def t_ID(t):
	r'[_a-zA-Z][a-zA-Z_0-9]*'
	t.type = palabrasReservadas.get(t.value,'ID')
	return t

# Token para Cadena de caracteres[^(\n)]
def t_String(t):
	r'\"(?:[^"\\\n]|\\.)*"|".*\\n".*"|".*\\/.*"|"[^"\n]*"'
	t.value=t.value[1:len(t.value)-1]
	return t

# Busca la columna en la que empieza la palabra
def find_column(input,token):
	last_cr = input.rfind('\n',0,token.lexpos)
	if last_cr < 0:
		last_cr = 0
	column = (token.lexpos - last_cr)
	return column

# Error
def t_error(t):
	listaErrores.append(t)
	t.lexer.skip(1)

# Funcion que verifica si se encontro algun error, en este caso se imprime en pantalla
# En caso contrario se imprimen los tokens encontrados.
def lexicografico(archivo):
	# Lista en la que se guardan los tokens encontrados en el archivo de texto
	tokensEncontrados =[]

	try:

		# Abrimos el archivo
		data = open(sys.argv[1])

		# Leemos el archivo
		data2 = data.read()

		# Construimos el lexer
		lexer = lex.lex()
		lexer.input(data2)

		# Vamos obteniendo los tokens y los guardamos en una lista
		while True:
			tok = lexer.token()
			if not tok: break
			tokensEncontrados.append(tok)

		# Cerramos el archivo
		data.close()

	except IOError:

		print 'ERROR: No se pudo abrir el archivo \"%s\".' % archivo
		exit()

	# Se imprimen los errores o tokens encontrados
	if (len(listaErrores) == 0):
		for a in tokensEncontrados:
			print "token " + a.type.upper(),
			if (a.type == "Llave_Cierra")|(a.type == "Llave_Abre")|\
				 (a.type == "GreaterEqual")|(a.type == "NumElemConj")|\
				 (a.type == "Par_Cierra")|(a.type == "LessEqual"):
				print "	value (",
			else:
				print "		value (",
			if (a.type == "ID")|(a.type == "String"):
				print "\""+a.value+"\"" + " )",
			else:
				print str(a.value) + " )",
			if (a.lineno > 1):
				print "(Linea " + str(a.lineno) + ", Columna " + \
							str(find_column(data2,a)) + ")"
			else:
				print "(Linea " + str(a.lineno) + ", Columna " + \
							str(find_column(data2,a)+1) + ")"
		lexer.lineno =1
	else:
		for b in listaErrores:
			if (b.lineno > 1):
				print "Error: Se encontró un caracter inesperado " + "'"+\
							b.value[0]+"'" + " en Linea " + str(b.lineno)+", Columna "+\
							str(find_column(data2,b)) + "."
			else:
				print "Error: Se encontró un caracter inesperado " + "'"+b.value[0]+\
							"'" + " en Linea " + str(b.lineno)+", Columna "+\
							str(find_column(data2,b)+1) + "."
			lexer.lineno =1
		exit()





