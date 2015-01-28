#!/usr/bin/env python
# CI-3725
# Proyecto I
# Primera Entrega 
# Lexer
# Autores:
# Alenxander Simoes 05-38956
# Jonathan Moreno 07-41249
#
# Version de Python 2.7.6
# Version de PLY 3.4

import sys
import re
import itertools
import ply.lex as lex

# Lista para guardar los errores encontrados en el recorrido del archivo
ListErrores = []

# C es la variable global donde se llevaran las cuentas de los espacios en blancos de cada linea
# anterior llevara la cuenta de los caracteres antes de llegar a un token

global C 
global anterior
global Cvieja

anterior = 1
C = 0
Cvieja = C

#Conjunto de palabras reservadas del Lenguaje Setlan
# las claves seran la expresion regular que las denotan
# y los valores representaran el identificador del token



reservadas = {
	'and' : 'TkAnd',
	'bool' : 'TkBool',
	'do' : 'TkDo',
	'else' : 'TkElse',
	'false' : 'TkFalse',
	'for' : 'TkFor',
	'if': 'TkIf',
	'in' : 'TkIn',
	'int' : 'TkInt',
	'max' : 'TkMax',
	'min' : 'TkMin',
	'not' : 'TkNot',
	'or' : 'TkOr',
	'print' : 'TkPrint',
	'println' : 'TkPrintLn',
	'program': 'TkProgram',
	'repeat' : 'TkRepeat',
	'scan' : 'TkScan',	
	'set': 'TkSet',
	'true': 'TkTrue',
	'using': 'TkUsing',
	'while': 'TkWhile',

}

#Lista con nombres de Tokens, mas la lista de reservadas
tokens = [
	'TkAbreLlave',
	'TkAbreParentesis',
	'TkAsignacion',
	'TkCadenaCaracteres',	
	'TkCierraLlave',
	'TkCierraParentesis',
	'TkContencion',
	'TkComa',
	'TkComentario',
	'TkDiferente',
	'TkDiv',
	'TkDivMapeada',
	'TkEquivalencia',
	'TkId',
	'TkInterseccion',
	'TkMayor',
	'TkMayorIgual',
	'TkMaxConjunto',
	'TkMenor',
	'TkMenorIgual',
	'TkMenos',
	'TkMenosMapeado',
	'TkMinConjunto',
	'TkMod',
	'TkModMapeado',
	'TkMultiplicacion',
	'TkMultiplicacionMapeada',
	'TkNumber',
	'TkRestaConjunto',
	'TkSecuenciacion',
	'TkSuma',
	'TkSumaMapeada',
	'TkTamConjunto',
	'TkUnion',
	
] + list(reservadas.values())



#Expresiones regulares para tokens simples


t_TkAbreLlave = r'\{'
t_TkAbreParentesis = r'\('
t_TkAsignacion = r'='		
t_TkCierraLlave = r'\}'
t_TkCierraParentesis = r'\)'
t_TkContencion = r'@'
t_TkComa = r','
t_TkDiferente = r'/='
t_TkDiv = r'/'
t_TkDivMapeada = r'</>'
t_TkEquivalencia = r'=='
t_TkInterseccion = r'><'
t_TkMayor = r'>'
t_TkMayorIgual = r'>='
t_TkMaxConjunto = r'>\?'
t_TkMenor = r'<'
t_TkMenorIgual = r'<='
t_TkMenos = r'-'
t_TkMenosMapeado = r'<->'
t_TkMinConjunto = r'<\?'
t_TkMod = r'%'
t_TkModMapeado = r'<%>'
t_TkMultiplicacion = r'\*'
t_TkMultiplicacionMapeada = r'<\*>'
t_TkRestaConjunto = r'\\'
t_TkSecuenciacion = r';'
t_TkSuma = r'\+'
t_TkSumaMapeada = r'<\+>'
t_TkTamConjunto = r'\$\?'
t_TkUnion = r'\+\+'

# Se definen a continuacion las expresiones regulares para casos mas 
# complejos

#Se definen los identificadores de variables

