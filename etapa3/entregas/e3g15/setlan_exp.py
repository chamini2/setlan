#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 24/02/2015
#
#proyecto 3 Traductores e interpretadores ci3725
#
#------------------------------------------------
#expresiones del lenguaje setlan
#------------------------------------------------

from setlan_func import *

class Expressions: pass

#operaciones binarias
class BinOp(Expressions):
  
  def __init__(self,left,op,right):
    self.op  = op
    self.left = left
    self.right = right

  def print_node(self,count):
    tab = tabs(count)
    print tab + operador(self.op) + (self.op) 
    print tab + "\tvariable "
    self.left.print_node(count + 2) 
    print tab + "\tvariable "
    self.right.print_node(count + 2)

#operaciones unarias  
class UnOp(Expressions):
  
  def __init__(self,op,value):
    self.op = op
    self.value = value
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + "\toperador " + op_unario(self.op) 
    print tab + "\toperando "
    self.value.print_node(count + 2)

#tipos de datos
class Type(Expressions): 
  
  def __init__(self,value):
    self.type = "TYPE"
    self.value = value

  def print_node(self,count):
    tab = tabs(count)
    print tab + str(self.value) 

#listas
class List(Expressions):

  def __init__(self,value):
    self.value = value
  
  def print_node(self,count):
    tab = tabs(count)
    for i in range(len(self.value)):
      print tab + self.value[i].name

#numeros
class Number(Expressions):
  
  def __init__(self,value):
    self.value = value

  def print_node(self,count):
    print tabs(count) + "\t"  + str(self.value)

  def traverse(self,count,scope,father):
    return "int"

#IDs (variables)
class Id(Expressions):
  
  def __init__(self,name,column):
    self.name = name
    self.column = column
    self.line     = None

  def setLine(self,line):
    self.line = line
  
  def print_node(self,count):
    print tabs(count + 1) + self.name

  def toString(self):
    return self.name

  def getColumn(self):
    return self.column

  def traverse(self,count,scope,father):
   pass

#booleanos
class Bool(Expressions):
  
  def __init__(self,value):
    self.type = "BOOL"
    self.value = value
    
  def print_node(self,count):
    print tabs(count) + "" + self.type
    print tabs(count) + "\t" + "valor: " + str(self.value)
  
  def traverse(self,count,scope,father):
    return "bool"

#strings
class String(Expressions):
  
  def __init__(self,value):
    self.type = "STRING"
    self.value = value
  
  def print_node(self,count):
    print tabs(count) + self.type
    print tabs(count) + "\t" + "valor: " + str(self.value)
 
#funciones 
class Function(Expressions):
  
  def __init__(self,name,value):
    self.type = "FUNCTION"
    self.name = name
    self.value = value
    
  def print_node(self,count):
    print tabs(count) + "EXPRESSION " + self.type
    print tabs(count) + "\t" + self.name
    print tabs(count) + "\t" + "ARGS"
    self.value.print_node(count + 2)
