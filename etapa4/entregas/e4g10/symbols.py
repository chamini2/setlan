# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Tabla de símbolos
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

def indent(tabs):
    return "   "*tabs

class SymbolTable:
	def __init__(self):
		self.previousScope = None
		self.currentScope = {}
		self.innerScopes = []

	def __str__(self):
		return self.printTable(0)

	def printTable(self,tabs):
		string = indent(tabs)+"SCOPE\n"
		for var in self.currentScope:
			string += indent(tabs+1) + self.currentScope[var].printSymbol()
		for scope in self.innerScopes:
			string += scope.printTable(tabs+1)
		string += indent(tabs)+"END_SCOPE\n"
		return string

	def insert(self, symbol):
		if not symbol.name in self.currentScope:
			self.currentScope[symbol.name] = symbol
			return True
		return False

	def delete(self, symbol):
		if self.contains(symbolName):
			del self.currentScope[symbolName]
			return True
		return False

	def update(self, name, value, type = None):
		if name in self.currentScope:
			if type:
				self.currentScope[name] = Symbol(name,type,value)
			else:
				self.currentScope[name] = Symbol(name,self.currentScope[name].type,value)
			return True
		elif self.previousScope:
			return self.previousScope.update(name,value,type)
		return False

	def contains(self, symbolName):
		if symbolName in self.currentScope:
			return True
		elif self.previousScope:
			return self.previousScope.contains(symbolName)
		return False

	def lookup(self, symbolName):
		if symbolName in self.currentScope:
			return self.currentScope[symbolName]
		elif self.previousScope:
			return self.previousScope.lookup(symbolName)
		return None


class Symbol(object):
	def __init__(self, name, type, value, iterator = False):
		self.name = name
		self.type = type
		self.value = value
		self.iterator = iterator

	def printSymbol(self):
		if self.type == "set":
			return "Variable: %s | Type: %s  | Value: {}\n"%(self.name,self.type)
		if self.type == "bool":
			value = "false"
			if self.value:
				value = "true"
			return "Variable: %s | Type: %s  | Value: %s\n"%(self.name,self.type,value)
		else:
			return "Variable: %s | Type: %s  | Value: %s\n"%(self.name,self.type,self.value)