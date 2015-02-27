#!/usr/bin/python
#encoding: utf-8

#############################################################################
## 							   Proyecto traductores e Interpretadores  							   ##
##															    SETLAN												  		   ##
#############################################################################
#																																						#
#														---(Tercera Entrega)---									 				#
#														 ANALIZADOR SINTÁCTICO													#
#																		Clases																	#
#Integrantes:																																#
#		Nelson Saturno 09-10797																		 							#
#		Neylin Belisario 09-10093																	 							#
#												 																										#
#############################################################################

import sys

# DICCIONARIO DE SIMBOLOS
# Se declaran estos simbolos para usarlos en las clases

DicSimbolos = {	
							"+" : "Suma",
							"-" : "Resta",
							"*" : "Mult",
							"/"	: "Div",
							"%" : "Mod",
							"++" : "Union",
							"\\" : "Dif",
							"><" : "Inter",
							"<+>" : "SumaConj",
							"<->" : "RestaConj",
							"<*>" : "MultConj",
							"</>" : "DivConj",
							"<%>" : "ModConj",
							"==" : "Equiv",
							">" : "Greater",
							"<" : "Less",
							">=" : "GreaterEqual",
							"<=" : "LessEqual",
							"@" : "IsInConj",
							"/=" : "NotEquiv",
							"&" : "And",
							"|" : "Or",
							} 

# TABLA DE SIMBOLOS
class TablaSimbolos:

	def __init__(self,padre):
		self.dic = {}
		self.hijos = []
		self.padre = padre

	def contains(self,key):
		if self.dic.has_key(key):
			return True

		if self.padre <> None:
			return self.padre.contains(key)
		else:
			return False

	def Tipo(self,key):
		if self.dic.has_key(key):
			return self.dic[key]

		if self.padre <> None:
			return self.padre.Tipo(key)

		else:
			return "NotDeclared"

	def imprimir(self,espacio):
		print self.dic

		if self.hijos:
			for i in self.hijos:
				i.imprimir(Identacion(espacio))

	def insert(self,key,value):
		if self.dic.has_key(key):
			sys.exit(1)

		self.dic[key] = value

	def born(self,hijo):
		self.hijos.append(hijo)


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
		New_TS = TablaSimbolos(None)
		self.type_check(New_TS)

	def imprimir(self,espacio):
		print espacio, "PROGRAM "
		self.cuerpo.imprimir(Identacion(espacio))
		print espacio, "PROGRAM_END"

	def type_check(self,TablaSimbolos):
		self.cuerpo.type_check(TablaSimbolos)


# Clase que defina a los boolean
class Boolean:

	def __init__(self,value):
		if value == None:
			self.value = "false"
		else:
			self.value = value						
		self.type = "boolean"

	def getValue(self):
		return self.value

	def imprimir(self,espacio):
		print espacio, " String: ", str(self.value)

	def type_check(self,TablaSimbolos):
		return self.type

# Clase que defina a los identificadores
class Identificador:

	def __init__(self,value):
		self.value = str(value)
		self.type = "id"

	def getValue(self):
		return self.value

	def imprimir(self,espacio):
		print espacio, "Variable ", str(self.value)

	def type_check(self,TablaSimbolos):
		if TablaSimbolos.contains(self.value) == False:
			print "ERROR: El identificador no se encuentra en la Tabla de Simbolos: " + str(self.value)
			sys.exit(1)

		return TablaSimbolos.Tipo(self.value)


# Clase que define a los String
class String:

	def __init__(self,cadena):
		self.cadena = cadena
		self.type = "string"

	def getValue(self):
		return self.cadena

	def imprimir(self,espacio):
		print espacio, "String ", self.cadena

	def type_check(self,TablaSimbolos):
		return self.type


# Clase que define a los Numeros
class Number:

	def __init__(self,numero):
		if numero == None:
			self.numero = 0
		else:
			self.numero = numero
		self.type = "int"

	def getValue(self):
		return self.numero

	def imprimir(self,espacio):
		print espacio, "Number ", self.numero

	def type_check(self,TablaSimbolos):
		return self.type


