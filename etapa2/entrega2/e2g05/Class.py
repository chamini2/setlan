#!/usr/bin/env python
# Modulo con  todas las clases que se usaran en el Parser.py

import sys

binary_symbol = {

						"+" 	: "Suma",
						"-" 	: "Resta",
						"*" 	: "Multiplicacion",
						"/" 	: "Division enteros",
						"%" 	: "Resto de la division",
						">" 	: "Mayor",
						">=" 	: "Mayor o igual",
						"<" 	: "Menor",
						"<=" 	: "Menor o igual",
						"==" 	: "Equivalencia",
						"/=" 	: "Distinto",
						"and"	: "Conjuncion",
						"or"	: "Disjuncion",
						"++" 	: "Union",
						"\\" 	: "Diferencia",
						"><"	: "Interseccion",
						"<+>"	: "Suma conjunto",
						"<->"	: "Resta conjunto",
						"<*>"	: "Multiplicacion conjunto",
						"</>"	: "Division conjunto",
						"<%>"	: "Resto conjunto",
						"@"	    : "Contencion conjunto",
						"min"	: "Orden Ascendente",
						"max"	: "Orden Descendente"
					}

# Funcion que se encarga de la espaciacion adecuada para la impresion

def spacing(espacio):
	i = 0
	while (i < 4):
		espacio += " "
		i += 1
	return espacio


# Clase Identificador

class Identifier:

	def __init__(self,name):		
		self.name = name

	def imprimir(self,espacio):
		print espacio,"   variable"
		print espacio,"       ", self.name


class Expresion_Not:

	def __init__(self,expresion):		
		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio,"   condition"
		print espacio,"      NOT not"
		self.expresion.imprimir(spacing(espacio))
# Clase  Numerico

class Numeric:

	def __init__(self,value):
		self.value = value

	def imprimir(self,espacio):
		print espacio,"    int"
		print espacio,"       ", self.value	

# Clase String

class String:

	def __init__(self,value):
		self.value = value
	
	def imprimir(self,espacio):
		print espacio,"  string"
		print espacio,"       ", self.value		
		

# Clase Booleano

class Boolean:

	def __init__(self,value):
		self.value = value

	def imprimir(self,espacio):
		print espacio,"     bool"
		print espacio,"       ", self.value		
		


class Set:

	def __init__(self,value):
		self.value = value

	def imprimir(self,espacio):
		print espacio,"  set\n",self.value

# Clase Declaracion de Variable
# t i
# t i = e (con inicializacion)

class Declaracion_Variable:

	def __init__(self,tipo,identifier,expresion=None):		
		self.tipo = tipo
		self.identifier = identifier		
		self.expresion = expresion

	def imprimir(self,espacio):
		if (isinstance(self.tipo,int) or isinstance(self.tipo,str)):
			print espacio,self.tipo
		else:
			self.tipo.imprimir(spacing(espacio))
		self.identifier.imprimir(spacing(espacio))			
 		if self.expresion:
			self.expresion.imprimir(spacing(espacio))


# Clase Asignacion

class Asignacion:

	def __init__(self,identifier,expresion):
		self.identifier = identifier

		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio,"ASSIGN\n"
		self.identifier.imprimir(spacing(espacio))
		self.expresion.imprimir(spacing(espacio))


# Clase Expresion Binaria
class Expresion_Binaria:

	def __init__(self,expresion1,operador,expresion2):
		self.expresion1 = expresion1
		self.expresion2 = expresion2
		self.operador  = operador
		

	def imprimir(self,espacio):
		s = binary_symbol[self.operador]
		print espacio,"'"+str(self.operador)+"'"

#Clase Unaria
class Expresion_Unaria:

	def __init__(self, operador, expresion):
		self.operador = operador
		self.expresion = expresion

	def imprimir(self, espacio):
		s = binary_symbol[self.operador]
		print espacio,s,"'"+str(self.operador)+"'"
		self.expresion.imprimir(spacing(espacio))

# Clase Scan
class Scan:

	def __init__(self,identifier):
		self.identifier = identifier
		
	def imprimir(self,espacio):
		print espacio,"SCAN"
   		self.identifier.imprimir(spacing(espacio))

class Using:

	def __init__(self,declaracion,instruccion):
		self.declaracion = declaracion
		self.instruccion = instruccion

	def imprimir(self,espacio):
		print espacio,"USING"
		for i in self.declaracion:
			i.imprimir(spacing(espacio))
		print espacio,"IN"
		for i in self.instruccion:
			i.imprimir(spacing(espacio))


# Clase Print
class Print:

	def __init__(self,expresion):
		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio,"PRINT"	
		for i in self.expresion:
			print espacio,"    elements"
			i.imprimir(spacing(espacio))

class Println:

	def __init__(self,expresion):
		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio,"PRINTLN"	
		for i in self.expresion:
			print espacio,"   elements"
			i.imprimir(spacing(espacio))
			print espacio,"\n"


# Clase If
class Condicional_Else:

	def __init__(self,instruccion):
		self.instruccion = instruccion		

	def imprimir(self,espacio):
		print espacio,"ELSE"
		for i in self.instruccion:
			i.imprimir(spacing(espacio))


# Clase If-Else
# if <condicion> then <instrucciones> else <instrucciones> 
class Condicional_If_Else:

	def __init__(self,condicion,instruccion1=None,instruccion2=None):
		self.condicion = condicion
		self.instruccion1 = instruccion1
		self.instruccion2 = instruccion2

	def imprimir(self,espacio):
		print espacio,"IF"
		print espacio,"  CONTAINS"
		self.condicion.imprimir(spacing(espacio))
		if self.instruccion1:
			for i in self.instruccion1:
				i.imprimir(spacing(espacio))

		if self.instruccion2:
			print espacio,"ELSE"
			for i in self.instruccion2:
				i.imprimir(spacing(espacio))


# Clase While
class Ciclo_While:

	def __init__(self,condicion,instruccion1):
		self.instruccion1 = instruccion1		
		self.condicion = condicion

	def imprimir(self,espacio):
		print espacio,"WHILE"
		print espacio,"  condition"
		self.condicion.imprimir(spacing(espacio))
		print espacio,"  DO"
		for i in self.instruccion1:
			i.imprimir(spacing(espacio))

class Ciclo_Repeat:

	def __init__(self,instruccion):
		self.instruccion = instruccion

	def imprimir(self,espacio):
		print espacio,"REPEAT"
		for i in self.instruccion:
			i.imprimir(spacing(espacio))

#Clase For
class Ciclo_For:
	def __init__(self,identificador,direccion,expresion,instruccion):
		self.identificador = identificador
		self.expresion = expresion
		self.direccion = direccion 
		self.instruccion = instruccion

	def imprimir(self,espacio):
		print espacio,"FOR"
		print espacio,"	variable"
		self.identificador.imprimir(spacing(espacio))
		print espacio,"	direction"
		print espacio,"     '"+str(self.direccion)+"'"	
		#self.direccion.imprimir(spacing(espacio))
		print espacio,"    IN"
		self.expresion.imprimir(spacing(espacio))
		print espacio, "   DO\n"
		for i in self.instruccion:
			i.imprimir(spacing(espacio))


class Program:

	def __init__(self,bloque = None):
		self.bloque = bloque
		
		# Imprime el programa
		self.imprimir("")
		
	def imprimir(self,espacio):
		print espacio,"PROGRAM\n"
		print espacio,"  BLOCK\n"
		self.bloque.imprimir(spacing(espacio))
		print espacio,"  BLOCK_END"




