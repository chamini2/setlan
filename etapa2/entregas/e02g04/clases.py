#!/usr/bin/python
#encoding: utf-8

#############################################################################
## 							   Proyecto traductores e Interpretadores  							   ##
##															    SETLAN												  		   ##
#############################################################################
#																																						#
#														---(Segunda Entrega)---									 				#
#														 ANALIZADOR SINTÁCTICO													#
#																		Clases																	#
#Integrantes:																																#
#		Nelson Saturno 09-10797																		 							#
#		Neylin Belisario 09-10093																	 							#
#												 																										#
#############################################################################

import sys
#import numpy as np

# Funcion para impresion del tab
def Identacion(espacio):
	i = 0

	while (i < 4):	
		espacio +=  "  "
		i += 1

	return espacio;


# Clase que define PROGRAM
class Program:

	def __init__(self,cuerpo):
		self.cuerpo = cuerpo
		self.imprimir("")

	def imprimir(self,espacio):
		print espacio, "PROGRAM "
		self.cuerpo.imprimir(Identacion(espacio))
		print espacio, "PROGRAM_END"


# Clase que defina a los boolean
class Boolean:

	def __init__(self,value):
		self.value = value
		self.type = "boolean"

	def imprimir(self,espacio):
		print espacio, " String: ", self.value


# Clase que defina a los identificadores
class Identificador:

	def __init__(self,value):
		self.value = value
		self.type = "id"

	def imprimir(self,espacio):
		print espacio, "Variable ", str(self.value)


# Clase que define a los String
class String:

	def __init__(self,cadena):
		self.cadena = cadena
		self.type = "string"

	def imprimir(self,espacio):
		print espacio, "String ", self.cadena


# Clase que define a los Numeros
class Number:

	def __init__(self,numero):
		self.numero = numero
		self.type = "number"

	def imprimir(self,espacio):
		print espacio, "Number ", self.numero


# Clase que define los Booleanos
class Boolean:

	def __init__(self,value):
		self.value = value

	def imprimir(self,espacio):
		print espacio, "BOOLEAN: "
		print espacio, " Valor: ", str(self.value)	


# Clase que define ASIGN
class Asignacion_Conj:

	def __init__(self,identificador,expresion):
		self.expresion = expresion
		self.identificador = identificador

	def imprimir(self,espacio):
		print espacio, "ASIGNACION "
		self.identificador.imprimir(Identacion(espacio))
		print espacio, "Valor"
		print espacio, "Set"
		for j in self.expresion:
			j.imprimir(Identacion(espacio))


# Clase que define ASIGN
class Asignacion:

	def __init__(self,identificador,expresion):
		self.expresion = expresion
		self.identificador = identificador

	def imprimir(self,espacio):
		print espacio, "ASIGNACION "
		self.identificador.imprimir(Identacion(espacio))
		print espacio, "Valor"
		self.expresion.imprimir(Identacion(espacio))


# Clase que define la funcion Scan
class Scan_Entrada(object):

  def __init__(self,variable):
      self.variable = variable

  def imprimir(self,espacio):
      print espacio, "Expresion Scan: "
      print espacio, "Variable: "
      self.variable.imprimir(Identacion(espacio))
         
 
# Clase que define la funcion println
class ImprimirLn_Expresion:

  def __init__(self,ImprimeExpresion):
    self.ImprimeExpresion = ImprimeExpresion
  
  def imprimir(self, espacio):
    print espacio, "Expresion PrintLn: "
    print espacio, " Expresion: "
    if isinstance(self.ImprimeExpresion,list):
    	for j in self.ImprimeExpresion:
    		j.imprimir(Identacion(espacio))
    else:
    	self.ImprimeExpresion.imprimir(Identacion(espacio))
 
 
