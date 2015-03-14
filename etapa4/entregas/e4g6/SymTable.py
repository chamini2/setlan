# -*- coding: UTF-8 -*-

##########################################
# CI3725 Traductores e Interpretadores   #
# Entrega 4. Grupo 6                     #
# Maria Victoria Jorge 11-10495          #
# Enrique Iglesias 11-10477              # 
##########################################


class Tabla:
	def __init__(self,padre = None):
		self.dic = {}
		self.padre = padre

	def insert(self,clave,valor,tipo):
		if not(clave in self.dic.keys()):
			self.dic[clave] = [valor,tipo]

	def delete(self,clave):
		if (clave in self.dic.keys()):
			del self.dic[clave]

	def update(self,clave,valor,tipo):
		if (clave in self.dic.keys()) and (self.dic[clave][1] == tipo):
			self.dic[clave] = [valor,tipo]
		else: 
			if (self.padre != None):
				self.padre.update(clave,valor,tipo)

	def contains(self,clave):
		if not(self.isInTable(clave)):
			if (self.padre != None):
				return self.padre.contains(clave)
			else:
				return None
		return self.isInTable(clave)

	def isInTable(self,clave):
		return clave in self.dic.keys()

	def lookup(self,clave):
		if (clave in self.dic.keys()):
			return self.dic[clave]
		else:
			if (self.padre != None):
				return self.padre.lookup(clave)
		return None

	def getFather(self):
		return self.padre


