#!/usr/bin/python
#encoding: utf-8

#############################################################################
## 							   Proyecto traductores e Interpretadores  							   ##
##															    SETLAN												  		   ##
#############################################################################
#																																						#
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

Results = []

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
		#self.imprimir("")
		New_TS = TablaSimbolos(None)
		self.type_check(New_TS)
		self.execute({})

	def imprimir(self,espacio):
		print espacio, "PROGRAM "
		self.cuerpo.imprimir(Identacion(espacio))
		print espacio, "PROGRAM_END"

	def type_check(self,TablaSimbolos):
		self.cuerpo.type_check(TablaSimbolos)

	def execute(self,dic):
		Results.append(dic)
		self.cuerpo.execute(dic)


# Clase que defina a los boolean
class Boolean:

	def __init__(self,value):
		if value == None:
			self.value = "false"
		else:
			self.value = value						
		self.type = "bool"

	def getValue(self):
		return self.value

	def imprimir(self,espacio):
		print espacio, " String: ", str(self.value)

	def type_check(self,TablaSimbolos):
		return self.type

	def execute(self,dic):
		if self.value == "true":
			return True
		elif self.value == "false":
			return False

		print "/ERROR/: El booleano esta mal declarado "
		sys.exit(1)

# Clase que defina a los identificadores
class Identificador:

	def __init__(self,value):
		self.value = str(value)
		self.type = "id"

	def getValue(self):
		return self.value

	def imprimir(self,espacio):
		print espacio, "Variable ", str(self.value)

	def buscarEnDic(self,dic,identificador):
		i = len(Results) - 1
		while i >= 0:
			if Results[i].has_key(identificador):
				return Results[i][identificador]
			i = i-1

	def type_check(self,TablaSimbolos):
		if TablaSimbolos.contains(self.value) == False:
			print "ERROR: El identificador no se encuentra en la Tabla de Simbolos: " + str(self.value)
			sys.exit(1)

		return TablaSimbolos.Tipo(self.value)

	def execute(self,dic):
		return self.buscarEnDic(dic,self.value)


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

	def execute(self,dic):
		return self.getValue()


# Clase que define a los Numeros
class Number:

	def __init__(self,numero):
		self.numero = numero
		self.type = "int"

	def getValue(self):
		return self.numero

	def imprimir(self,espacio):
		print espacio, "Int ", self.numero

	def type_check(self,TablaSimbolos):
		return self.type

	def execute(self,dic):
		return self.getValue()


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
	
	def type_check(self,TablaSimbolos):
		if isinstance(self.lista,list):
			for i in self.lista:
				if i.type_check(TablaSimbolos):
					print str(i.type_check(TablaSimbolos))
				else:
					print "ERROR: No se puede asignar '" + str(i) + \
								"' al dentro del conjunto"
  	 			sys.exit(1)
			return self.type

	def execute(self,dic):
		return self.getValue()


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
# class Expre_Conjunto:

# 	def __init__(self,expresion):
# 		self.expresion = expresion

# 	def imprimir(self,espacio):
# 		print espacio, "Conjunto"
# 		print espacio, "Valor(es)"
# 		if self.expresion:
# 			for j in self.expresion:
# 				j.imprimir(Identacion(espacio))

# 	def type_check(self,TablaSimbolos):
# 		if isinstance(self.expresion,list):
# 			for i in self.expresion:
# 				i.type_check(TablaSimbolos)
# 		else:
# 			self.expresion.type_check(TablaSimbolos)


