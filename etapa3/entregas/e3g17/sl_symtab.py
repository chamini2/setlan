# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Tercera entrega del proyecto.             #
#   Definicion de la Tabla de Simbolos        #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

# Clase definicion de Symbol Table

class SymTab:
	
	# Se implementa la Tabla de Simbolos utilizando para ello
	# la estructura 'dict' de python. Cada entrada esta
	# compuesta de dos tuplas: la clave es una tupla
	# (name, dec_scope), y el valor es una tupla
	# (type, val, lin_dec). A continuacion
	# el significado de estos atributos:

	# name: nombre de la variable (identificador)
	# type: tipo de la variable (int, set, bool)
	# val: valor inicial de la variable (0, false, {})
	# dec_scope: nro. de scope donde se declara la variable
	# lin_dec: linea del programa en que se declaro la variable.
	# read_only: con 1 especifica que la variable es de solo lectura (de un FOR)		 

	def __init__(self):
		self.st = {}

	def insert(self, name, dec_scope, type, val, lin_dec, read_only=0):
		if not self.contains(name, dec_scope):
			self.st[(name, dec_scope)] = (type, val, lin_dec, read_only)
			return True
		else:
			return False

	def delete(self, name, dec_scope, type, val, lin_dec, read_only=0):
		if self.contains(name, dec_scope) and self.st[(name, dec_scope)] == (type, val, lin_dec, read_only):
			del self.st[(name, dec_scope)]
			return True
		else:
			return False

	def update(self, name, dec_scope, type, val, lin_dec, read_only=0):
		if self.contains(name, dec_scope):
			self.st[(name, dec_scope)] = (type, val, lin_dec, read_only)
			return True
		else:
			return False

	def contains(self, name, dec_scope):
		return (name, dec_scope) in self.st.keys()

	def lookup(self, name, dec_scope):
		if self.contains(name, dec_scope):
			return self.st[(name, dec_scope)]
		else:
			return False

	def typeof(self, name, dec_scope):
		if self.contains(name, dec_scope):
			return self.st[(name, dec_scope)][0]
		else:
			return False

	def valof(self, name, dec_scope):
		if self.contains(name, dec_scope):
			return self.st[(name, dec_scope)][1]
		else:
			return False

	def lin_decof(self, name, dec_scope):
		if self.contains(name, dec_scope):
			return self.st[(name, dec_scope)][2]
		else:
			return False

	def isreadonly(self, name, dec_scope):
		return self.st[(name, dec_scope)][3] == 1

	def var_list(self):
		return self.st.keys()

	def var_str(self, name, dec_scope):
		if self.contains(name, dec_scope):
			type = self.typeof(name, dec_scope)
			val = self.valof(name, dec_scope)
			return "Variable: " + name + "\t| Type: " + type + "\t| Value: " + str(val)
		else:
			return False

	def __str__(self):
		return str(self.st)



# Clase definicion de Pila de Symbol Tables

class ST_Stack:

	def __init__(self):
		self.stack = []

	def push(self, st):
		if not isinstance(st, SymTab): return False
		else:
			self.stack.append(st)
			return True

	def pop(self):
		if self.isempty(): return False
		else: return self.stack.pop()

	def top(self):
		if self.isempty(): return False
		else: return self.stack[-1]

	def bottom(self):
		if self.isempty(): return False
		else: return self.stack[0]

	def isempty(self):
		return len(self.stack) == 0

	def __str__(self):
		s = ""
		for i in self.stack:
			s = s + str(i) + ", "
		s = s[:-2]
		return "[" + s + "]"