# Clase que define a los Conjuntos
class Sets:

	def __init__(self,lista):
		self.lista = lista
		self.type = "set"

	def getValue(self):
		return self.lista

	def imprimir(self,espacio):
		print espacio, "Set "
		print espacio, "Valor(es)"
		if isinstance(self.lista,list):
			for i in self.lista:
				i.imprimir(Identacion(espacio))
		else:
			self.lista.imprimir(Identacion(espacio))

	#############
	#  REVISAR
	
	def type_check(self,TablaSimbolos):
		if isinstance(self.lista,list):
			for i in self.lista:
				if i.type_check(TablaSimbolos):
					pass
				else:
					print "ERROR: No se puede asignar '" + str(i) + \
								"' al dentro del conjunto"
  	 			sys.exit(1)
			return self.type

	#############


# Clase que define a los conjuntos
# class Set_Conj:

# 	def __init__(self,identificador,listaNum):
# 		self.identificador = identificador 
# 		self.listaNum = listaNum

# 	def imprimir(self,espacio):
# 		self.identificador.imprimir(Identacion(espacio))
# 		print espacio, "Set "
# 		if self.listaNum:
# 			for j in self.listaNum:
# 				j.imprimir(Identacion(espacio))

# 	def type_check(self,TablaSimbolos):
# 		if TablaSimbolos.contains(self.identificador.getValue()) == False:
# 			print "ERROR: La variable '" + str(self.identificador.getValue()) + "' no ha sido declarada"
# 			sys.exit(1)

# 		else:
# 			Tipo_id = self.identificador.type_check(TablaSimbolos)
# 			Tipo_lista = self.listaNum.type_check(TablaSimbolos)

# 			#if Tipo_id == "number" or Tipo_id == "boolean" or Tipo_lista == "number" or Tipo_lista == "boolean":
# 			if Tipo_id <> Tipo_lista:
# 				print "ERROR: El tipo del identificador y de la expresion son distintos"
# 				sys.exit(1)


#Clase que define una expresion de tipo conjunto
class Expre_Conjunto:

	def __init__(self,expresion):
		self.expresion = expresion

	def imprimir(self,espacio):
		print espacio, "Conjunto"
		print espacio, "Valor(es)"
		if self.expresion:
			for j in self.expresion:
				j.imprimir(Identacion(espacio))

	def type_check(self,TablaSimbolos):
		if isinstance(self.expresion,list):
			for i in self.expresion:
				i.type_check(TablaSimbolos)
		else:
			self.expresion.type_check(TablaSimbolos)


# Clase que define ASIGN
class Asignacion_Conj:

	def __init__(self,identificador,expresion):
		self.expresion = expresion
		self.identificador = identificador

	def imprimir(self,espacio):
		print espacio, "ASIGNACION "
		self.identificador.imprimir(Identacion(espacio))
		self.expresion.imprimir(Identacion(espacio))
		# print espacio, "Valor"
		# print espacio, "Set"
		# if self.expresion:
		# 	for j in self.expresion:
		# 		j.imprimir(Identacion(espacio))

	def type_check(self,TablaSimbolos):
		if TablaSimbolos.dic.has_key(self.identificador.getValue()) == False:
			print "ERROR: Variable '" + str(self.identificador.getValue()) + "' no esta declarada dentro del alcance"
			sys.exit(1)

		else:
			Tipo_id = self.identificador.type_check(TablaSimbolos)
			Tipo_exp = self.expresion.type_check(TablaSimbolos)

			#if Tipo_id == "number" or Tipo_id == "boolean" or Tipo_exp == "number" or Tipo_exp == "boolean":
			if Tipo_id <> Tipo_exp:
				print "ERROR: El tipo del identificador y de la expresion son distintos"
				sys.exit(1)

		TablaSimbolos.insert(self.identificador.getValue(),self.expresion)


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

	def type_check(self,TablaSimbolos):
		if TablaSimbolos.contains(self.identificador.getValue()) == False:
			print "ERROR: La variable '" + str(self.identificador.getValue()) + "' no ha sido declarada"
			sys.exit(1)

		else:
			Tipo_id = self.identificador.type_check(TablaSimbolos)
			print Tipo_id, "tipo id"
			Tipo_exp = self.expresion.type_check(TablaSimbolos)
			print Tipo_exp, "tipo exp"

			#if Tipo_id == "number" or Tipo_id == "boolean" or Tipo_exp == "number" or Tipo_exp == "boolean":
			if Tipo_id <> Tipo_exp:
				print "ERROR: El tipo del identificador y de la expresion son distintos"
				sys.exit(1)


		TablaSimbolos.insert(self.identificador.getValue(),self.expresion)


