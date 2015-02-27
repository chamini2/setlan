#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------
# Setlan
#
# Tabla de simbolos del lenguaje Setlan
# CI-3725
#
# Gustavo Siñovsky 09-11207
# Luiscarlo Rivera 09-11020
# ------------------------------------------------------------

class variable:
	def __init__(self, nombre, tipo, reservado):
		self.nombre = nombre
		self.tipo = tipo
		self.reservado = reservado
		self.definida = False
	
	def update(self, valor):
		self.valor = valor
		self.definida = True
	
	def getValor(self): 
		return self.valor

	def getDefinida(self):
		return self.definida

	def getType(self):
		return self.tipo
	
	def getReservado(self):
		return self.reservado

class Table:
	def __init__(self, padre, esBloque = True):
		self.padre = padre
		self.table = {}
		self.esBloque = esBloque
	
	def insert(self, nombre, tipo, reservado = False):
		if (not self.contains(nombre, True)):
			self.table[nombre] = variable(nombre, tipo, reservado)
			return True
		else: 
			return False 

	def insertFor(self, nombre, tipo):
		a = self
		while (a != None and a.esBloque == False):
			a = a.getPadre()
		if (a != None and a.contains(nombre, True)):
			return False
		else:
			self.table[nombre] = variable(nombre, tipo, True)
			return True

	def delete(self, nombre):
		self.table.pop(nombre) 

	def update(self, nombre, valor):
		a = self.lookup(nombre)
		if (a == None):
			return False
		else: 
			a.update(valor)
			return True

	def getPadre(self):
		return self.padre

	def contains(self, nombre, local):
		if (local):
			return self.table.has_key(nombre)
		else:
			if (self.table.has_key(nombre)):
				return True
			else:
				if (self.padre == None):
					return False
				else:
					return self.padre.contains(nombre, False)

	def lookup(self, nombre, local):
		if (local):
			if (self.table.has_key(nombre)):
				return self.table[nombre]
			else:
				return None
		else:
			if (self.table.has_key(nombre)):
				return self.table[nombre]
			else:
				if (self.padre == None):
					return None
				else:
					return self.padre.lookup(nombre, False)