def t_TkId(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	t.type = reservadas.get(t.value,'TkId')
	return t

# Se construye la ER para los numeros (reales) del lenguaje

def t_TkNumber(t):
	r'(\d+)'
	t.value = int(t.value)
	return t	

#Se construye la ER para la cadena de caracteres

def t_TkCadenaCaracteres(t):
	r'"(([^"\n\\]*)|(.*(\\n|\\"|\\\\).*)+)"'
	t.type = reservadas.get(t.value,'TkCadenaCaracteres')
	return t

#Se ignoran las espacios en blanco (espacio y tab)
	
#t_ignore = ' \t'

#Permite ignorar los comentarios

def t_ignoredTkComentario(t):
	r'\#.*'
	pass

#Se define el salto de linea
def t_newline(t):
    r' \n+'
    t.lexer.lineno += len(t.value)

# Cada vez que se encuentra un TAB se incrementa en 4 la variable C 
# que se encarga de llevar la cuenta de espacios en blanco
def t_newtab(t):
	r' \t+'
	global C
	C = 4*len(t.value)
  
# Cada vez que se encuentra un TAB se incrementa en 1 la variable C 
# que se encarga de llevar la cuenta de espacios en blanco
# es importante que las verificaciones se hagan en este orden de codigo, 
# puesto que intercambiar el orden de las funciones cambiaria el resultado dela evaluacion de las expresiones    
def t_newblank(t):
	r' \s+'
	global C 
	C += 1*len(t.value)

#En caso de encontrarse un error se agrega a la lista de errores que luego seran impresos en pantalla
def t_error(t):
	global C
	aux = C
	print("C vale: " + str(C) + "Cvieja vale: " + str(Cvieja) + "\n" + "Anterior vale: " + str(anterior) + "\n")
	ListErrores.append([str(t.value[0]), str(t.lexer.lineno), str(find_column(anterior))])
	global Cvieja
	Cvieja = C
	global anterior
	if Cvieja == C:
		anterior = anterior + 1
	t.lexer.skip(1)

#Funcion para contar la columna de cada token
# Anterior es la longitud del token anterior mas su posicion, C se usa para llevar los espacios en blanco 
# de cada linea hasta el token sobre el cual se este investigando la columna

def find_column (anterior):
	return anterior + C

#Construccion del lexer
#
#
#Lista para guardar los tokens al ir recorriendo el archivo de entrada

ListTokens = []

#Se verificaque hayan suficientes argumentos para la entrada
if (len(sys.argv) > 1):
	
	#Se chequea la extension del archivo
	nombreArchivo = sys.argv[1]
	if re.match(".+\.stl",nombreArchivo):
		pass
	else:
		print("Error: el archivo de entrada debe ser de extension <.stl>, intente de nuevo" + "\n")
		sys.exit()
	print "\n" + "Leyendo el archivo de entrada: " + "<" + sys.argv[1] + ">" + "\n"
	
#Se abre el archivo de entrada
	archivo = open(sys.argv[1],'r')
	lex.lex()
	lexer = lex.lex()
	linea = archivo.readline()
	lexer.input(linea)
	
	
#Se lee la entrada, si no se consigue un token se pasa, en caso contrario se agrega a la lista
	while True:
		tok = lexer.token()
		Cvieja = C
		if not tok:
			anterior = 1
			pass
		else:
			while tok:
				col = find_column(anterior)
				anterior = anterior + len(str(tok.value))
				ListTokens.append([tok.type, tok.value, tok.lineno, col])
				tok = lexer.token()
				if not tok: 
					anterior = 1
					break
		linea = archivo.readline() 
		C = 0
		Cvieja = C
		anterior = 1
		lexer.input(linea)
		if not linea: break  	
else:
	print "Debes indicar el archivo de entrada, por favor intente de nuevo \n"

#Se imprimen solo los errores si hay alguno, en caso contrario se imprimen solo los tokens encontrados
if len(ListErrores)>0:
	for i in ListErrores:
		print ("Error: Caracter inesperado: " + i[0] + " " + "en la fila: " + i[1] +", columna: " + i[2] + "\n")
elif len(ListTokens)>0:
	print("A continuacion se muestran la lista de tokens, con su nombre, identificador, fila y columna: " + "\n")
	for j in ListTokens:
		print("Token --> "+ str(j[0]) + " " + ", Identificador: " + "'" + str(j[1])+ "'" + " " + ", en la fila: " + str(j[2]) + " " + ", columna: " + str(j[3]) + "\n")
else:
	print " No hay elementos para mostar \n" 
	
