#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
# Clase que representa la tabla de simbolos
#
class SymTable:

  def __init__(self):
    self.table  = None
    self.father = None
    self.scope  = None

  def new(self):
    self.table  = []
    self.father = -1
    self.scope  = -1
    return self.table
  
  def setScope(self,scope):
    self.scope = scope
  
  def getScope(self):
    return self.scope
  
  def setFather(self,father):
    self.father = father
  
  def getFather(self):
    return self.father
  
  def insert(self,element):
    self.table.append(element)
  
  def delete(self,variable):
    i = 0
    while i < len(self.table):
      if self.table[i].var == variable:
        del self.table[i] 
      i += 1
  
  def find(self,variable):
    i = 0
    while i < len(self.table):
      if self.table[i].var == variable:
        return self.table[i]
      i += 1
    return None

  def update(self,var,var_type,value):
    i = 0
    while i < len(self.table):
      if self.table[i].var == var:
        if var_type != None:
          self.table[i].setType(var_type)
        if var_type != None:
          self.table[i].setValue(value)
      i += 1

  def isMember(self,variable):
    i = 0
    while i < len(self.table):
      if self.table[i].var == variable:
        return True
      i += 1
    return False
  
  #funcion que imprime la tabla de simbolos siempre y cuando no este vacia
  def print_table(self,tab):
    if not self.isEmpty():
      print tab + "SCOPE"
      for e in self.table:
        e.toString(tab)

  def isEmpty(self):
    return (self.table == [])

#clase que representa los elementos de la tabla de simbolos

class Element:
  
  def __init__(self,var,t,value,it):
    self.type  = t
    self.var   = var
    self.value = value
    self.it    = it
  
  def toString(self,tab):
    val =  tab + "Variable: %s | Type: %s | Value: %s"
    print val % (self.var,self.type,self.value)
  
  def getVar(self):
    return str(self.var)
  
  def getType(self):
    return str(self.type)
  
  def getValue(self):
    return self.value
  
  def setVar(self,var1):
    self.var = var1
  
  def setType(self,t1):
    self.type = t1
  
  def setValue(self,value1):
    self.value = value1
  
  def getIt(self):
    return self.it