# Clase que define ASIGN
class Asignacion_Conj:

	def __init__(self,identificador,expresion):
		self.expresion = expresion
		self.identificador = identificador


	def imprimir(self,espacio):
		print espacio, "ASIGNACION "
		self.identificador.imprimir(Identacion(espacio))
		self.expresion.imprimir(Identacion(espacio))

	def type_check(self,TablaSimbolos):
		if TablaSimbolos.dic.has_key(self.identificador.getValue()) == False:
			print "ERROR: Variable '" + str(self.identificador.getValue()) + \
						"' no esta declarada dentro del alcance"
			sys.exit(1)

		else:
			Tipo_id = self.identificador.type_check(TablaSimbolos)
			Tipo_exp = self.expresion.type_check(TablaSimbolos)

			#if Tipo_id == "number" or Tipo_id == "boolean" or Tipo_exp == "number" or Tipo_exp == "boolean":
			if Tipo_id <> Tipo_exp:
				print "ERROR: El tipo del identificador y de la expresion son distintos"
				sys.exit(1)

	def execute(self,dic):
		if isinstance(expresion,list):
			if len(expresion) == 0:
				dic[self.identificador.getValue()] = set()
			else:
				aux = set()
				for i in expresion:
					aux.add(i)
				dic[self.identificador.getValue()] = aux


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

	def type_check(self,Tabla):
		if Tabla.contains(self.identificador.getValue()) == False:
			print "ERROR: La variable '" + str(self.identificador.getValue()) + "' no ha sido declarada"
			sys.exit(1)

		else:
			Tipo_id = self.identificador.type_check(Tabla)
			Tipo_exp = self.expresion.type_check(Tabla)

			#if Tipo_id == "int" or Tipo_id == "boolean" or Tipo_exp == "int" or Tipo_exp == "boolean":
			if Tipo_id <> Tipo_exp:
				print "ERROR: El tipo del identificador y de la expresion son distintos"
				sys.exit(1)

		# Tabla.insert(self.identificador.getValue(),self.expresion)

	def execute(self,dic):
		dic[self.identificador.getValue()] = self.expresion.execute(dic)


# Clase que define la funcion Scan
class Scan_Entrada(object):

  def __init__(self,variable):
    self.variable = variable

  def imprimir(self,espacio):
    print espacio, "SCAN "
    self.variable.imprimir(Identacion(espacio))

  def type_check(self,TablaSimbolos):
  	if TablaSimbolos.contains(self.variable.getValue()) == False:
  		print "ERROR: El valor de la variable '" + str(self.variable) +\
  				  "' no coincide con SCAN"

  def execute(self,dic):
  	entrada = raw_input()
  	if entrada== "true" and self.variable.execute(dic) == "bool":
  		entrada = True
  	elif entrada== "false" and self.variable.execute(dic) == "bool":
  		entrada = False
  	elif isinstance(int(entrada),int) and self.variable.execute(dic) == "int":
  		entrada = int(entrada)
  	else:
  		print "ERROR: solo se aceptan booleanos o enteros."
  		exit()

  	dic[self.variable.getValue()] = entrada
         
 
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

  def execute(self,dic):
  	aux = ""
  	for j in self.ImprimeExpresion:
  		aux = aux + str(j.execute(dic)) + " "
		print aux,"\n"
 
 
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

  def execute(self,dic):
  	aux = ""
  	for j in self.ImprimeExpresion:
  		aux = aux + str(j.execute(dic)) + " "
		print aux


# Clase que define la LISTA DE DECLARACIONES BASE
class Lista_Declaracion_Base:
	"""
		<tipo> <identificador>;

	"""

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

	def execute(self,dic):
		for i in self.identificador:
			dic[i.getValue()] = self.tipo


# Clase que define la LISTA DE DECLARACIONES
class Declaracion:
	"""
		USING
			<Lista_Declaracion_Base>
		IN

	"""

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
			#print "SCOPE "
			if isinstance(self.lista,list):
				for i in self.lista:
					if isinstance(i, Lista_Declaracion_Base):
						i.type_check(New_TS)
					else:
						print "ERROR: Dentro del alcance del USING ... IN solo puede aparecer la 'Declaracion de Variables'"
						sys.exit(1)
			else:
				self.lista.type_check(New_TS)

			for i in New_TS.dic:
				if New_TS.dic[i] == "int":
					valor = 0
				if New_TS.dic[i] == "string":
					valor = ""
				if  New_TS.dic[i] == "bool":
					valor = "false"
				if New_TS.dic[i] == "set":
					valor = "{}"
				#print "  ","Variable: ", i, "| Tipo: ", New_TS.dic[i], "| Valor: ", valor

		return New_TS

	def execute(self,dic):
		for i in self.lista:
			i.execute(dic)


# Clase que define al BLOQUE
class Bloque:
	"""
		{
			<declaracion>
			<instrucciones>
		}

	"""

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
		if self.declaracion:
			TablaSimbolos = self.declaracion.type_check(TablaSimbolos)

		for i in self.instruccion:
			i.type_check(TablaSimbolos)

	def execute(self,dic):
		dic = {}
		Results.append(dic)

		if self.declaracion:
			self.declaracion.execute(dic)	

		if self.instruccion:
			for j in self.instruccion:
				j.execute(dic)	

		Results.pop()



