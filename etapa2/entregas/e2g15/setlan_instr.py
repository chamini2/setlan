#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 8/02/2015
#
#proyecto 2 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#conjunto de instrucciones de setlan
#-----------------------------------------------

from setlan_func import *

class Instr: pass

#instruccion block
class Block(Instr):
  
  def __init__(self,block_type,instructions):
    self.type = block_type
    self.instructions = instructions
  
  def print_node(self,count):
    tab = tabs(count)
    i = 0
    print tab + self.type
    for ins in self.instructions:
      if not (ins == None):
        ins.print_node(count + 1)
        i += 1
      else:
        print tab + "BLOCK_END"

#instruccion using
class Using(Instr):
  
  def __init__(self,declarations,instructions):
    self.type = "USING"
    self.end = "IN"
    self.declarations = declarations
    self.instructions = instructions
  
  def print_node(self,count):
    tab = tabs(count)
    i = 0
    print tab + self.type
    for dec in self.declarations:
      if not (i == len(self.declarations)-1):
        dec.print_node(count + 1)
        i += 1
    print tab + self.end

    count = 1

    for ins in self.instructions:
      ins.print_node(count + 1)
      i += 1

#instruccion declare
class Declare(Instr):
  
  def __init__(self,dec_type,dec_id):
    self.type = dec_type
    self.id = dec_id
  
  def print_node(self,count):
    tab = tabs(count)
    self.type.print_node(count) 
    self.id.print_node(count)

#instruccion scan
class Scan(Instr):
  
  def __init__(self,var):
    self.type = "SCAN"
    self.var = var
  
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable"
    self.var.print_node(count + 2)

#instruccion assign    
class Assign(Instr):
  
  def __init__(self,var,expr):
    self.type = "ASSIGN"
    self.var = var
    self.expr = expr
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tvalue " 
    self.expr.print_node(count + 1)

#instruccion assign_Set
class Assign_set(Instr):
  
  def __init__(self,var,list_n):
    self.type = "ASSIGN"
    self.var = var
    self.list_n = list_n
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tvalue "
    for i in range(len(self.list_n)):
      print tab + tab + str(self.list_n[i].value) 

#instrucciones print y println
class Fun_print(Instr):
  
  def __init__(self,class_type,variables):
    self.type = class_type
    self.variables = variables
    
  def print_node(self,count):
    tab = tabs(count)
    for var in self.variables:
      print tab + "\telements "
      var.print_node(count + 2)

#instruccion for
class For(Instr):
  
  def __init__(self,var,direction,expression,instruction):
    self.type = "FOR"
    self.var = var
    self.direction = direction
    self.expression = expression
    self.instruction = instruction
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tdirection "
    print tab + tab + self.direction
    print tab + "\tIN " 
    self.expression.print_node(count + 1)
    print tab + "\tDO "
    for i in self.instruction:
      if not (i == None):
        i.print_node(count + 2)
      else:
        print tab + "BLOCK_END"

#instruccion while
class While(Instr):
  
  def __init__(self,condition,instruction):
    self.type = "ITERACION_INDET"
    self.condition = condition
    self.instruction = instruction
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion:"
    self.condition.print_node(count + 2)
    print tab + "\tinstruccion: "
    for i in self.instruction:
      i.print_node(count + 2)
  
#instruccion if then   
class IfThen(Instr):
  
  def __init__(self,condition,instruction):
    self.type = "CONDICIONAL"
    self.condition = condition
    self.instruction = instruction
  
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion: "
    self.condition.print_node(count + 2)
    print tab + "\tverdadero: "
    for i in self.instruction:
      i.print_node(count + 2)

#instruccion if then else
class IfThenElse(Instr):
  
  def __init__(self,condition,instruction1,instruction2):
    self.type = "CONDICIONAL"
    self.condition = condition
    self.instruction1 = instruction1
    self.instruction2 = instruction2
  
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion: "
    self.condition.print_node(count + 2)
    print tab + "\tverdader: "
    for i1 in self.instruction1:
      i1.print_node(count + 2)
    print tab + "\tfalso:"
    for i2 in self.instruction2:
      i2.print_node(count + 2)  