# Clase que define la funcion Scan
class Scan_Entrada(object):

  def __init__(self,variable):
    self.variable = variable

  def imprimir(self,espacio):
    print espacio, "SCAN "
    self.variable.imprimir(Identacion(espacio))

  def type_check(self,TablaSimbolos):
  	if TablaSimbolos.contains(self.variable.getValue()) == False:
  		print "ERROR: El valor de la variable '" + str(self.variable) + "' no coincide con SCAN"
         
 
# Clase que define la funcion println
class ImprimirLn_Expresion:

  def __init__(self,ImprimeExpresion):
    self.ImprimeExpresion = ImprimeExpresion
  
  def imprimir(self,espacio):
    print espacio, "PRINTLN: "
    if isinstance(self.ImprimeExpresion,list):
    	for j in self.ImprimeExpresion:
    		j.imprimir(Identacion(espacio))
    else:
    	self.ImprimeExpresion.imprimir(Identacion(espacio))
    print espacio, "	 String  \\n"

  def type_check(self,TablaSimbolos):
  	for i in self.ImprimeExpresion:
  		i.type_check(TablaSimbolos)
 
 
# Clase que define la funcion print
class Imprimir_Expresion:

  def __init__(self,ImprimeExpresion):
    self.ImprimeExpresion = ImprimeExpresion

  def imprimir(self,espacio):
    print espacio, "PRINT: "
    if isinstance(self.ImprimeExpresion,list):
    	for j in self.ImprimeExpresion:
    		j.imprimir(Identacion(espacio))
    else:
    	self.ImprimeExpresion.imprimir(Identacion(espacio))

  def type_check(self,TablaSimbolos):
  	for i in self.ImprimeExpresion:
  		i.type_check(TablaSimbolos)


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

	def type_check(self,TablaSimbolos):
		for i in self.identificador:
			if TablaSimbolos.dic.has_key(i.getValue()):
				print "ERROR: Variable declarada dentro del alcance"
				sys.exit(1)

			else:
				if isinstance(self.tipo,Number) or isinstance(self.tipo,Boolean) or \
					 isinstance(self.tipo,Sets):
					if i.type_check(TablaSimbolos) <> self.tipo:
						print "ERROR: El tipo del identificador y la expresion son distintos"
						sys.exit(1)

			TablaSimbolos.insert(i.getValue(),self.tipo)


# Clase que define la LISTA DE DECLARACIONES
class Declaracion:

	def __init__(self,lista):
		self.lista = lista

	def imprimir(self,espacio):
		print espacio, "USING "
		for i in self.lista:
			i.imprimir(Identacion(espacio))
		print espacio, "IN "
		
	def type_check(self,Tabla):
		New_TS = TablaSimbolos(Tabla)
		Tabla.born(New_TS)

		if self.lista:
			print "SCOPE "
			for i in self.lista:
				if isinstance(i, Lista_Declaracion_Base):
					i.type_check(New_TS)
				else:
					print "ERROR: Dentro del alcance del USING ... IN solo puede aparecer la 'Declaracion de Variables'"
					sys.exit(1)
			
			for i in New_TS.dic:
				if New_TS.dic[i] == "int":
					valor = 0
				if New_TS.dic[i] == "string":
					valor = ""
				if  New_TS.dic[i] == "bool":
					valor = "false"
				if New_TS.dic[i] == "set":
					valor = "{}"
				print "  ","Variable: ", i, "Tipo: ", New_TS.dic[i], "Valor: ", valor

		return New_TS

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

	def type_check(self,TablaSimbolos):
		TablaSimbolos = self.declaracion.type_check(TablaSimbolos)

		for i in self.instruccion:
			i.type_check(TablaSimbolos)