# Clase que define la funcion print
class Imprimir_Expresion:

  def __init__(self,ImprimeExpresion):
    self.ImprimeExpresion = ImprimeExpresion

  def imprimir(self,espacio):
    print espacio, "Expresion Print: "
    print espacio, " Expresion: "
    if isinstance(self.ImprimeExpresion,list):
    	for j in self.ImprimeExpresion:
    		j.imprimir(Identacion(espacio))
    else:
    	self.ImprimeExpresion.imprimir(Identacion(espacio))


# Clase que define INSTRUCCION unitaria
class Instruccion1:

	def __init__(self,asignacion):
		self.asignacion = asignacion

	def imprimir(self,espacio):
		print espacio, "INSTRUCCION "
		self.asignacion.imprimir(Identacion(espacio))


# Clase que define INSTRUCCION con otra
class Instruccion2:

	def __init__(self,next,instruccion=None):
		self.instruccion = instruccion
		self.next = next

	def imprimir(self,espacio):

		if self.instruccion:
			print espacio, "INSTRUCCION "
			self.instruccion.imprimir(Identacion(espacio))
		if self.next:
			print espacio, "INSTRUCCION "
			self.next.imprimir(Identacion(espacio))


# Clase que define la LISTA DE DECLARACIONES BASE
class Lista_Declaracion_Base:

	def __init__(self,tipo,identificador,expresion=None):
		self.tipo = tipo
		self.identificador = identificador
		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio, "Tipo: ", str(self.tipo)
		if isinstance(self.identificador,list):
			if len(self.identificador) > 1:
				print espacio, "IDs"
				for j in self.identificador:
					j.imprimir(Identacion(espacio))
			else:
				print espacio, "ID: "
				for j in self.identificador:
					j.imprimir(Identacion(espacio))
		else:
			print espacio, "ID: "
			self.identificador.imprimir(Identacion(espacio))

		if self.expresion:
			print espacio, "Valor:"
			print espacio, "Expresion: "
			self.expresion.imprimir(Identacion(espacio))



# Clase que define la LISTA DE DECLARACIONES
class Declaracion:

	def __init__(self,lista):
		self.lista = lista

	def imprimir(self,espacio):
		print espacio, "USING "
		for i in self.lista:
			i.imprimir(Identacion(espacio))
		print espacio, "IN "
		

 # Clase que define al BLOQUE
class Bloque:
	
	def __init__(self,declaracion,instruccion):
		self.declaracion = declaracion
		self.instruccion = instruccion

	def imprimir(self,espacio):
		print espacio, "BLOQUE "

		if self.declaracion:
			print espacio, "DECLARACION: "
			self.declaracion.imprimir(Identacion(espacio))

		if self.instruccion:
			print espacio, "INSTRUCCION bloque "
			for i in self.instruccion:
				i.imprimir(Identacion(espacio))
	
		print espacio, "BLOQUE_END"


# Clase que define la CONDICION
class Condicion:

	def __init__(self,cuerpo,expresion=None,condicion_Else=None,condicion_ElseIf=None):
		self.cuerpo = cuerpo
		self.expresion = expresion
		self.condicion_Else = condicion_Else
		self.condicion_ElseIf = condicion_ElseIf

	def imprimir(self,espacio):
		print espacio, "IF "
		print espacio, "condicion: "

		if self.expresion:
			self.expresion.imprimir(Identacion(espacio)) # imprime la condicion del if
			print espacio, "THEN "
		
		if isinstance(self.cuerpo,list):
			for j in self.cuerpo:
				print espacio, "Instruciones: "
				j.imprimir(Identacion(espacio)) #imprime las instrucciones del cuerpo
		else:
			print espacio, "Instruccion: "
			self.cuerpo.imprimir(Identacion(espacio))

		# si existe else if imprime
		if self.condicion_ElseIf:
			print espacio, "ELSE IF "
			if isinstance(self.condicion_ElseIf,list):
				for k in self.condicion_ElseIf:
					print espacio, "Instruciones: "
					k.imprimir(Identacion(espacio)) #imprime las instrucciones del else if
			else:
				print espacio, "Instruccion: "
				self.condicion_ElseIf.imprimir(Identacion(espacio))

		# si existe else imprime
		if self.condicion_Else:
			print espacio, "ELSE "
			if isinstance(self.condicion_Else,list):
				for l in self.condicion_Else:
					print espacio, "Instruciones: "
					l.imprimir(Identacion(espacio)) #imprime las instrucciones del else
			else:
				print espacio, "Instruccion: "
				self.condicion_Else.imprimir(Identacion(espacio))