# Clase que define la CONDICION
class Condicion:

	def __init__(self,cuerpo,expresion=None,condicion_Else=None):
		self.cuerpo = cuerpo
		self.expresion = expresion
		self.condicion_Else = condicion_Else
		#self.condicion_ElseIf = condicion_ElseIf

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
		# if self.condicion_ElseIf:
		# 	print espacio, "ELSE IF "
		# 	if isinstance(self.condicion_ElseIf,list):
		# 		for k in self.condicion_ElseIf:
		# 			print espacio, "Instruciones: "
		# 			k.imprimir(Identacion(espacio)) #imprime las instrucciones del else if
		# 	else:
		# 		print espacio, "Instruccion: "
		# 		self.condicion_ElseIf.imprimir(Identacion(espacio))

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
			if self.expresion.type_check(TablaSimbolos) <> "bool":
				print "ERROR: El tipo de la condicion debe ser booleano"
				sys.exit(1)

		if isinstance(self.cuerpo,list):
			for i in self.cuerpo:
				i.type_check(TablaSimbolos)
		else:
			self.cuerpo.type_check(TablaSimbolos)

		# if self.condicion_ElseIf:
		# 	if isinstance(self.condicion_ElseIf,list):
		# 		for i in self.condicion_ElseIf:
		# 			i.type_check(TablaSimbolos)
		# 	else:
		# 		self.type_check(TablaSimbolos)

		if self.condicion_Else:
			if isinstance(self.condicion_Else,list):
				for i in self.condicion_Else:
					i.type_check(TablaSimbolos)
			else:
				self.condicion_Else.type_check(TablaSimbolos)


	def execute(self,dic):
		if self.expresion.execute(dic):
			if self.cuerpo:
				if isinstance(self.cuerpo,list):
					for j in self.cuerpo:
						j.execute(dic)
				else:
					self.cuerpo.execute(dic)
		else:	
			if self.condicion_Else:
				if isinstance(self.condicion_Else,list):
					for k in self.condicion_Else:
						k.execute(dic)
				else:
					self.condicion_Else.execute(dic)


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

		New_TS.insert(self.identificador.getValue(),"int")
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

		if self.expression.type_check(TablaSimbolos) <> "bool":
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

		if self.expression.type_check(TablaSimbolos) <> "bool":
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

		if self.expression.type_check(TablaSimbolos) <> "bool":
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

		if Tipo_exp == "bool" and self.operador == "not":
			return "bool"

		elif Tipo_exp == "int" and self.operador == "-":
			return "int"

		elif Tipo_exp == "set" and self.operador == ">?":
			return "int"

		elif Tipo_exp == "set" and self.operador == "<?":
			return "int"

		elif Tipo_exp == "set" and self.operador == "$?":
			return "int"

		else:
			print "ERROR: La expresion "
			self.expresion.imprimir("")
			sys.exit(1)

	def execute(self,dic):
		Tipo_exp = self.expresion.execute(dic)

		if isinstance(Tipo_exp,bool) and self.operador == "not":
			return not(Tipo_exp)

		elif isinstance(Tipo_exp,int) and self.operador == "-":
			return -(Tipo_exp)

		elif isinstance(Tipo_exp,set) and self.operador == "<?":
			tupla = tuple(Tipo_exp)
			return min(tupla)

		elif isinstance(Tipo_exp,set) and self.operador == ">?":
			tupla = tuple(Tipo_exp)
			return max(tupla)

		elif isinstance(Tipo_exp,set) and self.operador == "$?":
			return len(Tipo_exp)

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

		# Tipo int op int = int
		A = self.operador == "+"
		B = self.operador == "-"
		C = self.operador == "*"
		D = self.operador == "/"
		E = self.operador == "%"

		# Tipo set op set = set
		F = self.operador == "++"
		G = self.operador == "\\"
		I = self.operador == "><"

		# Tipo int op set = set
		J = self.operador == "<+>"
		K = self.operador == "<->"
		L = self.operador == "<*>"
		M = self.operador == "</>"
		N = self.operador == "<%>"

		# Tipo int op int = bool
		# Tipo set op set = bool
		# Tipo bool op bool = bool
		O = self.operador == "=="
		P = self.operador == "/="

		# Tipo int op int = bool
		Q = self.operador == ">"
		R = self.operador == "<"
		S = self.operador == ">="
		T = self.operador == "<="

		# Tipo int op set = bool
		U = self.operador == "@"
		
		# Tipo bool op bool = bool
		V = self.operador == "and"
		W = self.operador == "or"


		if Tipo_exp_der == Tipo_exp_izq:

			if Tipo_exp_der == "int":
				if A or B or C or D or E:
					return "int"

				elif O or P or Q or R or S or T:
					return "bool"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con enteros"
					sys.exit(1)

			elif Tipo_exp_der == "set":
				if F or G or I:
					return "set"

				elif O or P:
					return "bool"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con conjuntos"
					sys.exit(1)

			elif Tipo_exp_der == "bool":
				if O or P or V or W:
					return "bool"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con booleanos"
					sys.exit(1)

		else:

			if Tipo_exp_izq == "int" and Tipo_exp_der == "set":
				if J or K or L or M or N:
					return "set"

				elif U:
					return "bool"

				else:
					print "ERROR: El operador " + str(self.operador) + " no opera con enteros y conjuntos"
					sys.exit(1)

	def execute(self,dic):

		ExpresionBaseR =  self.exp_der
		ExpresionBaseL = self.exp_izq

		RightType = ExpresionBaseR.execute(dic)
		LeftType = ExpresionBaseL.execute(dic)

		if isinstance(ExpresionBaseL, Identificador):
			ExpresionBaseL = Number(ExpresionBaseL.execute(dic))

		if isinstance(ExpresionBaseR, Identificador):
			ExpresionBaseR = Number(ExpresionBaseR.execute(dic))

		if isinstance(ExpresionBaseL, Exp_Binaria):
			ExpresionBaseL = Number(ExpresionBaseL.execute(dic))

		if isinstance(ExpresionBaseR, Exp_Binaria):
			ExpresionBaseR = Number(ExpresionBaseR.execute(dic))

		if isinstance(ExpresionBaseL, Exp_Unaria):
			ExpresionBaseL = Number(ExpresionBaseL.execute(dic))

		if isinstance(ExpresionBaseR, Exp_Unaria):
			ExpresionBaseR = Number(ExpresionBaseR.execute(dic))


		# para operaciones con int op int
		if isinstance(ExpresionBaseR,Number) and isinstance(ExpresionBaseL,Number):

			if self.operador == "+":
				return LeftType + RightType
			elif self.operador == "-":
				return LeftType - RightType
			elif self.operador == "*":
				return LeftType * RightType
			elif self.operador == "/":
				return LeftType / RightType
			elif self.operador == "%":
				return LeftType % RightType

			elif self.operador == "==":
				return LeftType == RightType
			elif self.operador == "/=":
				return LeftType != RightType
			elif self.operador == ">":
				return LeftType > RightType
			elif self.operador == "<":
				return LeftType < RightType
			elif self.operador == ">=":
				return LeftType >= RightType
			elif self.operador == "<=":
				return LeftType <= RightType

		# para operaciones con bool op bool
		if isinstance(ExpresionBaseR,Boolean) and isinstance(ExpresionBaseL,Boolean):

			if self.operador == "and":
				return LeftType and RightType
			elif self.operador == "or":
				return LeftType or RightType
			elif self.operador == "==":
				return LeftType == RightType
			elif self.operador == "/=":
				return LeftType != RightType

		# para operaciones con set op set
		if isinstance(ExpresionBaseR,Sets) and isinstance(ExpresionBaseL,Sets):

			if self.operador == "++":
				return LeftType | RightType
			elif self.operador == "\\":
				return LeftType - RightType
			elif self.operador == "><":
				return LeftType & RightType

			elif self.operador == "==":
				return LeftType == RightType
			elif self.operador == "/=":
				return LeftType != RightType

		# para operaciones con int op set
		if isinstance(ExpresionBaseR,Number) and isinstance(ExpresionBaseL,Sets):

			if self.operador == "<+>":
				tupla = tuple(RightType)
				for i in tupla:
					LeftType + i
				return tupla   
				###### retornar tupla o una var que contenga la tupla nueva

			elif self.operador == "<->":
				tupla = tuple(RightType)
				for i in tupla:
					LeftType - i
				return tupla   
				###### retornar tupla o una var que contenga la tupla nueva

			elif self.operador == "<*>":
				tupla = tuple(RightType)
				for i in tupla:
					LeftType * i
				return tupla   
				###### retornar tupla o una var que contenga la tupla nueva

			elif self.operador == "</>":
				tupla = tuple(RightType)
				for i in tupla:
					LeftType / i
				return tupla   
				###### retornar tupla o una var que contenga la tupla nueva

			elif self.operador == "<%>":
				tupla = tuple(RightType)
				for i in tupla:
					LeftType % i
				return tupla   
				###### retornar tupla o una var que contenga la tupla nueva

			elif self.operador == "@":
				return LeftType in RightType