# Clase que define la CONDICION
class Condicion:

	def __init__(self,cuerpo,expresion=None,condicion_Else=None,condicion_ElseIf=None):
		self.cuerpo = cuerpo
		self.expresion = expresion
		self.condicion_Else = condicion_Else
		self.condicion_ElseIf = condicion_ElseIf

	def imprimir(self,espacio):
		if self.expresion:
			print espacio, "IF "
			print espacio, "condicion: "			
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

	def type_check(self,TablaSimbolos):

		if self.expresion:
			if self.expresion.type_check(TablaSimbolos) <> "boolean":
				print "ERROR: El tipo de la condicion debe ser booleano"
				sys.exit(1)

		######### REVISAR ##########

		if isinstance(self.cuerpo,list):
			for i in self.cuerpo:
				i.type_check(TablaSimbolos)
		else:
			self.cuerpo.type_check(TablaSimbolos)

		if self.condicion_ElseIf:
			if isinstance(self.condicion_ElseIf,list):
				for i in self.condicion_ElseIf:
					i.type_check(TablaSimbolos)
			else:
				self.type_check(TablaSimbolos)

		if self.condicion_Else:
			if isinstance(self.condicion_Else,list):
				for i in self.condicion_Else:
					i.type_check(TablaSimbolos)
			else:
				self.type_check(TablaSimbolos)

		###############################


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

		print espacio, "FOR "
		print espacio, " Variable: "
		self.identificador.imprimir(Identacion(espacio))
		print espacio, " Direccion: "
		print espacio, espacio, self.direccion
		print espacio, " In"
		if isinstance(self.rango,list):
			print espacio, " Set"
			for j in self.rango:
				j.imprimir(Identacion(espacio))
		else:
			self.rango.imprimir(Identacion(espacio))
			print espacio, "DO "

		if self.instructions:
			self.instructions.imprimir(Identacion(espacio))

	def type_check(self,Tabla):
		New_TS = TablaSimbolos(Tabla)
		Tabla.born(New_TS)

		New_TS.insert(self.identificador.getValue(),"number")
		Tipo_rango = self.rango.type_check(New_TS)

		if self.instructions:
			for j in self.instructions:
				j.type_check(New_TS)


# Clase que define El ciclo Repeat1
class Expre_Repeat1:
	"""
	Repeat1:
		repeat <instrucción 1> while (<condición>) do <instrucción 2>

	"""

	#Constructor de la clase
	def __init__(self,instruccionRp,expression,instructionWh):
		
		self.instruccionRp = instruccionRp
		self.expression = expression 	
		self.instructionWh = instructionWh
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "REPEAT "
		print espacio, " Instruccion: "
		self.instruccionRp.imprimir(Identacion(espacio))
		print espacio, "WHILE "
		print espacio, " Condicion: "
		self.expression.imprimir(Identacion(espacio))
		print espacio, "DO "
		print espacio, " Instruccion: "
		self.instructionWh.imprimir(Identacion(espacio))

	#Funcion para construir la tabla de simbolos
	def type_check(self,TablaSimbolos):

		if self.instruccionRp:
			for i in self.instruccionRp:
				i.type_check(TablaSimbolos)

		if self.expression.type_check(TablaSimbolos) <> "boolean":
			print "ERROR: El tipo de la condicion debe ser booleano"

		if self.instructionWh:
			for j in self.instructionWh:
				j.type_check(TablaSimbolos)




# Clase que define El ciclo Repeat2
class Expre_Repeat2:
	"""
	Repeat2:
	  while (<condición>) do <instrucción 2>

	"""

	#Constructor de la clase
	def __init__(self,expression,instructionWh):
		
		self.expression = expression 	
		self.instructionWh = instructionWh
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "WHILE "
		print espacio, " Condicion:"
		self.expression.imprimir(Identacion(espacio))
		print espacio, " Instruciones:"
		self.instructionWh.imprimir(Identacion(espacio))

	#Funcion para construir la tabla de simbolos
	def type_check(self,TablaSimbolos):

		if self.expression.type_check(TablaSimbolos) <> "boolean":
			print "ERROR: El tipo de la condicion debe ser booleano"

		if self.instructionWh:
			for i in self.instructionWh:
				i.type_check(TablaSimbolos)