# Clase que define El ciclo for
class Expre_For:

	#Constructor de la clase
	def __init__(self,identificador,direccion,rango,instructions):
		
		self.identificador = identificador	#Lista de identificadores
		self.instructions = instructions 	#Lista de instruction
		self.direccion = direccion
		self.rango = rango
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "Expresion For: "
		print espacio, " Variable: "
		self.identificador.imprimir(Identacion(espacio))
		print espacio, " Direccion: "
		print espacio, self.direccion
		print espacio, "In"
		if isinstance(self.rango,list):
			print espacio, "Set"
			for j in self.rango:
				j.imprimir(Identacion(espacio))
		else:
			self.rango.imprimir(Identacion(espacio))
			print espacio, "Do"

		if self.instructions:
			self.instructions.imprimir(Identacion(espacio))


# Clase que define El ciclo Repeat1
class Expre_Repeat1:

	#Constructor de la clase
	def __init__(self,instruccionRp,expression,instructionWh):
		
		self.instruccionRp = instruccionRp
		self.expression = expression 	
		self.instructionWh = instructionWh
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "Expresion Repeat: "
		print espacio, " Instrucion: "
		self.instruccionRp.imprimir(Identacion(espacio))
		print espacio, " Expresion While: "
		print espacio, " Condicion:"
		self.expression.imprimir(Identacion(espacio))
		print espacio, "Instrucion:"
		self.instructionWh.imprimir(Identacion(espacio))


# Clase que define El ciclo Repeat2
class Expre_Repeat2:

	#Constructor de la clase
	def __init__(self,expression,instructionWh):
		
		self.expression = expression 	
		self.instructionWh = instructionWh
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, " Expresion While: "
		print espacio, " Condicion:"
		self.expression.imprimir(Identacion(espacio))
		print espacio, "Instruciones:"
		self.instructionWh.imprimir(Identacion(espacio))


# Clase que define El ciclo Repeat1
class Expre_Repeat3:

	#Constructor de la clase
	def __init__(self,instruccionRp,expression):
		
		self.instruccionRp = instruccionRp
		self.expression = expression 	
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "Expresion Repeat: "
		print espacio, " Instruciones: "
		self.instruccionRp.imprimir(Identacion(espacio))
		print espacio, " Expresion While: "
		print espacio, " Condicion:"
		self.expression.imprimir(Identacion(espacio))


# Clase que define la EXPRESION UNARIA		
class Exp_Unaria:

	def __init__(self,expresion):	
		self.expresion = expresion 		#Lista de expresiones al lado der del operador 

	def imprimir(self,espacio):
		print espacio, "Operador: not "
		self.expresion.imprimir(Identacion(espacio))


# Clase que define la EXPRESION BINARIA
class Exp_Binaria:

	def __init__(self,exp_izq,operador,exp_der):
		
		self.exp_izq = exp_izq	#Lista de expresiones al lado izq del operador
		self.operador = operador 	
		self.exp_der = exp_der 		#Lista de expresiones al lado der del operador 

	def imprimir(self,espacio):
		print espacio, "Operador: ", str(self.operador)
		print espacio, " Expresion Izq: "
		self.exp_izq.imprimir(Identacion(espacio))
		print espacio, " Expresion Der: "
		self.exp_der.imprimir(Identacion(espacio))


