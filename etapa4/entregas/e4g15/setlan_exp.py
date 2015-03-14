#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
#------------------------------------------------
#expresiones del lenguaje setlan
#------------------------------------------------

from setlan_func import *

class Expressions: pass

#operaciones binarias
class BinOp(Expressions):
  
  def __init__(self,left,op,right,line,column):
    self.op  = op
    self.left = left
    self.right = right
    self.line   = line
    self.column = column

  def print_node(self,count):
    tab = tabs(count)
    print tab + operador(self.op) + (self.op) 
    print tab + "\tvariable "
    self.left.print_node(count + 2) 
    print tab + "\tvariable "
    self.right.print_node(count + 2)

  def toString(self):
    return self.left.toString() + " " + self.op + " " + self.right.toString()

  def traverse(self,count,scope,father,iswrong):

    if isinstance(self.left,Id):
      self.left.setLine(self.line)
    if isinstance(self.right,Id):
      self.right.setLine(self.line)
    
    _left  = self.left.traverse(count,scope,father,iswrong)
    _right = self.right.traverse(count,scope,father,iswrong)
    if _left != None and _right != None:
      if self.op == "-" or self.op == "/" or self.op == "%":
        if _left == _right and _left == "int":
          return _right
        else:
          type_error(2,self.op,self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
      if self.op == "+":
        if _left == _right and (_left == "int" or _left == "range"):
          return _right
        else: 
          type_error(2,"sumar",self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
      if self.op == "*":
        if _left == _right and _left == "int":
          return _right
        elif _left == "range" and _right == "int":
          return "range"
        else:
          type_error(2,"multiplicar",self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
      if self.op == "<>":
        if _left == _right and _left == "range":
          return "range"
        else:
          type_error(2,"interseccion",self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
      if self.op == ">>":
        if _left == "int" and _right == "range":
          return "bool"
        else:
          type_error(2,"pertenece",self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
      if self.op == "and" or self.op == "or":
        if _left == "bool" and _right == "bool":
          return "bool"
        else:
          type_error(2,self.op,self.left,_left,self.right,_right,self.line)
          iswrong.append(1)
    else:
      iswrong.append(1)

  def evaluate(self,count,scope,father):
    if isinstance(self.left,int): print "self.left (int)" + str(self.left)
    _left = self.left.evaluate(count,scope,father)
    if isinstance(self.right,int): print "self.right (int)" + str(self.right)
    _right = self.right.evaluate(count,scope,father)
    
    if self.op == "+":
      _left_type = self.left.traverse(count,scope,father,0)
      if _left_type == "int":
        overflow(_left + _right,self.line)
        return _left + _right
    elif self.op == "-":
      overflow(_left - _right,self.line)
      return _left - _right
    elif self.op == "%":
      overflow(_left % _right,self.line)
      return _left % _right
    elif self.op == "/":
      if _right == 0:
        div_by_zero(self.line)
      else:
        overflow(_left / _right,self.line)
        return _left / _right 
    elif self.op == "*":
      _left_type  = self.left.traverse(count,scope,father,0)
      _right_type = self.right.traverse(count,scope,father,0)
      overflow(_left * _right,self.line)
      return _left * _right
    elif self.op == "and":
      if _left.toString() == "false" or _right.toString() == "false":
        return Bool("false",self.line,self.column)
      elif _left.toString() == "true" and _right.toString() == "true":
        return Bool("true",self.line,self.column)
    elif self.op == "or":
      if _left.toString() == "true" or _right.toString() == "true":
        return Bool("true",self.line,self.column)
      else:
        return Bool("false",self.line,self.column)

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

  def evaluate(self,count,scope,father):
    if self.op == "-":
      return (- self.value.evaluate(count,scope,father))
    elif self.op == "not":
      value = self.value.evaluate(count,scope,father)
      if value.toString() == "true":
        return Bool("false",self.line,self.column)
      elif value.toString() == "false":
        return Bool("true",self.line,self.column)
    return None

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

  def traverse(self,count,scope,father,iswrong):
    return "int"

  def evaluate(self,count,scope,father):
    return self.value

  def toString(self):
    return str(self.value)

#IDs (variables)
class Id(Expressions):
  
  def __init__(self,name,column):
    self.name = name
    self.column = column
    self.line = None

  def setLine(self,line):
    self.line = line
  
  def print_node(self,count):
    print tabs(count + 1) + self.name

  def toString(self):
    return self.name

  def getColumn(self):
    return self.column

  def traverse(self,count,scope,father,iswrong):
   pass

  def evaluate(self,count,scope,father):
   elem  = find_in_scopes(self,count,0,scope,"",self.line)
   value = elem.getValue()

   if value == None:
     not_initialized(self,self.line)
   else: return value

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

  def evaluate(self,count,scope,father):
    return self

#strings
class String(Expressions):
  
  def __init__(self,value):
    self.type = "STRING"
    self.value = value
  
  def print_node(self,count):
    print tabs(count) + self.type
    print tabs(count) + "\t" + "valor: " + str(self.value)

  def evaluate(self,count,scope,father):
    return self.value

  def getColumn(self):
    return self.column
  
  def toString(self):
    return self.value

  def traverse(self,count,scope,father,iswrong): pass

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

  def evaluate(self,count,scope,father):
    if isinstance(self.value,Id):
      self.value = find_in_scopes(self.value,count,father,scope,self.type,self.line)
      self.value = self.value.getValue()
      _tmp = self.value.toString().split()
      self.value = Range(int(_tmp[0]),_tmp[1],int(_tmp[2]),self.line,self.column)
    return None