# Clase que define El ciclo Repeat1
class Expre_Repeat3:
	"""
	Repeat3:
		repeat <instrucción 1> while (<condición>)

	"""

	#Constructor de la clase
	def __init__(self,instruccionRp,expression):
		
		self.instruccionRp = instruccionRp
		self.expression = expression 	
	
	#Funcion para imprimir
	def imprimir(self,espacio):

		print espacio, "REPEAT "
		print espacio, " Instruciones: "
		self.instruccionRp.imprimir(Identacion(espacio))
		print espacio, "WHILE "
		print espacio, " Condicion:"
		self.expression.imprimir(Identacion(espacio))

	#Funcion para construir la tabla de simbolos
	def type_check(self,TablaSimbolos):

		if self.instruccionRp:
			for i in self.instruccionRp:
				i.type_check(TablaSimbolos)

		if self.expression.type_check(TablaSimbolos) <> "boolean":
			print "ERROR: El tipo de la condicion debe ser booleano"


# Clase que define la EXPRESION UNARIA		
class Exp_Unaria:

	def __init__(self,operador,expresion):	
		self.expresion = expresion 		#Lista de expresiones al lado der del operador 
		self.operador = operador

	def imprimir(self,espacio):
		print espacio, "Operador: " , str(self.operador)
		self.expresion.imprimir(Identacion(espacio))

	def type_check(self,TablaSimbolos):
		Tipo_exp = self.expresion.type_check(TablaSimbolos)

		if Tipo_exp == "boolean" and self.operador == "not":
			return "boolean"

		elif Tipo_exp == "number" and self.operador == "-":
			return "number"

		elif Tipo_exp == "set" and self.operador == ">?":
			return "number"

		elif Tipo_exp == "set" and self.operador == "<?":
			return "number"

		elif Tipo_exp == "set" and self.operador == "$?":
			return "number"

		else:
			print "ERROR: La expresion "
			self.expresion.imprimir("")
			sys.exit(1)


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

	def type_check(self,TablaSimbolos):
		Tipo_exp_der = self.exp_der.type_check(TablaSimbolos)
		Tipo_exp_izq = self.exp_izq.type_check(TablaSimbolos)

		if isinstance(self.exp_izq, Exp_Binaria):
			self.exp_izq = self.exp_izq.type_check(TablaSimbolos)

		if isinstance(self.exp_der, Exp_Binaria):
			self.exp_der = self.exp_der.type_check(TablaSimbolos)

		if isinstance(self.exp_izq, Exp_Unaria):			
			self.exp_izq = self.exp_izq.type_check(TablaSimbolos)

		if isinstance(self.exp_der, Exp_Unaria):
			self.exp_der = self.exp_der.type_check(TablaSimbolos)

		# Tipo number op number = number
		A = self.operador == "+"
		B = self.operador == "-"
		C = self.operador == "*"
		D = self.operador == "/"
		E = self.operador == "%"

		# Tipo set op set = set
		F = self.operador == "++"
		G = self.operador == "\\"
		I = self.operador == "><"

		# Tipo number op set = set
		J = self.operador == "<+>"
		K = self.operador == "<->"
		L = self.operador == "<*>"
		M = self.operador == "</>"
		N = self.operador == "<%>"

		# Tipo number op number = bool
		# Tipo set op set = bool
		# Tipo bool op bool = bool
		O = self.operador == "=="
		P = self.operador == "/="

		# Tipo number op number = bool
		Q = self.operador == ">"
		R = self.operador == "<"
		S = self.operador == ">="
		T = self.operador == "<="

		# Tipo number op set = bool
		U = self.operador == "@"
		
		# Tipo bool op bool = bool
		V = self.operador == "&"
		W = self.operador == "|"


		if Tipo_exp_der == Tipo_exp_izq:

			if Tipo_exp_der == "number":
				if A or B or C or D or E:
					return "number"

				elif O or P or Q or R or S or T:
					return "boolean"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con enteros"
					sys.exit(1)

			elif Tipo_exp_der == "set":
				if F or G or I:
					return "set"

				elif O or P:
					return "boolean"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con conjuntos"
					sys.exit(1)

			elif Tipo_exp_der == "boolean":
				if O or P or V or W:
					return "boolean"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con booleanos"
					sys.exit(1)

		else:

			if Tipo_exp_izq == "number" and Tipo_exp_der == "set":
				if J or K or L or M or N:
					return "set"

				elif U:
					return "boolean"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con enteros y conjuntos"
					sys.exit(1)
